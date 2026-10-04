# Nibomo for Executor

This standalone Executor app connects to the existing Nibomo MCP service at https://mcp.nibomo.com/mcp. It requires your own Nibomo account and OAuth authorization. No product credentials are included in the source.

## Install and connect

Install a reviewed public copy through Executor when the listing is available, then connect and select your own Nibomo account in the app account settings. An installed copy is separate from its public registry listing; publishing an update does not update existing copies. This repository does not establish that a public listing has been published.

Empty account selections expose no upstream tools. Each selected account discovers its own tools and can read and write cards, tags, saved decks, and review progress in workspaces that account can access. Tools marked destructive by the MCP server require approval. Other writes follow the upstream tool policies. Authorize only your own account and review requested changes before approving them.

The app uses Executor's native OAuth discovery, credential handling, per-account catalog cache, and cancellation support. Credentials are restricted to `mcp.nibomo.com`. Exhaustive client runtime testing, including connected-account tool calls, has not been performed.

## Publish from reviewed source

The `Executor typecheck` GitHub Actions job installs the pinned dependencies without a lockfile and checks both TypeScript files. After independent review, merge the source and wait for all cloud checks to pass. Use the official Executor CLI authenticated to the `@nibomo` organization, passing `--host https://v2.executor.sh` on every app command.

Create a Nibomo app with `executor apps create --name "Nibomo" --files ./executor --host https://v2.executor.sh` from the exact merged repository source. Read back its saved commit, deploy that commit, and publish the same commit as `@nibomo/nibomo` using the current CLI commands. Verify the owned app and anonymous listing show the reviewed source and visible website/MCP URLs. Keep account selections empty during publication; installing and authorizing a user copy is a separate action. Do not include lockfiles, dependencies, scratch files, or credentials in the uploaded directory. See the [official app deployment instructions](https://github.com/UsefulSoftwareCo/executor/blob/v2/packages/app-templates/executor/skills/app-authoring/deploy.md) for the current commit, deploy, and publication workflow.

## Links

- [Nibomo website](https://nibomo.com)
- [Hosted MCP endpoint](https://mcp.nibomo.com/mcp)
- [Connector documentation](https://nibomo.com/docs/mcp-connector/)
- [Privacy policy](https://nibomo.com/privacy/)
- [Reviewed app source](https://github.com/kirill-markin/nibomo-plugins/tree/main/executor)
