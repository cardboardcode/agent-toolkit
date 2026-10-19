#!/usr/bin/env python3
"""Helper script to create a draft (pending) PR review on GitHub.

This script validates all comment line numbers against the PR diff hunks
before posting, automatically corrects line offsets when code matches are found,
and retries with isolated comments if GitHub encounters line resolution issues.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Set, Tuple


def get_auth_token(provided_token: Optional[str] = None) -> str:
    """Retrieve GitHub token from argument, env variables, or `gh auth token`."""
    if provided_token:
        return provided_token
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        res = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True,
        )
        token = res.stdout.strip()
        if token:
            return token
    except Exception:
        pass
    print(
        "ERROR: No GitHub token found. Please set GITHUB_TOKEN / GH_TOKEN "
        "or authenticate using 'gh auth login'.",
        file=sys.stderr,
    )
    sys.exit(1)


def parse_pr_url(url_or_slug: str) -> Tuple[str, str, int]:
    """Parse GitHub PR URL or 'owner/repo/pull/123' format into (owner, repo, pr_number)."""
    pattern = r"(?:https?://github\.com/)?([^/]+)/([^/]+)/pull/(\d+)"
    match = re.search(pattern, url_or_slug)
    if not match:
        raise ValueError(
            f"Invalid PR identifier or URL: '{url_or_slug}'. "
            "Expected format: https://github.com/owner/repo/pull/123 or owner/repo/pull/123"
        )
    return match.group(1), match.group(2), int(match.group(3))


def github_api_request(
    endpoint: str,
    token: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    headers_extra: Optional[Dict[str, str]] = None,
) -> Any:
    """Make an authenticated request to the GitHub REST API."""
    url = f"https://api.github.com{endpoint}" if endpoint.startswith("/") else endpoint
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "GitHub-Draft-PR-Reviewer",
    }
    if headers_extra:
        headers.update(headers_extra)

    body_bytes = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            if resp.headers.get("content-type", "").startswith("application/json"):
                return json.loads(content) if content else {}
            return content
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub API error ({e.code} {e.reason}) on {method} {url}:\n{err_msg}"
        ) from e


def get_pr_head_commit(owner: str, repo: str, pull_number: int, token: str) -> str:
    """Fetch the latest HEAD commit SHA for a pull request."""
    pr_data = github_api_request(
        f"/repos/{owner}/{repo}/pulls/{pull_number}",
        token=token,
    )
    return pr_data["head"]["sha"]


def fetch_pr_diff(owner: str, repo: str, pull_number: int, token: str) -> str:
    """Fetch raw unified diff for the PR."""
    try:
        res = subprocess.run(
            ["gh", "pr", "diff", str(pull_number), "-R", f"{owner}/{repo}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout
    except Exception:
        return github_api_request(
            f"/repos/{owner}/{repo}/pulls/{pull_number}",
            token=token,
            headers_extra={"Accept": "application/vnd.github.diff"},
        )


def parse_diff_hunks(diff_str: str) -> Dict[str, Dict[str, Any]]:
    """Parse diff into mapping: file_path -> {'valid_lines': set(), 'hunk_lines': {line: text}}."""
    files_map = {}
    current_file = None
    hunk_regex = re.compile(r"^@@\s+-(?:\d+)(?:,\d+)?\s+\+(\d+)(?:,(\d+))?\s+@@")
    file_regex = re.compile(r"^diff --git a/(.*?) b/(.*?)$")

    lines = diff_str.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        file_match = file_regex.match(line)
        if file_match:
            current_file = file_match.group(2)
            files_map[current_file] = {"valid_lines": set(), "hunk_lines": {}}
            i += 1
            continue

        if current_file:
            hunk_match = hunk_regex.match(line)
            if hunk_match:
                new_start = int(hunk_match.group(1))
                curr_line_no = new_start

                i += 1
                while i < len(lines) and not lines[i].startswith("diff --git ") and not lines[i].startswith("@@"):
                    hunk_l = lines[i]
                    if hunk_l.startswith("+") or hunk_l.startswith(" "):
                        files_map[current_file]["valid_lines"].add(curr_line_no)
                        files_map[current_file]["hunk_lines"][curr_line_no] = hunk_l[1:]
                        curr_line_no += 1
                    i += 1
                continue
        i += 1

    return files_map


def extract_keywords_from_comment(comment_body: str) -> List[str]:
    """Extract code snippets or identifiers from comment body for line matching."""
    sugg_match = re.search(r"```suggestion\s*\n(.*?)\n```", comment_body, re.DOTALL)
    if sugg_match:
        lines = [l.strip() for l in sugg_match.group(1).split("\n") if l.strip()]
        if lines:
            return lines

    inline_codes = re.findall(r"`([^`\n]+)`", comment_body)
    return [c.strip() for c in inline_codes if len(c.strip()) > 3]


def pre_validate_and_reconcile_comments(
    comments: List[Dict[str, Any]],
    diff_map: Dict[str, Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Validate each comment against diff hunks; attempt auto-alignment for out-of-range lines."""
    valid_comments = []
    out_of_diff_comments = []

    print(f"Pre-validating {len(comments)} comments against PR diff hunks...", file=sys.stderr)

    for c in comments:
        path = c.get("path")
        orig_line = int(c.get("line", 1))
        body = c.get("body", "")

        if path not in diff_map:
            print(f" - [Out-of-Diff] {path}:{orig_line}: File not modified in this PR.", file=sys.stderr)
            out_of_diff_comments.append(c)
            continue

        file_valid_lines: Set[int] = diff_map[path]["valid_lines"]
        file_hunk_lines: Dict[int, str] = diff_map[path]["hunk_lines"]

        if orig_line in file_valid_lines:
            valid_comments.append(c)
            continue

        print(f" - [Line Check] {path}:{orig_line} is outside diff hunk. Attempting auto-alignment...", file=sys.stderr)
        keywords = extract_keywords_from_comment(body)
        matched_line = None

        if keywords:
            for kw in keywords:
                for l_no, text in file_hunk_lines.items():
                    if kw in text or text.strip() in kw:
                        matched_line = l_no
                        break
                if matched_line:
                    break

        if matched_line and matched_line in file_valid_lines:
            print(f"   Reconciled {path}:{orig_line} -> {path}:{matched_line}", file=sys.stderr)
            reconciled_comment = dict(c)
            reconciled_comment["line"] = matched_line
            valid_comments.append(reconciled_comment)
        else:
            print(f"   Could not resolve line in diff hunk for {path}:{orig_line}. Moving to review summary.", file=sys.stderr)
            out_of_diff_comments.append(c)

    return valid_comments, out_of_diff_comments


