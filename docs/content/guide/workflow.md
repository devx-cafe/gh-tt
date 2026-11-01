---
title: "The TakT Workflow"
description: "An opinionated, GitHub-centric workflow built around issues, projects and issue branches."
sidebar:
  order: 1
redirectFrom: /
---

## Suitability Filter

This workflow is opinionated and tailored for teams who value a streamlined, GitHub-centric process. If you share our approach, this workflow will suit you well.

👉 **GitHub-Centric:** We use GitHub _repositories_, _issues_, _projects_, and _actions_ as the backbone of our workflow.

👉 **Kanban Approach:** Our kanban board is implemented using GitHub _issues_ and a single _project_ that serves as both our upstream and downstream board.

👉 **Single Long-Lived Branch:** We maintain only one long-lived branch; The trunk (also referred to as `main`). All other branches are short-lived and are intended to be closed as soon as possible.

👉 **Issue-Driven Development:** Every addition — be it development, bug-fixing, or refactoring—starts with a GitHub _issue_. No commits are allowed on `main` unless they are linked to an issue.

👉 **Always shippable trunk:** The trunk (`main`) branch is always _shippable_ and _pristine_. Only commits that pass the _trunk worthy_ quality gate are allowed.

👉 **Pristine trunk*** All commits on all development branches, regardless if they derive from PR branches, headless spec driven AI sessions or internal issue branches are always squeezed into a single commit, which is then pushed as a _ready_ branch (`ready/**`) The CI flow on the _ready_ must test _all_ trunk worthyness and shall mark the result of all gates on the commit itself as commit statuses. Only single-commit branches that can be fast-forwarded are permitted onto `main`.

👉 **Multi-Tier Automated Testing and deploy**

1. The workspace uses a `pre-commit` git hook which runs a _trunk worthyness_ check.
2. Issue branches (`[0-9]-**`) (may) trigger a `wrapup` workflow for internal status checks.
3. _Ready_ branches trigger a `ready` workflow. If all checks pass, the branch is automatically merged to `main`. Any
   `pr` or `ai` branches are never merged to `main`- they are always `delivered` to _ready_ branches like any other development branch.
4. Commits on `main` are deployed to the _stage_ environment and tested.
5. Formally reviewed commits on `main` are labeled as _releases_ or potentially _pre releases_ according to SemVer.
6. Pre-releases - if any - are deployed to _qa_ or _pre-release_ and tested. Passing commits are marked _shippable_.
7. When ready for production, the latest _shippable_ commit is labeled (`<major>.<minor>.<patch>`) and deployed to _production_.<br/>

👉 **Mentorship Over Pull Requests:** Instead of peer-reviews, we use a [`RESPONSIBLES`](responsibles.md) file (similar to GItHub's `CODEOWNERS`). If a commit affects files with assigned responsibles, those individuals are mentioned on the issue to review or assist. This trust-based mentorship model replaces traditional quality gates.

This is what you sign you for with TakT if this is not a desirable workflow, you should probably look for different tooling.

It is implemented as a `gh` CLI extension `devx-cafe/gh-tt` is designed to support this workflow, with three core subcommands: `workon`, `wrapup`, and `deliver`, which manage the entire branching strategy, and the seamless integration to the kanban board.

Additional supporting tools include:

---

## Workon, Wrapup, Deliver

This is the core development cycle. Each increment to `main` follows this process:

### Workon

**Checks out a branch for an issue. If a branch already exists (locally or remotely), it reuses it; otherwise, it creates a new branch. The issue is assigned to you. If a GitHub project is connected, the issue is added to the project and its status is set to `Work in Progress`.**

To work on an existing issue:

```sh
gh tt workon -i 23
```

Typically, you start with an issue in the _To Do_ column of the downstream board. The context is always the current repository. Cross-repo work requires checking out the other repo — simply add more repos to your workspace.

To create and immediately work on a new issue — rather than use existing one:

```sh
gh tt workon -t "Correcting some spelling"
```

Using the `-t|--title` switch over `-i|--issue` just means that the issue will created for you in the process.

All `gh tt` commands support `--verbose` for detailed output and `--help` for usage information:

---

## Wrapup

**Stages all your changes, unless you already stages something manually. It creates a commit with your message and a reference to the issue, and checks the `RESPONSIBLES` file for any additional reviewers. If responsibles are found, it comments on the issue and mentions them. Finally, it pushes the branch to `origin` — which may trigger a `wrapup` workflow.**

```sh
gh tt wrapup -m "Finished a subset of the issue, taking a break"
```

Using wrapup is a very informal action. Plausible reasons to use `wrapup` could be:

- To safely push your current work before a break.
- To celebrate a milestone.
- To notify a _responsible_ when touching unfamiliar files.
- To request help from a colleague.
- To leverage more detailed insights from the `wrapup` workflow.

There are no strict rules on the issue branch — work as you see fit. Use `--verbose` to see detailed operations.

---

## Deliver

**Requires your development branch to be rebased onto `main`. Squashes all commits on your issue branch into a single commit, using the issue title as the commit message header and listing all individual commit messages. Pushes this as a `ready/**` branch, triggering the `ready` workflow. If all checks pass, the branch is fast-forward merged to `main`, and both the issue and ready branches are deleted. The issue is then closed.**

```sh
gh tt deliver
```

If the `ready/**` branch fails checks, simply continue working on the issue branch, use `wrapup` as needed, and rerun `deliver` when ready.

## Semver

**Typically used to create a new annotated tag**

It can bump five different levels.

- major
- minor
- patch
- prerelease
- build

These are all used in full compliancy with SemVer v2.0

```sh
gh tt semver bump --patch
git push origin --tags"
```

If a semver triggering workflow is defined it will run.
