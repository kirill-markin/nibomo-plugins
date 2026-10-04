# Nibomo for Executor

This standalone Executor app connects to the existing Nibomo MCP service at https://mcp.nibomo.com/mcp. It requires your own Nibomo account and OAuth authorization. No product credentials are included in the source.

## Install and connect

Install a reviewed copy from the existing [public Nibomo listing](https://v2.executor.sh/apps/nibomo/nibomo), then connect and select your own Nibomo account in the app account settings. An installed copy is separate from its public registry listing; publishing an update does not update existing copies.

Empty account selections expose no upstream tools. Each selected account discovers its own tools and can read and write cards, tags, saved decks, and review progress in workspaces that account can access. Tools marked destructive by the MCP server require approval. Other writes follow the upstream tool policies. Authorize only your own account and review requested changes before approving them.

The app uses Executor's native OAuth discovery, credential handling, per-account catalog cache, and cancellation support. Credentials are restricted to `mcp.nibomo.com`. Exhaustive client runtime testing, including connected-account tool calls, has not been performed.

## Update the published app

Use the existing owned app behind `@nibomo/nibomo`. The [app release runbook](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release-current-version.md) owns release authorization and sequencing; [plugin publishing](../docs/publishing.md#release-source-and-durable-packages) defines source evidence and outcome states. A GitHub push does not deploy Executor. Its framework and MCP SDK dependency versions are not a Nibomo release version.

1. Pin the reviewed merged GitHub SHA and require both cloud **Plugin packages** jobs, including **Executor typecheck**, to pass. Inspect the complete `executor/` upload directory; exclude credentials, dependencies, lockfiles, and scratch files. Omitted remote files are deleted by a source commit, so reconcile intentional differences first.
2. Authenticate the official CLI to the owning `@nibomo` organization. Follow the [official deployment instructions](https://github.com/UsefulSoftwareCo/executor/blob/v2/packages/app-templates/executor/skills/app-authoring/deploy.md), passing `--host https://v2.executor.sh` on every app command. Inspect owned apps and read the selected app's working source:

   ```sh
   executor apps list --host https://v2.executor.sh
   executor apps source --app <existing-app-id> --host https://v2.executor.sh
   ```

   Confirm its ownership and published `@nibomo/nibomo` identity. Compare working and deployed source with the reviewed directory and public listing; record the working `revision.commit`. If source, deployment, and listing already match the target, record **no update needed** with evidence. Missing access is a blocker, not permission to create a replacement.
3. From the repository root, save the reviewed complete directory with the expected working revision, then deploy the returned revision:

   ```sh
   executor apps commit --app <existing-app-id> --files ./executor \
     --expected <observed-working-commit> --message "Update Nibomo" \
     --host https://v2.executor.sh
   executor apps deploy --app <existing-app-id> --commit <returned-revision-commit> \
     --host https://v2.executor.sh
   ```

   On a stale expected-commit rejection, reread source and reconcile before retrying. A saved commit alone does not change running code. Read back the deployed revision and deployment ID; failed deployment does not establish an update.
4. Publish that same selected source revision to the existing registry listing. Consult the current CLI help or discovered management-tool signature and the official procedure for supported publication arguments; do not guess flags. Read back the public listing commit and compare it with the deployed commit. Preserve the owned app's account selections; test with a separate installed copy.
5. Verify the [anonymous public listing](https://v2.executor.sh/apps/nibomo/nibomo), source identity, website, and MCP URL. In a separate copy, verify empty selection exposes no upstream tools, OAuth connects the intended account, account selection discovers its tools, and relevant read/write and destructive-approval behavior works. Use the [manual workflow checks](../docs/publishing.md#real-workflow-verification) with synthetic data. Record failures or unexecuted checks explicitly.

Keep the mapping **GitHub SHA + cloud run → Executor source commit → deployment ID/commit → public listing commit → tested installed-copy revision** in the separate release ledger. Registry publication does not update installed copies; users must review and install the new source separately. A first-create flow is appropriate only after independently proving that no existing owned app exists and obtaining explicit authorization.

## Links

- [Nibomo website](https://nibomo.com)
- [Hosted MCP endpoint](https://mcp.nibomo.com/mcp)
- [Connector documentation](https://nibomo.com/docs/mcp-connector/)
- [Privacy policy](https://nibomo.com/privacy/)
- [Reviewed app source](https://github.com/kirill-markin/nibomo-plugins/tree/main/executor)
