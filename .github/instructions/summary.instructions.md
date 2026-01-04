---
applyTo: '**'
---
# Annotate summaries to issues

## Default behaviour

If you recieved noting but a reference to this file, the default behaviour is to annotate a summary of the changeset to the issue being worked on.

## Use an itermediate md file

When in agent mode, and you are asked to create issues and comments to issues, please consider that I'm using zsh and unescaped use of backtick are likely to be mistaken as command substitutions. So for that reason prefer to generate the markdown in intermediate `*.md` files in the `./temp` folder and restrain from using the `--body` flag to `gh issue create` and  `gh issue comment`. But favor the `--body-file` flag instead. Name the file the same as the branch we're working on, with a `.md` extension, and store it in the `./temp` folder. Open it in the editor for my review and annotations.

## Read issue number from branch name

When in agent mode and you ask to _annotate a comment on the current changeset to the issue_, extract the issue number directly from the terminal prompt shown in the `@terminal` context. Development branches are formatted as `(ISSUE_NUMBER-branch_name)` in the zsh prompt. For example, the prompt `vscode ➜ /workspaces/gh-tt (321-Update_summary_instructions) $` indicates you're working on issue 321.

Extract the issue number (the integer before the first hyphen in the branch name shown in parentheses). If the full prompt with branch name is not visible in the `@terminal` context, run `git branch --show-current` to get the branch name, then extract the issue number from it. Do not ask for clarification—just get the information you need to proceed.

Let the summary serve as a work log note to future self and current colleagues. It should summarize the changes made in the branch we're working on since we left `main`, equivalent to `git diff main...HEAD --name-status && git diff main...HEAD`.

## Change set summary

Only summarize on the accumulated change set in the branch. Do not dive into - or reference - the individual commits on the branch. The branch will be squashed into one commit before it hits main so no BOM (Bill of Material) is need - just a summary in prose. Make it a high-level overview of what was done (describe the changes), why it was done (the rationale behind our decisions), and any relevant context (maybe external links of general architectural or design decisions). The summary should have the header `## Change log summary` and even if I did ask you to create such a summary earlier on this branch, you should create the full change set summary again (don't just summarize the increment since last).

The purpose of the summary is to help my future self and current team mates to recall and understand the purpose of - and rationale behind - the changes without needing to read through all the code or commit messages.

Workflow for efficient summary creation and posting:

1. Extract issue number directly from branch name with a single command (no need for multiple tool calls)
2. Create the summary file directly without asking for confirmation or explaining each step
3. Post the comment using the `--body-file` flag without excessive explanation
4. Confirm success with just the URL of the posted comment

This streamlined process should minimize back-and-forth exchanges and unnecessary explanation of each step.
