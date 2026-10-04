# Publishing Nibomo plugins

Use these procedures during an authorized release. The [app release runbook](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/README.md) owns authorization, cross-platform sequence, and completion gates; its [versioning policy](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/versioning.md) owns target selection and source alignment. Editing these docs does not authorize publication or settings changes.

## Shared source and package formats

The repository root is one Nibomo plugin with a single `skills/` directory. Keep identity fields in `plugin.json` and `.claude-plugin/plugin.json` aligned, including name and version in `gemini-extension.json`. All formats and skill dependencies use the existing `https://mcp.nibomo.com/mcp` endpoint. Antigravity metadata is derived during packaging. No second server or provider-specific copy of the skills is needed.

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

## Prepare the selected release

Follow the canonical [versioning policy](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/versioning.md) before preparing artifacts. For a new release, ask the user to select patch, minor, or major, show the resulting versions, and recommend a choice from completed changes. Wait for the answer before bumping, building release artifacts, or publishing unless this session already explicitly supplies the choice or exact target. Resume a prepared or partly published release at its recorded target without another bump.

Merge all app and companion source-version updates through their normal PR and cloud-CI gates before signed release builds, registry publication, provider packages, or metadata publication. Pin each resulting source SHA in the release ledger. Development keeps the last coordinated release version, so an unchanged manifest version does not prove matching source. The app continuously deploys web/backend from `main`; the formal coordinated version and each exact build/deployment SHA are separate identities.

## Release source and durable packages

