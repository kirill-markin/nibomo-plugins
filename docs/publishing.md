# Publishing Nibomo plugins

Use these procedures during an authorized release. The [app release runbook](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/README.md) owns authorization, cross-platform sequence, and completion gates; its [versioning policy](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/versioning.md) owns target selection and source alignment. Editing these docs does not authorize publication or settings changes.

## Shared source and package formats

The repository root is one Nibomo plugin with a single `skills/` directory. Keep identity fields in `plugin.json` and `.claude-plugin/plugin.json` aligned, including name and version in `gemini-extension.json`. Keep `server.json.version` aligned with these plugin versions; **Plugin packages** checks this locally within the repository. All formats and skill dependencies use the existing `https://mcp.nibomo.com/mcp` endpoint. Antigravity metadata is derived during packaging. No second server or provider-specific copy of the skills is needed.

| Component | Anthropic | OpenAI |
|---|---|---|
| Manifest | `.claude-plugin/plugin.json` | Root `plugin.json` with Agent Plugins schema 1.0.0 |
| Remote MCP | `.mcp.json`, type `http` | `mcp.json`, type `streamable-http` |
| Skills | `skills/<name>/SKILL.md` | Same files; `agents/openai.yaml` declares the MCP dependency |
| Listing content | Manifest and README | `extensions.com.openai.interface` and assets |
| Directory submission | GitHub repository and optional folder | ZIP upload to the existing plugin |
| Skill updates | Selected release source on tracked branch or tag, checked before publication | New complete ZIP, checked and reviewed |

The GitHub Actions **Plugin packages** workflow validates the Claude manifest with the official CLI, validates the portable manifests against their published schemas, checks shared identity and MCP wiring including Gemini, and produces four ZIPs in its `nibomo-plugin-packages` artifact. It verifies archive contents against the shared source, validates Antigravity's minimal manifest against the inline documented contract, and installs and lists the Gemini package with the official CLI in a temporary profile. Download the artifact from the successful run. CI success proves package structure and Gemini installation, not directory approval, OAuth compatibility, or workflow quality.

The archives include only each platform's manifest and MCP configuration plus shared skills, bundled references, assets, README, and license. Repository maintenance scripts and CI dependencies are excluded. The Claude source submission uses this repository's root and tracked branch `main`.

## MCP Registry

