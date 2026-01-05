# GitHub CLI Authentication in Devcontainers

**Repos using TakT Github CLI extension may need elevated permissions on GitHub (if a `project` node is  defined in `.tt_config.json`)**

## Problem

Both Devcontainers running on your local machine and Codespaces running on GitHub will set you up with a GitHub authentication. But It may not be sufficient for the TakT flow which assumes `project:write` permissions.

GitHub Codespaces automatically injects a `GITHUB_TOKEN` environment variable containing a `ghu_***` (GitHub User) token but with some limited permissions. This token is automatically generated and expires with the CodeSpace, however, it does **not** include `project:write` scope, which may be required by `devx-cafe/gh-tt`.

If that is the case you need to setup a different token with project permissions.

## Token Precedence in gh CLI

GitHub tokens can be stored in different places. The gh CLI uses a specific precedence order to determine which one to use. The first one found is used.

The gh CLI checks for authentication in this order:

1. **`GH_TOKEN`** environment variable (highest priority)
2. **`GITHUB_TOKEN`** environment variable
3. Stored credentials in **`~/.config/gh/hosts.yml`** (lowest priority)

## Solution

Use an OAuth Token (`gho_***`) with `project:write` permissions and make it available as the `GH_TOKEN` environment variable throughout all terminal sessions in your Codespace.

_N.B: This is not be the only solution — but the simplest_

### Step 1: Create a GitHub OAuth Token

If you don't already have a Personal Access Token (gho) with the required permissions, create one:

```bash
# Use GitHub's web-based auth flow to create a token with project access
unset GH_TOKEN  && unset GITHUB_TOKEN && gh auth logout #Clear all existing tokens
gh auth login -h github.com -p https -s project -w -c # stores the token in ~/.config/gh/hosts.yml 
```

This will prompt you for authentication in the browser and create a token with `project:write` scope in addition to the default permissions. You can verify the permissions by running:

```bash
gh auth status
```

The token that is generates is an OAuth token that never expires -if you ever need to revoke it goto the [Applications settings in your GitHub profile](
https://github.com/settings/applications). It will be listed as _GitHub CLI_

### Step 2: Store the Token so containers can read it

Retrieve the token by running:

```bash
# Get the token
gh auth token
```

It will print the token to `STDOUT` (starts with `gho_`)

#### Codespaces

To use the token in Codespaces store it as a **Codespaces secret** named `GH_TOKEN`:

- Go to [Codespace settings in your profile](https://github.com/settings/codespaces)
- Under "Secrets", create a new secret named `GH_TOKEN`
- Paste your token value

#### VS Code

To use the token in Devcontainers hosted in your local Docker, store it as an **environment variable** named `GH_TOKEN`:

- Edit either your `~/.profile` or `~/.zprofile` dependant on what shell you use locally.
- The profile should define the GH_TOKEN variable like this (replace with your token):
  
  ```bash
  export GH_TOKEN=gho_********************  
  ```

<details><summary>Avoid writing you token in plain text - here's how</summary>

**Encode the token with base64 store that, and decode from there.

**Step 1:**

Same as above; login with `gh auth login` and then encode the token and write it to the profile:

```shell
gh auth login -s project -h github.com -p https -w -c
gh auth token | base64 # capture this output and store it
```

**Step 2:**

Then in your `~/.zprofile` or `~/.profile` you go like this instead:

```bash
export _GH_TOKEN=Z2hvX*** # The output you captured from the command above
export GH_TOKEN=$(echo $_GH_TOKEN | base64 --decode)
```

</details>  

## Verification

After restarting your Codespace, verify that `GH_TOKEN` is set and takes precedence:

```bash
echo $GH_TOKEN
gh auth status
```

The output should show:

- `GH_TOKEN` is set to your gho token (starting with `gho_`)
- Authentication with your GitHub account using the `GH_TOKEN`
- Required scopes including `project`, `repo`, `workflow`, `gist`, and `read:org`

Example successful output:

```bash
github.com
  ✓ Logged in to github.com account <your-username> (GH_TOKEN)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_************************************
  - Token scopes: 'gist', 'project', 'read:org', 'repo', 'workflow'
```

## Required settings in your `.devcontainer/devcontainer.json`

```json
    "remoteEnv": {
        "GH_TOKEN": "${localEnv:GH_TOKEN}",
    }
```