def get_existing_pending_review(
    owner: str, repo: str, pull_number: int, token: str
) -> Optional[Dict[str, Any]]:
    """Check if the user already has an active pending review on this PR."""
    try:
        reviews = github_api_request(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews",
            token=token,
        )
        if isinstance(reviews, list):
            for r in reviews:
                if r.get("state") == "PENDING":
                    return r
    except Exception:
        pass
    return None


def delete_pending_review(
    owner: str, repo: str, pull_number: int, review_id: int, token: str
) -> None:
    """Delete an existing pending review."""
    try:
        github_api_request(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}",
            token=token,
            method="DELETE",
        )
    except Exception as e:
        print(f"Warning: Could not delete pending review #{review_id}: {e}", file=sys.stderr)


def format_review_summary(
    summary_body: str,
    model_name: Optional[str] = None,
    include_attribution: bool = True,
    out_of_diff_notes: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Format the review summary body with model attribution and out-of-diff notes."""
    result = ""
    if include_attribution:
        resolved_model = (
            model_name
            or os.environ.get("AI_MODEL")
            or os.environ.get("LLM_MODEL")
            or os.environ.get("MODEL_NAME")
        )
        model_label = f" ({resolved_model})" if resolved_model else ""
        if "AI-Assisted Code Review" not in summary_body:
            result += (
                f"AI-Assisted Code Review{model_label}: This draft review was generated "
                "via a 3-agent multi-perspective analysis (Correctness, Architecture, Guidelines). "
                "Please review and adjust findings before final submission.\n\n"
            )

    result += summary_body

    if out_of_diff_notes:
        result += "\n\nGeneral / Out-of-Diff Notes:\n"
        for note in out_of_diff_notes:
            result += f"\n* `{note.get('path')}:{note.get('line')}`:\n{note.get('body')}\n"

    return result


def post_draft_review(
    owner: str,
    repo: str,
    pull_number: int,
    commit_id: str,
    summary_body: str,
    comments: List[Dict[str, Any]],
    token: str,
    model_name: Optional[str] = None,
    include_attribution: bool = True,
) -> Dict[str, Any]:
    """Create a pending (draft) review with verified inline comments."""
    review_endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews"

    # Step 1: Fetch and parse PR diff to build valid line ranges
    diff_text = fetch_pr_diff(owner, repo, pull_number, token)
    diff_map = parse_diff_hunks(diff_text)

    # Step 2: Pre-validate comments against diff ranges and reconcile line offsets
    valid_comments, out_of_diff_comments = pre_validate_and_reconcile_comments(comments, diff_map)

    # Step 3: Delete existing pending review if any exists
    existing_review = get_existing_pending_review(owner, repo, pull_number, token)
    if existing_review:
        print(f"Replacing existing pending review #{existing_review['id']}...", file=sys.stderr)
        delete_pending_review(owner, repo, pull_number, existing_review["id"], token)

    formatted_summary = format_review_summary(
        summary_body,
        model_name=model_name,
        include_attribution=include_attribution,
        out_of_diff_notes=out_of_diff_comments,
    )

    clean_comments = [
        {
            "path": c["path"],
            "line": int(c["line"]),
            "side": c.get("side", "RIGHT"),
            "body": c["body"],
        }
        for c in valid_comments
    ]

    # Step 4: Batch review creation
    payload = {
        "commit_id": commit_id,
        "body": formatted_summary,
        "comments": clean_comments,
    }

    try:
        result = github_api_request(
            review_endpoint, token=token, method="POST", data=payload
        )
        print(
            f"Successfully posted pending review #{result.get('id')} with {len(clean_comments)} inline comments "
            f"and {len(out_of_diff_comments)} summary notes.",
            file=sys.stderr,
        )
        return result
    except RuntimeError as batch_err:
        print(
            f"Warning: Batch creation failed ({batch_err}). Running isolation pass on comments...",
            file=sys.stderr,
        )

    # Step 5: Retry & Isolation fallback if GitHub rejected line numbers
    tested_valid_comments = []
    failed_comments = list(out_of_diff_comments)

    for c in clean_comments:
        test_payload = {
            "commit_id": commit_id,
            "body": "validation_test",
            "comments": [c],
        }
        try:
            test_rev = github_api_request(
                review_endpoint, token=token, method="POST", data=test_payload
            )
            delete_pending_review(owner, repo, pull_number, test_rev["id"], token)
            tested_valid_comments.append(c)
        except RuntimeError:
            print(f"Line {c.get('path')}:{c.get('line')} rejected by GitHub. Moving to summary.", file=sys.stderr)
            failed_comments.append(c)

    final_summary = format_review_summary(
        summary_body,
        model_name=model_name,
        include_attribution=include_attribution,
        out_of_diff_notes=failed_comments,
    )

    final_payload = {
        "commit_id": commit_id,
        "body": final_summary,
        "comments": tested_valid_comments,
    }

    final_review = github_api_request(
        review_endpoint, token=token, method="POST", data=final_payload
    )
    print(
        f"Draft review #{final_review['id']} created with {len(tested_valid_comments)} inline comments "
        f"and {len(failed_comments)} summary notes.",
        file=sys.stderr,
    )
    return final_review


def main():
    parser = argparse.ArgumentParser(
        description="Post a draft (pending) PR review to GitHub with automated line validation."
    )
    parser.add_argument(
        "--pr",
        required=True,
        help="GitHub PR URL or slug (e.g. https://github.com/owner/repo/pull/123)",
    )
    parser.add_argument(
        "--commit-id",
        default=None,
        help="Target commit SHA (defaults to latest PR HEAD commit)",
    )
    parser.add_argument(
        "--summary",
        default="Code Review Findings:\n\n* Review completed across Correctness, Architecture, and Guidelines.",
        help="Main summary body for the review",
    )
    parser.add_argument(
        "--comments-file",
        help="Path to JSON file containing list of comment objects [{'path', 'line', 'body', 'side'}]",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name or provider to announce in review header (e.g. 'Claude 3.7', 'GPT-4o', 'Gemini 2.5 Pro')",
    )
    parser.add_argument(
        "--no-attribution",
        action="store_true",
        help="Disable the AI disclosure / attribution header banner",
    )
    parser.add_argument(
        "--token",
        help="GitHub Personal Access Token (defaults to GITHUB_TOKEN / GH_TOKEN / gh CLI)",
    )

    args = parser.parse_args()

    token = get_auth_token(args.token)
    owner, repo, pull_number = parse_pr_url(args.pr)

    commit_id = args.commit_id
    if not commit_id:
        commit_id = get_pr_head_commit(owner, repo, pull_number, token)

    comments = []
    if args.comments_file:
        with open(args.comments_file, "r", encoding="utf-8") as f:
            comments = json.load(f)

    review = post_draft_review(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
        commit_id=commit_id,
        summary_body=args.summary,
        comments=comments,
        token=token,
        model_name=args.model,
        include_attribution=not args.no_attribution,
    )

    html_url = review.get("html_url") or f"https://github.com/{owner}/{repo}/pull/{pull_number}/files"
    print("\nSuccessfully created / updated pending draft review!")
    print(f"Review ID: {review.get('id')}")
    print(f"State: {review.get('state', 'PENDING')} (Draft / Pending)")
    print(f"PR Review URL: {html_url}")
    print(
        "\nOpen the PR URL in your browser to view your pending comments, edit them, or submit the review."
    )


if __name__ == "__main__":
    main()
