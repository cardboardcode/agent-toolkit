---
name: prclone
description: Clone the head branch of a GitHub PR into a dedicated <REPO>_<PR_NO> folder using a fast, single-branch shallow clone.
---

# PR Branch Clone

Clone the head branch of a GitHub pull request into a dedicated local directory formatted as `<REPO>_<PR_NO>`.

## Rules

1. Parse the owner (`<OWNER>`), repository name (`<REPO>`), and pull request number (`<PR_NO>`) from the URL: `https://github.com/<OWNER>/<REPO>/pull/<PR_NO>`. If the user has not provided a PR link, ask for it before proceeding.
2. Determine the PR's head branch (`<HEAD_BRANCH>`). Preferred method (no auth for public repos):
   `curl -s https://api.github.com/repos/<OWNER>/<REPO>/pulls/<PR_NO>` and extract the head branch ref (e.g. from `.head.ref` or `grep '"head_branch"'`).
   If the API is unavailable, ask the user for the branch name instead of guessing.
3. Compose the clone command EXACTLY in this shape:

       git clone https://github.com/<OWNER>/<REPO> --branch <HEAD_BRANCH> --single-branch --depth 1 <REPO>_<PR_NO>

   - `--single-branch` and `--depth 1` are MANDATORY. They minimize download size and time. Never omit them, never suggest a full clone.
   - The destination directory MUST be formatted as `<REPO>_<PR_NO>` where `<REPO>` is the repository name and `<PR_NO>` is the pull request number.
   - No extra flags (no `--recurse-submodules`, no `-b` aliases, etc.) unless the user explicitly asks.
4. Execute the command to clone the branch into `<REPO>_<PR_NO>` in the current working directory.
5. Report the clone status and destination path upon completion. If the command fails (e.g. directory already exists, authentication or network issue), report the error clearly to the user.
