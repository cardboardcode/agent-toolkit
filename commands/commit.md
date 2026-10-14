---
name: git-commit
description: Commit and push the current code changes with an emoji-prefixed, signed-off, single-line message, then let the user decide the next step.
---

# Git Commit

Commit the current changes to the current branch with an appropriate message summarising the changes in one line and one line only.

## Rules

1. Never include `Co-Authored` statements.
2. Do it as fast as possible.
3. Add relevant emojis as a prefix to the message (see emoji mapping below). Ensure there are no duplicate emojis when multiple emojis are used.
4. Sign off on the commit using `git commit -s`.
5. Never use `git commit -S` (it requires GPG key setup).
6. Do not stage the commit yet. Show the git commit message to the user and present the following options for the next step:
   - 1. Be more specific about the git message.
   - 2. Be more concise about the git message.
   - 3. Go ahead and push the commit.
   - 4. Do not continue for now.
7. Execute the corresponding action represented by the integer index the user inputs.

Message format: `:emoji_name_1: :emoji_name_2: :emoji_name_n: <git message>`

## Choosing the Right Emojis

- If something is **Added**, include `:heavy_plus_sign:`
- If a **document** is being updated, include `:blue_book:`
- If something is **Removed**, include `:fire:`
- Else, include `:hammer:`
