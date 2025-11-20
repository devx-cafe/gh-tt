<!-- cspell:ignore Hackity, clickity -->
# Takt: The Lean Workflow Extension for GitHub

**Takt** is a GitHub CLI extension and GitHub workflow collection built for developers committed to **Lean Software Development** principles. I fosters a **Continuous Delivery** workflow with an always pristine and shippable `man`. It utilizes GitHub Issues and Projects to support **Kanban** true principles (as opposed to _misunderstood_ kanban principles). It encourages and supports you to exploit the four-eye-principle _during_ development — as a collaboration strategy — as opposed to stick it on as a rubber stamp peer-review _in the end_. The flow is completely **Pull Request free**. The Takt flow is designed to enable an optimized **one-piece flow** with no friction, no wait states. While you work with the takt flow it automatically builds up a complete audit trail that you can access on the GitHub Issues.

No more task-switching and arbitrary wait-states of traditional Pull Request and Peer-review based workflows; Switch to Takt to get a true quality-centric one-piece-flow.

<!--
| CI/CD Status | GitHub Marketplace | Version | License |
| :---: | :---: | :---: | :---: |
| [](https://www.google.com/search?q=TBD) | [](https://www.google.com/search?q=TBD) | [](https://www.google.com/search?q=TBD) | [](LICENSE.md) |
-->
-----

## 1\. ⚔️ GitHub's _Enfant Terrible_: The Pull Requests[^gh-enfant-terrible]

[^gh-enfant-terrible]: Dive into the the blog post [_GitHub’s Enfant Terrible: Pull Requests_](https://www.lakruzz.com/stories/githubs-enfant-terrible/) and read up on the gory details on _why_ exactly the Takt flow was developed, why it's superior to GitHubs Pull Request that are essentially working against desired core features in Git itself.

GitHub's default Pull Request (PR) workflow, is based on the assumed need for peer-reviews, It's a bit of an Enfant Terrible, we claim that it often behaves like an anti-pattern for efficient, internal team development.

- **Wait States:** PRs introduce deliberate waiting and idle time in the Value Stream, inflating Change Lead Time (a key DORA metric).
- **Task Switching:** Peer Reviews used at quality gates imposes task-switching, increases the cognitive load and disrupts focus.
- **Weak Ownership:** Peer Reviews encourages "rubber-stamping" and team-shared responsibility over explicit code ownership and responsibility. It's allows technical debt to build up.

We believe **Quality is built in at the source** — which is the developer's workspace — not glued on as a manual, self-inflicted gate.

## 2\. ⚙️ The Solution: The Takt Principle

The name **Takt** comes from Lean Manufacturing (specifically, the Toyota Production System) and refers to the available production time divided by customer demand. It represents the required pace — the "rhythm" — to keep the flow moving.

[See the discussions](../../discussions/5) for a full introduction

The `gh tt` extension enforces a disciplined, rhythmic workflow that ensures continuous movement and built-in quality:

- **Single-Piece Flow:** One Issue $\rightarrow$ One Commit $\rightarrow$ Merge to `main`.
- **Pristine History:** `main` is always linear, shippable, and updated only via fast-forward merges.
- **Automation First:** Automated status checks and static analysis replace manual, opinionated peer reviews as the strict quality gate.
- **Responsibility & Ownership:** Changes are validated by the contributor and verified by the automated pipeline before delivery.

## 3\. 🚀 The Three-Command Workflow

**Takt** abstracts complex Git commands and workflow logic into three intuitive, high-velocity commands:

| Command | Action | Goal (Lean Principle) |
| :---: | :--- | :--- |
| `gh tt workon <issue-id>` | Creates or reuses a dedicated, synchronized development branch for an issue. | **Paired Programming & Synchronicity** |
| `gh tt wrapup <message>` | Commits and pushes the current state frequently, triggering early automated status checks. | **Build Quality In & Reduce Batch Size** |
| `gh tt deliver` | Squeezes the branch into a single, atomic commit, runs final verification, and **fast-forwards** it to `main`. | **Single-Minute Exchange of Die (SMED)** |

### Example Flow

```bash
# 1. Start work on issue #42
$ gh tt workon -i 42


# 2. Develop code and make multiple commits throughout the day
$ gh tt wrapup "Implemented the database query."
$ gh tt wrapup "Finished API endpoint, ready for lunch."

# 3. When work is complete, prepare the final artifact
# Takt requires that your are in sync with remote main when you deliver.
# It's up to you wether you prefer merge or rebase

$ git rebase

# 4. Deliver will create a single fast-forward-able commit from your issue branch and push it to your remote
# A workflow will verify it fast-forwarded to main, and clean up the branches.

$ gh tt deliver
```

### 4\. 🔗 Installation

Requires the official GitHub CLI (`gh`) to be installed.

```bash
# 1. Install the extension
gh extension install devx-cafe/gh-tt

# 2. Verify installation
gh tt --help
```

### 5\. 💡 Why `tt`?

The shortname `tt` is an abbreviation that honors both our history and our core philosophy:

1. This is a fork from the original internal tool used in out team **T**ech **T**hat.
2. **T**ak**t**: The first and last letter of the foundational **Lean Principle** driving our velocity.

By maintaining `tt`, we ensure a short, native-feeling CLI experience without compromising the powerful, professional narrative of **Takt**.

-----

## gh-tt

This utility supports an [opinionated flow](docs/workflow.md). If you share our values and like our process, you can easily set this up for your own team.

**Addendum**

- [The opinionated Takt workflow](docs/workflow.md)
- [How we work with _mentorship_ over _pull requests_](docs/responsibles.md)

**More goodies in the discussions**

- [The Discussions on the repo](../../discussions) contains a lot of additional perspective and reflections on how the get the most our of this `gh tt` utility.

## Introduction

In short, `gh-tt` supports a workflow that

1. follows trunk-based development practices (`main` is the only long-lived branch)
2. does **not** rely on Pull Requests, wait states and bureaucracy
3. works with [RESPONSIBLES](docs/responsibles.md) (CODEOWNERS re-implemented for the PR-less team)

`gh tt` implements ideas from DevOps, GitOps and CI/CD, wrapped up into a sweet, highly configurable, workflow. It looks something like this:

1. `gh tt workon -i 101` - start working on issue #101
    - Create a new development branch and switch to it
    - Move the issue to `In Progress` in a GitHub Project
2. Hackity hack clickity clack
3. `git add .`
4. `gh tt wrapup -m "Rewrite everything in Rust"`
    - Create and push a new commit to the development branch, automatically mentioning the issue
    - Parse and notify `RESPONSIBLES`
    - Run CI
5. `gh tt deliver`
    - Squash the development branch into one commit, create and push a new `ready/<dev_branch_name>` branch with that commit
    - Run CI
    - If CI passes, fast-forward merge the ready branch commit to main

Read about it in more detail in [docs/workflow.md](docs/workflow.md).

## Feedback, discussions, contributing

Issues are open on the repo: [`devx-cafe/gh-tt`](../../issues). If you experience errors, misbehavior, or have feature requests, feel free to join the discussion.

For contributing, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Getting started

### Install

This utility is a GitHub Command Line extension.

Dependencies:

- `python3` – any version, but developed and tested on v3.13. No additional Python dependencies ([install Python](https://www.python.org/downloads/))
- `gh` – the GitHub Command Line Interface ([install GitHub CLI](https://github.com/cli/cli#installation))

Once you have both dependencies installed, run:

```sh
gh extension install devx-cafe/gh-tt
```

The extension requires write access to GitHub Projects (scope `project`). If you don't have it, you'll be prompted with instructions.

### Configure required values

Create a `.tt-config.json` in the root of your repository. You can take inspiration from the default configuration file, [classes/tt-config.json](classes/tt-config.json).

> [!IMPORTANT]
> `gh tt` requires a GitHub Project to work with.

The minimal required configuration looks like:

```jsonc
{
    "project": {
        "owner": "your-github-organization",
        "number": 1 # The project number
    }
}
```

### Configure optional values

You might also want to configure which `Status` issues are assigned when executing `workon` (start working on an issue) and `deliver` (finish and push to `main` if CI passes).

The defaults are

```json
{
    "workon": {
        "status": "In Progress"
    },
    "deliver": {
        "status": "Delivery Initiated"
    }
}
```

> [!TIP]
> There's many more configuration options laid out in [`classes/tt-config.json`](classes/tt-config.json).

### Add files to `.gitignore`

Our setup may pollute the workspace with two files you might want to add to `.gitignore`:

```gitignore
.tt_cache
_temp.token
```

- `.tt_cache` is used to optimize execution. If you change project settings in `.tt-config.json`, delete this cache.
- `_temp.token` is related to the optional configuration described below. It's created and used by `gh-login.sh`. You only need to add it to `.gitignore` if you use `gh-login.sh`.

## Syntax

Run `gh tt -h` to see the syntax.

The extension provides four subcommands: `workon`, `wrapup`, and `deliver`, `responsibles` and `semver`. See the [workflow](docs/workflow.md) for details.

> [!TIP]
> Each subcommand supports the `-h, --help` option to display in-detail guidance for the specific subcommand, e.g.
> `gh tt workon -h`

For an overview, run `gh tt -h`

```sh
usage: gh tt [-h] [-v] [--version] {workon,wrapup,deliver,responsibles,semver} ...

A command-line tool to support a consistent team workflow. It supports a number of subcommands which
define the entire process: `workon`, `wrapup`, `deliver`. Use the `-h|--help` switch on each to learn
more. The extension utilizes the GitHub CLI tool `gh` to interact with GitHub and therefore it's
provided as a gh extension. GitHub Projects integration is supported. It enables issues to
automatically propagate through the columns in the (kanban) board. Please consult the README.md file
in 'devx-cafe/gh-tt' for more information on how to enable this feature - and many more neat
tricks.

positional arguments:
  {workon,wrapup,deliver,responsibles,semver}
    workon              Set the issue number context to work on
    wrapup              Commit the status of the current issue branch and push it to the remote
    deliver             Create a collapsed 'ready' branch for the current issue branch and push it to
                        the remote
    responsibles        List the responsibles for the current issue branch
    semver              Reads and sets the current version of the repo in semantic versioning format

options:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose output
  --version             Print version information and exit
```

## Workflow nice-to-haves

Next to `gh-tt`, we also use devcontainers. Here's some neat tricks that will make your life easier.

For inspiration, see [`devcontainer.json`](.devcontainer/devcontainer.json) in this repo.

```json
"initializeCommand": "./.devcontainer/initializeCommand.sh",
"postCreateCommand": "./.devcontainer/postCreateCommand.sh",
```

Both are designed as one-liners and are placed in separate files.

[**`initializeCommand.sh`**](.devcontainer/initializeCommand.sh)

Uses [`gh-login.sh`](.devcontainer/gh-login.sh) to generate a token from your host machine and prepare it for reuse in the container by [`postCreateCommand.sh`](.devcontainer/postCreateCommand.sh). This allows your container to inherit your host's `gh auth` status.

[**`postCreateCommand.sh`**](.devcontainer/postCreateCommand.sh)

Expands the repo's `.git/.gitconfig` with some additional aliases defined in [`.gitconfig`](.gitconfig). Git does not natively support a `.gitconfig` file in the repository root. So we add it:

```shell
git config --local --get include.path | grep -e ../.gitconfig >/dev/null 2>&1 || git config --local --add include.path ../.gitconfig
```

We install the GitHub extension and import some aliases:

```shell
gh extension install devx-cafe/gh-tt
gh alias import .gh_alias.yml --clobber
```

This creates shortcuts so you can run:

```sh
gh workon        # instead of gh tt workon
gh wrapup        # instead of gh tt wrapup
gh deliver       # instead of gh tt deliver
gh responsibles  # instead of gh tt responsibles
gh semver        # instead of gh tt semver
```

Your feedback - or request for help - is always welcome: Use [the Issues](../../issues) or [the Discussions](../../discussions) to communicate.
