# Publishing Nibomo plugins

## Shared source and package formats

The repository root is one Nibomo plugin with a single `skills/` directory. Keep identity fields in `plugin.json` and `.claude-plugin/plugin.json` aligned, including name and version in `gemini-extension.json`. All formats and skill dependencies use the existing `https://mcp.nibomo.com/mcp` endpoint. Antigravity metadata is derived during packaging. No second server or provider-specific copy of the skills is needed.

| Component | Anthropic | OpenAI |
|---|---|---|
| Manifest | `.claude-plugin/plugin.json` | Root `plugin.json` with Agent Plugins schema 1.0.0 |
| Remote MCP | `.mcp.json`, type `http` | `mcp.json`, type `streamable-http` |
| Skills | `skills/<name>/SKILL.md` | Same files; `agents/openai.yaml` declares the MCP dependency |
| Listing content | Manifest and README | `extensions.com.openai.interface` and assets |
| Directory submission | GitHub repository and optional folder | ZIP upload to the existing plugin |
| Skill updates | New version on tracked branch or tag, checked before publication | New complete ZIP, checked and reviewed |

The GitHub Actions **Plugin packages** workflow validates the Claude manifest with the official CLI, validates the portable manifests against their published schemas, checks shared identity and MCP wiring including Gemini, and produces four ZIPs in its `nibomo-plugin-packages` artifact. It verifies archive contents against the shared source, validates Antigravity's minimal manifest against the inline documented contract, and installs and lists the Gemini package with the official CLI in a temporary profile. Download the artifact from the successful run. CI success proves package structure and Gemini installation, not directory approval, OAuth compatibility, or workflow quality.

The archives include only each platform's manifest and MCP configuration plus shared skills, bundled references, assets, README, and license. Repository maintenance scripts and CI dependencies are excluded. The Claude source submission uses this repository's root and tracked branch `main`.

## Anthropic

1. Open [the developer portal](https://claude.ai/directory/manage) in the same Claude organization as the published Nibomo connector.
2. Choose **Plugin bundle**, repository `kirill-markin/nibomo-plugins`, empty plugin path, and branch `main`.
3. Select **Validate** and fix blocking findings in this repository. Revalidate after each push; validation is tied to a commit.
4. Review the listing preview, data answers, and compliance acknowledgments with the owner. Keep automatic publication off for the first version and use scheduled checks unless push webhooks are explicitly wanted.
5. Submit for review after owner review. Creating the repository or passing validation does not publish a directory listing.

The package references the same MCP URL as the published connector, so the companion submission should pair with that connector. Do not submit another MCP server. A GitHub connection needs push access in the same Claude organization; public repository validation can run before that connection is completed.

| Data question | Prepared answer |
|---|---|
| Personal data | Reads and stores |
| Skills send data outside declared connectors | No |
| Retention | Longer |
| Intended for users under 18 | Yes, subject to Nibomo's minimum age and parental-permission rules |
| Contact | kirill@kirill-markin.com |

The [privacy policy](https://nibomo.com/privacy/) and [terms](https://nibomo.com/terms/) govern the hosted service. Confirm the live portal's exact acknowledgments before accepting them.

## OpenAI

MCP access and skills belong in one plugin submission; prior MCP approval is not a prerequisite for submitting the combined package. For Nibomo, keep the already pending submission in place. OpenAI permits only one active review per plugin, so replacing a package under review requires waiting for the decision or cancelling the review.

After the decision, download the existing listing's package if needed, preserve its established identity and review metadata, and incorporate these skills into a complete updated ZIP for that same plugin. The source manifest supplies portable packaging and public metadata; it does not replace private reviewer credentials, test evidence, or video required by the dashboard. Keep those out of GitHub.

Do not create a separate OpenAI listing just for skills that use Nibomo. The public directory is shared by ChatGPT and Codex. Test the package in both target products before requesting publication.

## Google

| Package | Root manifest | Remote MCP |
|---|---|---|
| Gemini CLI | `gemini-extension.json` | Embedded `mcpServers.nibomo.httpUrl` |
| Antigravity | Generated `plugin.json` with only `name` and `description` | Generated `mcp_config.json` with `mcpServers.nibomo.serverUrl` |

Both ZIPs contain the same shared skills, references, and assets. Gemini uses automatic OAuth discovery; Antigravity supports automatic OAuth for servers with dynamic client registration. Neither package embeds credentials. Antigravity's documented inline schema rejects additional manifest properties, so its archive must not reuse the portable root manifest.

### Install and connect

Use the [README installation commands](../README.md#get-started). For a Gemini archive installation, extract `nibomo-1.29.0-gemini.zip` into a `nibomo` directory and run `gemini extensions install /absolute/path/to/nibomo`. Restart the CLI, inspect `gemini extensions list`, then use `/mcp auth nibomo` and `/mcp list` inside the session.

For Antigravity, inspect `/plugin list` after installing the extracted archive. In Antigravity 2.0, open Agent settings > Customizations and select **Authenticate** beside Nibomo, then follow the browser authorization prompts. A workspace-scoped alternative is to extract the archive into `.agents/plugins/nibomo/` so its `plugin.json` is directly inside that directory. See the [official plugin installation guide](https://antigravity.google/docs/plugins/) for surface-specific behavior.

Google client installation, OAuth, and the real study flows below remain unverified end to end. Package checks must not be reported as successful account connection or study verification.

### Public listings

1. Gemini: merge the root `gemini-extension.json` onto `main` in the public `kirill-markin/nibomo-plugins` repository. In GitHub's repository **About** settings, add topic `gemini-cli-extension`. The [gallery crawler](https://geminicli.com/docs/extensions/releasing/) checks tagged public repositories daily and lists extensions that pass validation; verify the gallery entry afterward. No issue or email submission is required.
2. Antigravity: apply through the official [Marketplace interest form](https://forms.gle/2EX5RFYPoJe1UgxR9), linked by the [Marketplace documentation](https://antigravity.google/docs/marketplace?tab=cli). Use the existing Nibomo identity, repository, website, and MCP endpoint. Interest-form submission and an installable archive do not establish Marketplace acceptance or publication.

## Real workflow verification

The initial private Claude package exposed all three skills and one connected Nibomo connector. A fresh chat read the self-contained instructions, and read-only `list_workspaces` and four `get_guide` calls succeeded. The shared skills use bundled API, authoring, and review references rather than fetching behavioral guidance at runtime. Full card creation, editing, and review flows still need the following smoke checks in a synthetic workspace before publication; never describe them as passed without running them.

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
