# Nibomo for Executor

This standalone Executor app connects to the existing Nibomo MCP service at https://mcp.nibomo.com/mcp. It requires your own Nibomo account and OAuth authorization. No product credentials are included in the source.

## Install and connect

Install a reviewed copy from the existing [public Nibomo listing](https://v2.executor.sh/apps/nibomo/nibomo), then connect and select your own Nibomo account in the app account settings. An installed copy is separate from its public registry listing; publishing an update does not update existing copies.

Empty account selections expose no upstream tools. Each selected account discovers its own tools and can read and write cards, tags, saved decks, and review progress in workspaces that account can access. Tools marked destructive by the MCP server require approval. Other writes follow the upstream tool policies. Authorize only your own account and review requested changes before approving them.

The app uses Executor's native OAuth discovery, credential handling, per-account catalog cache, and cancellation support. Credentials are restricted to `mcp.nibomo.com`. Exhaustive client runtime testing, including connected-account tool calls, has not been performed.

## Update the published app

Use the existing owned app behind `@nibomo/nibomo`. The [app release runbook](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/README.md) owns release authorization, sequencing, and operator completion, including [target selection and unchanged development versions](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/versioning.md); [plugin publishing](../docs/publishing.md#release-source-and-durable-packages) defines source evidence and outcome states. A GitHub push does not deploy Executor. Its framework and MCP SDK dependency versions are not a Nibomo release version.

1. Pin the reviewed merged GitHub SHA and require both cloud **Plugin packages** jobs, including **Executor typecheck**, to pass. Complete applicable [focused workflow checks](../docs/publishing.md#real-workflow-verification) before publication, reusing valid unchanged-input evidence and resolving known failures. Inspect the complete `executor/` upload directory; exclude credentials, dependencies, lockfiles, and scratch files. Omitted remote files are deleted by a source commit, so reconcile intentional differences first.
2. Connect to the MCP for [hosted Executor](https://v2.executor.sh) with access to the owning `@nibomo` organization. Follow the [official MCP deployment instructions](https://github.com/UsefulSoftwareCo/executor/blob/v2/packages/app-templates/executor/skills/app-authoring/deploy.md#deploy-through-mcp). In Executor's `execute`, discover the current management tools:

   ```js
   return await tools.search({ query: "Executor" });
   ```

   Page through results as needed and read the exact callable paths and signatures. Discover and call `context.get({})`; verify its approved organization, slug, and role, and use its returned `organization` explicitly. Discover `appManagement.list`, `appManagement.source`, `apps.source`, and publication reads; confirm the existing app ID, ownership, and published `@nibomo/nibomo` identity. Compare working source, immutable deployed source, and public listing with the reviewed directory; record the working `revision.commit`. If all match the target, record **no update needed** with evidence. If access or a required operation is missing, stop and record the exact missing grant/signature or error. Do not create a replacement or guess CLI flags.
3. Discover `appManagement.commit` and `appManagement.deploy`. Serialize the reviewed complete `executor/` directory as `{ path, content }` entries with paths relative to that directory, retaining the exclusions from step 1. Pass the actual file contents as JSON data; remote `execute` cannot read a local directory. Using the discovered management profile and signatures:

   ```js
   const executor = tools.executor.profiles["<discovered-management-profile-id>"];
   const path = { organization: "<approved-organization-id>", app: "<existing-app-id>" };
   const saved = await executor.appManagement.commit({
     path,
     body: { expected: "<observed-working-commit>", files, message: "Update Nibomo" },
   });
   return await executor.appManagement.deploy({
     path,
     body: { commit: saved.revision.commit },
   });
   ```

   Here `files` is the complete serialized file list, not a local path. On a stale expected-commit rejection, reread working source and reconcile before retrying. Deployment takes the returned commit without `expected` or `expectedDeployment`; a saved commit alone does not change running code. Read back the deployed revision, deployment ID, and active deployment; failed deployment does not establish an update. Start a new `execute` to rediscover tools after deployment.
4. Discover `appManagement.publish` and publish that same source commit to the existing registry listing. The [official management contract](https://github.com/UsefulSoftwareCo/executor/blob/v2/packages/app-management/src/contracts/api.ts) takes the organization/app in `path` and `{ commit }` in `body`; verify the serving signature before calling it. The hosted UI's [Share publicly control](https://github.com/UsefulSoftwareCo/executor/blob/v2/packages/ui/src/implementation/dashboard/publish-app.tsx) is also available; verify its selected source commit before publication. Record the successful publication response and read back the public listing commit when immediately available, comparing it with the deployed commit. Record propagation as pending rather than claiming a matching live commit before observing it; diagnose any unexpected mismatch. Preserve the owned app's account selections; test with a separate installed copy.
5. Inspect the [anonymous public listing](https://v2.executor.sh/apps/nibomo/nibomo), source identity, website, and MCP URL when available immediately. For changed auth/tool/provider inputs or a diagnosed failure, use a separate copy to verify affected empty-selection, OAuth, account discovery, read/write, or destructive-approval behavior with synthetic data under the [focused workflow policy](../docs/publishing.md#real-workflow-verification); reuse applicable passing evidence for unchanged inputs. Record failures or unexecuted checks explicitly. Successful publication after required checks completes operator work under the app runbook; any external propagation or unavailable public observation remains pending, not verified live.

Keep the mapping **GitHub SHA + cloud run → Executor source commit → deployment ID/commit → public listing commit → tested installed-copy revision** in the separate release ledger. Registry publication does not update installed copies; users must review and install the new source separately. A first-create flow is appropriate only after independently proving that no existing owned app exists and obtaining explicit authorization.

## Links

- [Nibomo website](https://nibomo.com)
- [Hosted MCP endpoint](https://mcp.nibomo.com/mcp)
- [Connector documentation](https://nibomo.com/docs/mcp-connector/)
- [Privacy policy](https://nibomo.com/privacy/)
- [Reviewed app source](https://github.com/kirill-markin/nibomo-plugins/tree/main/executor)