This repository owns the registry manifest, validation, and manual publisher. Follow [Publishing to the MCP Registry](mcp-registry-publishing.md) for namespace credential setup, the companion workflow, and troubleshooting. The [MCP release gate](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/mcp-and-plugins.md#mcp) remains part of the app release runbook; backend source and deployment stay in the app repository. Registry publication and plugin/provider publication are separate release actions.

## Prepare the selected release

Follow the canonical [versioning policy](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/versioning.md) before preparing artifacts. For a new release, ask the user to select patch, minor, or major, show the resulting versions, and recommend a choice from completed changes. Wait for the answer before bumping, building release artifacts, or publishing unless this session already explicitly supplies the choice or exact target. Resume a prepared or partly published release at its recorded target without another bump.

Merge all app and companion source-version updates through their normal PR and cloud-CI gates before signed release builds, registry publication, provider packages, or metadata publication. Pin each resulting source SHA in the release ledger. Development keeps the last coordinated release version, so an unchanged manifest version does not prove matching source. The app continuously deploys web/backend from `main`; the formal coordinated version and each exact build/deployment SHA are separate identities.

## Release source and durable packages

1. Record the user-selected shared release version and exact companion GitHub SHA on `main` after preparation. Require both `packages` and **Executor typecheck** in **Plugin packages** to pass for that SHA, as well as the PR checks before merge. A successful older run is not evidence for changed source.
2. Download that run's `nibomo-plugin-packages` artifact: `nibomo-<version>-claude.zip`, `nibomo-<version>-openai.zip`, `nibomo-<version>-gemini.zip`, and `nibomo-<version>-antigravity.zip`. Inspect filenames, manifests, shared skills/references, and MCP identity against the selected source; retain run URL and archive SHA-256 digests in the release ledger. Antigravity's minimal manifest has no version field; its filename and source mapping identify the version.
3. Inspect existing companion tags and [GitHub Releases](https://github.com/kirill-markin/nibomo-plugins/releases). Reuse only an exact matching release, or create an immutable tag and Release for this SHA using the existing convention, or `vX.Y.Z` if none exists. Attach all four original CI ZIPs as durable assets. A conflicting tag, source SHA, or asset digest blocks publication; never move the tag or overwrite conflicting assets. Establish and verify the Gemini asset selection below before advertising this release as installable.
4. Record provider outcomes separately. Matching versions in Git do not publish any provider, and a CI artifact is not a public release. Keep dated evidence in the release's separate ledger, not this guide.

For every in-scope provider, record the selected source/version, existing listing or submission ID, evidence URL and timestamp, next action, and provider state: **no update needed** (verified matching live content), **submitted**, **approved** (not yet live), **live** (public installation verified), **pending review/propagation**, or **blocked**. Record **operator-complete** separately, under the app runbook's completion policy: required CI/scans and applicable checks passed, immediate source/version/package/install observations were recorded where available, and the existing provider's applicable submission/update/publication request succeeded (or matching live content needs no update). External review, gallery crawling, and propagation can remain pending after operator completion; record the next provider action without keeping operator work open for that wait. Unknown, unavailable, and unexecuted observations are not passed or proof of public availability.

Before submission or publication, fix known release errors, failed required tests, and lint/compiler/toolchain warnings affecting the release. Reuse valid passing evidence when its relevant inputs are unchanged, identifying the tested source and those inputs; do not reuse an older CI run for changed source. Historical evidence gaps on an already-published artifact are follow-up work, not retrospective release blockers, and optional checks do not reopen completed publication. OpenAI's initial launch and optional marketplace expansion are separate scope by default; routine releases do not need repeated exclusions for them.

## Anthropic

1. In the owning Claude organization, open existing submission `d8c1028d-4318-4da5-8514-1ed3e0b9a09e` in the [developer portal](https://claude.ai/directory/manage). Preserve its GitHub integration: `kirill-markin/nibomo-plugins`, root path, tracked `main`, and existing MCP connector pairing.
2. Compare the selected release SHA/version with **Versions**, including validation and security results. Let normal detection run; use **Check for new commits** only if detection or retry is needed. Recheck results after any source change and require applicable validation/security checks to pass before submission or publication.
3. Inspect the actual Overview auto-publish policy and Settings toggle. Follow the state shown: submit/resubmit or request **Publish** only when required; record any reviewer hold. Passing checks and publish requests do not by themselves establish availability. Do not assume every update requires a reviewer or that every passing version publishes automatically.
4. When the selected version is publicly available now, verify the plugin's own listing and a fresh directory installation expose its version and skills. Otherwise record public installation as pending, with the actual provider state and next action. Passing applicable checks and a successful required submission/update/publication request complete operator work under the canonical policy; external review or propagation remains a background state. Record public evidence separately from authenticated workflow results. The connector listing or a privately imported copy does not prove the public plugin version.

Use the [focused workflow checks](#real-workflow-verification), reusing actual passing creation/study/edit evidence when relevant inputs are unchanged. Media and disconnected-session checks are targeted regressions when affected, not mandatory additions to every update.

Follow [Anthropic's update and publication procedure](https://claude.com/docs/plugins/submit) for live controls. Recheck listing/data declarations when changed; do not create another plugin or MCP submission.

| Data question | Prepared answer |
|---|---|
| Personal data | Reads and stores |
| Skills send data outside declared connectors | No |
| Retention | Longer |
| Intended for users under 18 | Yes, subject to Nibomo's minimum age and parental-permission rules |
| Contact | kirill@kirill-markin.com |

The [privacy policy](https://nibomo.com/privacy/) and [terms](https://nibomo.com/terms/) govern the hosted service. Confirm the live portal's exact acknowledgments before accepting them.

## OpenAI

A first public OpenAI release has not been established. Exclude this channel from routine coordinated releases until a separately scoped initial launch is complete; do not repeat MFA, portal review reconciliation, or launch checks during every release. Keep the existing plugin identity and combined MCP/skills listing. For an authorized initial launch, follow [OpenAI's submission and update procedure](https://developers.openai.com/plugins/deploy/submission):

1. Inspect the existing submission, selected package, and active review. If replacing it would cancel pending review, preserve it and record the pending follow-up; cancellation requires explicit direction. Record the current state rather than assuming an earlier pending status still applies.
2. For metadata, assets, or skills changes, upload the complete CI OpenAI ZIP to that plugin when permitted. Preserve all retained components and established identity; download the existing release ZIP if needed to reconcile metadata. Check package version, automated findings, reviewer materials, test cases, and video. Keep private credentials outside GitHub and archives.
3. Submit the corrected draft and record the decision as pending until observed. Successful submission can complete that operator stage under the app runbook; record the follow-up to open the approved version and select **Publish plugin**. Approval and submission are not publication, and initial public launch is not established until it is verified.
4. Runtime tool changes use the existing MCP server's scans, including **Rescan** when available; inspect held updates and live tool definitions. They do not require another package ZIP. Complete applicable scans and focused authenticated workflow checks before submission/publication. At initial launch, verify public availability in both ChatGPT and Codex when available; retain evidence of the actual live package and tools, or record unavailable observations as pending.

## Executor

The [Executor Publish workflow](../.github/workflows/executor-publish.yml) runs on a published GitHub Release and supports manual retries for an existing stable `vX.Y.Z` release. Both paths use the publisher from reviewed `main`, but upload only the selected release's exact Git source. Main retains the last release version during development; a main push never triggers publication. Release tags and ZIPs remain immutable, including `v1.29.0` at `41cd84f6f8b947131dbbca36b6f8a577db1f1993`.

### One-time access setup

1. In hosted Executor [Account settings → Tokens](https://v2.executor.sh/account/tokens), create a dedicated personal access token scoped only to **Nibomo**, following the [official token instructions](https://v2.executor.sh/docs/api-keys). Its user needs current owner/admin access and edit/publish permission for the existing app. Select an appropriate expiry and retain the token in your secret manager; it is displayed once. Nibomo card OAuth credentials are separate.
2. Add it to this repository's Actions secrets as `EXECUTOR_API_TOKEN`. For example, run the interactive command below and paste the token into its hidden prompt. Never put the token in source, command arguments, logs, or release artifacts.

   ```sh
   gh secret set EXECUTOR_API_TOKEN --repo kirill-markin/nibomo-plugins
   ```

The workflow receives a read-only `GITHUB_TOKEN` with `contents: read` and `actions: read`. A missing Executor secret fails before provider access. Rotate or revoke the dedicated token through Account settings, then update the GitHub secret.

### Release and retry

1. Complete [release preparation](#release-source-and-durable-packages) and applicable [real workflow verification](#real-workflow-verification). Require the latest **Plugin packages** main-push run for the exact release SHA to succeed, including `packages` and **Executor typecheck**. The publisher rejects an absent, pending, or failed run. Publish the prepared stable GitHub Release to start the workflow.
2. To retry after fixing access, waiting for CI, or reconciling a diagnosed failure, dispatch from `main` with the existing release tag:

   ```sh
   gh workflow run executor-publish.yml --repo kirill-markin/nibomo-plugins --ref main -f release_tag=v1.31.0
   gh run list --repo kirill-markin/nibomo-plugins --workflow executor-publish.yml --limit 5
   gh run watch <run-id> --repo kirill-markin/nibomo-plugins --exit-status
   ```

3. Retain the Actions summary in the separate release ledger: release/tag SHA, publisher SHA, exact source cloud run, Executor source commit, deployment ID/commit, accepted publication, and immediate anonymous listing/source result. A matching working source, active deployment, and public source produces **no update needed**. Accepted publication after required checks completes operator work; external propagation can remain pending. A mismatched response fails immediately. Record unexecuted installed-copy/runtime checks explicitly.

Publication is serialized for organization `nibomo` and app `app_741c52b8-681c-4e8c-8536-9b278e02d671`, with no cancellation of an in-progress run. GitHub may replace an older pending run with a newer queued one; use manual dispatch when a skipped release must be published. The public `@nibomo/nibomo` listing has one replaceable revision, so retrying a selected release is supported. Review the selected tag carefully: dispatching an older release intentionally republishes its source.

The publisher reads the complete private workspace, deployed source, public source, ownership, permissions, and saved account selections before writing. The reviewed upload set is `LICENSE`, `README.md`, `index.ts`, `package.json`, and `provider.ts`; it uses Git objects, so credentials, dependencies, lockfiles, and scratch files are excluded. Unexpected source paths stop publication before any omission/deletion. A source-set change requires reviewing the publisher's `SOURCE_PATHS` together with the intended release. Different remote working source must match the deployed/public source and a complete reviewed snapshot in main ancestry; otherwise reconcile the drift explicitly before retrying.

The [hosted management API](https://github.com/UsefulSoftwareCo/executor/blob/v2/packages/app-management/src/contracts/api.ts) saves complete files using the observed working commit as `expected`, deploys the returned immutable commit, and publishes that same commit. Deployment and account selections are read back before publication. A stale revision, response mismatch, or transport error terminates the run; inspect the recorded stage and remote state before rerunning. The publisher never creates an app or changes account selections. Follow the [official deployment model](https://v2.executor.sh/docs/concepts/apps-and-deployments) for manual diagnosis. Existing installed copies do not auto-update; users must review and install the new source separately.

## Google

| Package | Root manifest | Remote MCP |
|---|---|---|
| Gemini CLI | `gemini-extension.json` | Embedded `mcpServers.nibomo.httpUrl` |
| Antigravity | Generated `plugin.json` with only `name` and `description` | Generated `mcp_config.json` with `mcpServers.nibomo.serverUrl` |

Both ZIPs contain the same shared skills, references, and assets. Gemini uses automatic OAuth discovery; Antigravity supports automatic OAuth for servers with dynamic client registration. Neither package embeds credentials. Antigravity's documented inline schema rejects additional manifest properties, so its archive must not reuse the portable root manifest.

### Install and connect

Use the [README installation commands](../README.md#get-started). For a Gemini archive installation, extract the selected release's `nibomo-<version>-gemini.zip` into a `nibomo` directory and run `gemini extensions install /absolute/path/to/nibomo`. Restart the CLI, inspect `gemini extensions list`, then use `/mcp auth nibomo` and `/mcp list` inside the session.

For Antigravity, inspect `/plugin list` after installing the extracted archive. In Antigravity 2.0, open Agent settings > Customizations and select **Authenticate** beside Nibomo, then follow the browser authorization prompts. A workspace-scoped alternative is to extract the archive into `.agents/plugins/nibomo/` so its `plugin.json` is directly inside that directory. See the [official plugin installation guide](https://antigravity.google/docs/plugins/) for surface-specific behavior.

Record Google client installation, OAuth, and real study-flow results separately. Package checks must not be reported as successful account connection or study verification. Reuse passing shared runtime evidence when relevant provider configuration and runtime inputs are unchanged; run focused authentication/workflow checks for changed auth, tool, or skill inputs or a diagnosed failure, using the scope below.

### Public listings

Use the existing [Gemini gallery entry](https://geminicli.com/extensions/?name=kirill-markinnibomo-plugins) and retain topic `gemini-cli-extension`. Its daily crawl may lag; gallery visibility does not prove release installability.

The [official release guide](https://geminicli.com/docs/extensions/releasing/) supports Git branch/tag/commit `--ref` selection and GitHub Release assets. The installed metadata determines the update channel. For `type: github-release`, an unpinned install checks GitHub's Latest release; a `--ref=<verified-release-tag>` install checks that exact tag and will not advance to a later release. This distinction is enforced by the [Gemini updater](https://github.com/google-gemini/gemini-cli/blob/v0.62.0/packages/cli/src/config/extensions/github.ts). Git installations instead follow their selected ref, or `HEAD` without one; local installations compare the source directory's manifest version. Before any development commits reach `main`, even with unchanged manifest versions:

1. Establish the immutable companion release above with matching manifest/tag version. With four ZIP formats attached, avoid ambiguous generic-asset selection: attach byte-identical copies of the CI Gemini ZIP as `darwin.nibomo.zip`, `linux.nibomo.zip`, and `win32.nibomo.zip`, using the documented platform naming. Verify their digests and root `gemini-extension.json`.
2. Only after the tag/assets exist and GitHub Latest points to the selected release, verify both README command variants in separate clean profiles: unpinned for future release updates and `--ref=<verified-release-tag>` for a fixed release. Inspect the selected asset, manifest, and installation metadata (`~/.gemini/extensions/nibomo/.gemini-extension-install.json`, under the selected profile home). Require `type: github-release`, the repository `source`, and the expected `releaseTag`; require no `ref` for Latest or the exact tag in `ref` for the pinned channel. Run `gemini extensions update nibomo` and verify its destination and resulting metadata/payload; an already-current result is not proof of a future-version upgrade.
3. Explicitly migrate existing Git/local installations, or pinned installations that should follow Latest: preserve any local customizations/settings, run `gemini extensions uninstall nibomo`, then reinstall with the chosen [README command](../README.md#get-started) and repeat the metadata checks. Adding a Release or running update alone does not establish migration. If the install resolves to Git/local source, stop and diagnose before treating it as a release channel.
4. Record OAuth and workflow evidence separately under the [focused verification policy](#real-workflow-verification). Advertise only the verified stable command/channel; keep development commits off that channel. Record gallery crawling/visibility separately from installer availability; any later gallery recheck is follow-up, not an operator-completion gate.

Antigravity is optional marketplace expansion. If requested, use the existing identity and the official [Marketplace interest form](https://forms.gle/2EX5RFYPoJe1UgxR9) linked by [Marketplace documentation](https://antigravity.google/docs/marketplace?tab=cli). Record actual review/publication status; an interest form or installable archive is not public approval.

<a id="before-the-next-development-version"></a>

## Release closeout and development protections

Apply the [app runbook's](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/README.md) completion policy across every in-scope platform and channel. Complete required CI/scans, applicable checks, tags, GitHub Releases, durable packages, and successful operator submission/update/publication requests. Preserve each release SHA, operator-completion result, immediate public observations, and live or pending provider version in the separate release ledger. External review/crawling/propagation does not hold operator closeout open; pending review remains pending and must not be described as live. Keep the selected version after completion, with no next-development bump. Published tags and packages remain immutable.

Before **any development commits** merge onto tracked `main`, regardless of unchanged manifest versions, turn off Anthropic's **Publish new versions automatically** and verify the saved setting. Preserve the current published/pending commit and review; do not change the tracked ref to bypass review. Do not publish detected development source. If the portal cannot preserve the required state, block development merges to tracked `main` and resolve that condition first. These protections apply whenever development proceeds, including while provider review is pending.

Protect Gemini fresh-install and update paths with the [verified stable release channel](#public-listings) before development advances `main`. Existing Git/local installs must explicitly move to the verified stable channel; do not infer migration from a Release or unchanged version. Keep shared manifest versions aligned with the last coordinated release during development, as the canonical versioning policy directs. OpenAI reviews and Executor publication remain separate from a GitHub merge; preserve pending submissions and use the [Executor update procedure](../executor/README.md#update-the-published-app) for that surface.

## Real workflow verification

Before requesting submission or publication, select the affected checks below from changed auth, tool, skill, runtime, or provider-configuration inputs and diagnosed failures. Run them in a synthetic workspace on the relevant authenticated client; an exhaustive provider/client matrix is not required. Reuse actual passing creation/study/edit and shared runtime evidence when the relevant inputs are unchanged, recording its source/version, client, account connection, evidence, and applicability. If no applicable passing evidence exists for a required affected flow, execute it before publication. Read-only discovery or guide calls do not establish successful creation, editing, or study. Never describe unexecuted flows as passed.

Record immediate public installation observations when the version is available; external availability waits remain pending after operator closeout. The stable Gemini asset/install/update checks above remain required independently of workflow-evidence reuse.

1. Create two tagged cards about WHERE and HAVING from supplied notes. Verify duplicate inspection, question-only fronts, answer-first backs, tags, saved IDs, and readback. Repeat the request and verify duplicate handling.
2. Study one test card with a supplied IANA timezone. Verify an attempt precedes answer reveal, then feedback, the announced rating, one acknowledged review, and the resulting schedule. Use the bundled same-payload retry procedure for uncertain outcomes.
3. Audit the test cards without writes; then explicitly request a scoped edit and verify saved text and tag-filter deck behavior. Include media preservation when the change affects media.
4. For affected behavior or a diagnosed failure, use targeted regression checks for skips, ambiguous answers, audit-only cleanup, media, or a disconnected session. Verify clarification or stopping without an invented grade, unauthorized edits, or unacknowledged success claims. These extra scenarios are optional when unrelated to the release.

## Official specifications

- [Anthropic plugin structure](https://claude.com/docs/plugins/build)
- [Anthropic pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist)
- [Anthropic source submission and updates](https://claude.com/docs/plugins/submit)
- [Anthropic connector and plugin pairing](https://claude.com/docs/directory/publish)
- [OpenAI portable plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI skills and MCP dependencies](https://developers.openai.com/plugins/build/skills)
- [OpenAI submission, review, and updates](https://developers.openai.com/plugins/deploy/submission)
- [OpenAI adaptation of Claude plugins](https://developers.openai.com/plugins/guides/submit-claude-plugin)
- [Gemini extension format](https://geminicli.com/docs/extensions/reference/)
- [Gemini MCP and OAuth](https://geminicli.com/docs/tools/mcp-server/)
- [Antigravity MCP and OAuth](https://antigravity.google/docs/mcp)
