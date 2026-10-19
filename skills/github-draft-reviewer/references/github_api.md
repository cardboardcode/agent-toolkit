# GitHub REST API Reference for Draft Reviews

## How GitHub Pending (Draft) Reviews Work

When you review a PR via GitHub web interface, your comments remain in a Pending state (visible only to you) until you click Submit review.

In the GitHub REST API:
* Endpoint: POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
* To create a Pending / Draft review: Omit the event field in the request body (do not pass APPROVE, REQUEST_CHANGES, or COMMENT).
* When event is omitted, the API creates the review with state: PENDING.
* Comments attached to a pending review are visible exclusively to the authenticated user on GitHub until submitted.

## Authentication and Tokens

The following authentication methods are supported (in order of resolution):
* --token parameter passed to the helper script
* GITHUB_TOKEN environment variable
* GH_TOKEN environment variable
* Active session from GitHub CLI: gh auth token / gh auth status

### Required Token Scopes
* Fine-grained PAT:
  * Pull requests: Read and Write
  * Contents / Repository contents: Read-only
  * Metadata: Read-only
* Classic PAT:
  * repo scope (or public_repo for open-source repositories)

## API Payload Example

```json
{
  "commit_id": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
  "body": "Code Review Summary:\n\n* Summary: ...\n* Key Points for Maintainer: ...",
  "comments": [
    {
      "path": "src/services/auth.ts",
      "line": 45,
      "side": "RIGHT",
      "body": "Bug (Null Safety): user.session may be undefined if token is expired.\n\n```suggestion\nif (!user?.session) {\n  throw new UnauthorizedException();\n}\n```"
    }
  ]
}
```