1. Record the user-selected shared release version and exact companion GitHub SHA on `main` after preparation. Require both `packages` and **Executor typecheck** in **Plugin packages** to pass for that SHA, as well as the PR checks before merge. A successful older run is not evidence for changed source.
2. Download that run's `nibomo-plugin-packages` artifact: `nibomo-<version>-claude.zip`, `nibomo-<version>-openai.zip`, `nibomo-<version>-gemini.zip`, and `nibomo-<version>-antigravity.zip`. Inspect filenames, manifests, shared skills/references, and MCP identity against the selected source; retain run URL and archive SHA-256 digests in the release ledger. Antigravity's minimal manifest has no version field; its filename and source mapping identify the version.
3. Inspect existing companion tags and [GitHub Releases](https://github.com/kirill-markin/nibomo-plugins/releases). Reuse only an exact matching release, or create an immutable tag and Release for this SHA using the existing convention, or `vX.Y.Z` if none exists. Attach all four original CI ZIPs as durable assets. A conflicting tag, source SHA, or asset digest blocks publication; never move the tag or overwrite conflicting assets. Establish and verify the Gemini asset selection below before advertising this release as installable.
4. Record provider outcomes separately. Matching versions in Git do not publish any provider, and a CI artifact is not a public release. Keep dated evidence in the release's separate ledger, not this guide.

For every provider, record the selected source/version, existing listing or submission ID, evidence URL and timestamp, next action, and one precise state: **no update needed** (verified matching live content), **submitted**, **approved** (not yet live), **live** (public installation verified), **pending review/propagation**, **blocked**, or **explicitly excluded** by the user. Never convert an unexecuted check into success.

## Anthropic

1. In the owning Claude organization, open existing submission `d8c1028d-4318-4da5-8514-1ed3e0b9a09e` in the [developer portal](https://claude.ai/directory/manage). Preserve its GitHub integration: `kirill-markin/nibomo-plugins`, root path, tracked `main`, and existing MCP connector pairing.
2. Compare the selected release SHA/version with **Versions**, including validation and security results. Let normal detection run; use **Check for new commits** only if detection or retry is needed. Recheck results after any source change.
3. Inspect the actual Overview auto-publish policy and Settings toggle. Follow the state shown: submit/resubmit or request **Publish** only when required; record any reviewer hold. Passing checks and publish requests do not by themselves establish availability. Do not assume every update requires a reviewer or that every passing version publishes automatically.
4. Verify the plugin's own public listing and a fresh directory installation expose the selected version and skills. Record that evidence separately from authenticated workflow results. The connector listing or a privately imported copy does not prove the public plugin version.

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

Follow [OpenAI's submission and update procedure](https://developers.openai.com/plugins/deploy/submission) using the existing plugin identity and combined MCP/skills listing.

1. Inspect the existing submission, selected package, and active review. If replacing it would cancel pending review, preserve it and wait; cancellation requires explicit direction. Record the current state rather than assuming an earlier pending status still applies.
2. For metadata, assets, or skills changes, upload the complete CI OpenAI ZIP to that plugin when permitted. Preserve all retained components and established identity; download the existing release ZIP if needed to reconcile metadata. Check package version, automated findings, reviewer materials, test cases, and video. Keep private credentials outside GitHub and archives.
3. Submit the corrected draft and track its decision. After approval, open that version and select **Publish plugin**. Approval and submission are not publication.
4. Runtime tool changes use the existing MCP server's scans, including **Rescan** when available; inspect held updates and live tool definitions. They do not require another package ZIP. Verify public availability in both ChatGPT and Codex and the relevant authenticated workflows below; retain evidence of the actual live package and tools.

## Google

| Package | Root manifest | Remote MCP |
|---|---|---|
| Gemini CLI | `gemini-extension.json` | Embedded `mcpServers.nibomo.httpUrl` |
| Antigravity | Generated `plugin.json` with only `name` and `description` | Generated `mcp_config.json` with `mcpServers.nibomo.serverUrl` |

Both ZIPs contain the same shared skills, references, and assets. Gemini uses automatic OAuth discovery; Antigravity supports automatic OAuth for servers with dynamic client registration. Neither package embeds credentials. Antigravity's documented inline schema rejects additional manifest properties, so its archive must not reuse the portable root manifest.

### Install and connect

Use the [README installation commands](../README.md#get-started). For a Gemini archive installation, extract the selected release's `nibomo-<version>-gemini.zip` into a `nibomo` directory and run `gemini extensions install /absolute/path/to/nibomo`. Restart the CLI, inspect `gemini extensions list`, then use `/mcp auth nibomo` and `/mcp list` inside the session.

For Antigravity, inspect `/plugin list` after installing the extracted archive. In Antigravity 2.0, open Agent settings > Customizations and select **Authenticate** beside Nibomo, then follow the browser authorization prompts. A workspace-scoped alternative is to extract the archive into `.agents/plugins/nibomo/` so its `plugin.json` is directly inside that directory. See the [official plugin installation guide](https://antigravity.google/docs/plugins/) for surface-specific behavior.

Record Google client installation, OAuth, and real study-flow results separately. Package checks must not be reported as successful account connection or study verification.

### Public listings

Use the existing [Gemini gallery entry](https://geminicli.com/extensions/?name=kirill-markinnibomo-plugins) and retain topic `gemini-cli-extension`. Its daily crawl may lag; gallery visibility does not prove release installability.

The [official release guide](https://geminicli.com/docs/extensions/releasing/) supports Git branch/tag/commit `--ref` selection and GitHub Release assets. Unpinned Git installations follow branch `HEAD`; release installations check GitHub's Latest release, not the manifest version. Before any development commits reach `main`, even with unchanged manifest versions:

1. Establish the immutable companion release above with matching manifest/tag version. With four ZIP formats attached, avoid ambiguous generic-asset selection: attach byte-identical copies of the CI Gemini ZIP as `darwin.nibomo.zip`, `linux.nibomo.zip`, and `win32.nibomo.zip`, using the documented platform naming. Verify their digests and root `gemini-extension.json`.
2. Only after the tag/assets exist, install the repository URL with `--ref=<verified-release-tag>` in a clean profile. Inspect the selected asset, manifest, and installation metadata (`~/.gemini/extensions/nibomo/.gemini-extension-install.json`). Verify the actual update destination too. Existing Git installs need an explicit move to the verified stable installation channel; adding a Release does not prove they migrated.
3. Confirm OAuth and workflows separately. Advertise only the verified stable command/channel; keep development commits off that channel. Recheck the gallery after propagation.

Antigravity is optional marketplace expansion. If requested, use the existing identity and the official [Marketplace interest form](https://forms.gle/2EX5RFYPoJe1UgxR9) linked by [Marketplace documentation](https://antigravity.google/docs/marketplace?tab=cli). Record actual review/publication status; an interest form or installable archive is not public approval.

<a id="before-the-next-development-version"></a>

## Release closeout and development protections

Apply the [app runbook's](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/README.md) completion gate across every in-scope platform and channel, including tags, GitHub Releases, durable packages, and public evidence. Preserve each release SHA and live or pending provider version in the separate release ledger; pending review remains pending. Keep the selected version after completion, with no next-development bump. Published tags and packages remain immutable.

Before **any development commits** merge onto tracked `main`, regardless of unchanged manifest versions, turn off Anthropic's **Publish new versions automatically** and verify the saved setting. Preserve the current published/pending commit and review; do not change the tracked ref to bypass review. Do not publish detected development source. If the portal cannot preserve the required state, block development merges to tracked `main` and resolve that condition first. These protections apply whenever development proceeds, including while provider review is pending.

Protect Gemini fresh-install and update paths with the [verified stable release channel](#public-listings) before development advances `main`. Existing Git installs must explicitly move to the verified stable channel; do not infer migration from a Release or unchanged version. Keep shared manifest versions aligned with the last coordinated release during development, as the canonical versioning policy directs. OpenAI reviews and Executor publication remain separate from a GitHub merge; preserve pending submissions and use the [Executor update procedure](../executor/README.md#update-the-published-app) for that surface.

## Real workflow verification

Before requesting publication, run these manual checks on each relevant authenticated client in a synthetic workspace during an authorized release; verify the public installation again afterward. Record client, source/version, account connection, observed result, and evidence. Read-only discovery or guide calls do not establish successful creation, editing, or study. Never describe unexecuted flows as passed.

1. Create two tagged cards about WHERE and HAVING from supplied notes. Verify duplicate inspection, question-only fronts, answer-first backs, tags, saved IDs, and readback. Repeat the request and verify duplicate handling.
2. Study one test card with a supplied IANA timezone. Verify an attempt precedes answer reveal, then feedback, the announced rating, one acknowledged review, and the resulting schedule. Use the bundled same-payload retry procedure for uncertain outcomes.
3. Audit the test cards without writes; then explicitly request a scoped edit and verify saved text, media preservation, and tag-filter deck behavior.
4. Check skips, ambiguous answers, audit-only cleanup, and a disconnected session. Verify clarification or stopping without an invented grade, unauthorized edits, or unacknowledged success claims.

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
