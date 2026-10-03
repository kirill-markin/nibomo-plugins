# Publishing Nibomo plugins

## Shared source and package formats

The repository root is one Nibomo plugin with a single `skills/` directory. Keep identity fields in `plugin.json` and `.claude-plugin/plugin.json` aligned. Use the existing `https://mcp.nibomo.com/mcp` endpoint in both MCP files and skill dependencies. No second server or provider-specific copy of the skills is needed.

| Component | Anthropic | OpenAI |
|---|---|---|
| Manifest | `.claude-plugin/plugin.json` | Root `plugin.json` with Agent Plugins schema 1.0.0 |
| Remote MCP | `.mcp.json`, type `http` | `mcp.json`, type `streamable-http` |
| Skills | `skills/<name>/SKILL.md` | Same files; `agents/openai.yaml` declares the MCP dependency |
| Listing content | Manifest and README | `extensions.com.openai.interface` and assets |
| Directory submission | GitHub repository and optional folder | ZIP upload to the existing plugin |
| Skill updates | New version on tracked branch or tag, checked before publication | New complete ZIP, checked and reviewed |

The GitHub Actions **Plugin packages** workflow validates the Claude manifest with the official CLI, validates the portable manifests against their published schemas, checks shared identity and MCP wiring, and produces two ZIPs in its `nibomo-plugin-packages` artifact. Download the artifact from the successful run. CI success proves package structure, not directory approval or workflow quality.

The archives include only each platform's manifest and MCP configuration plus shared skills, assets, README, and license. Repository maintenance scripts and CI dependencies are excluded. The Claude source submission uses this repository's root and tracked branch `main`.

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

## Real workflow verification

The initial private Claude package exposed all three skills and one connected Nibomo connector. A fresh chat read the self-contained instructions, and read-only `list_workspaces` and four `get_guide` calls succeeded. The shared skills retain those workflows with host-neutral connection instructions. Full card creation, editing, and review flows still need the following smoke checks in a synthetic workspace before publication; never describe them as passed without running them.

1. Create two tagged cards about WHERE and HAVING from supplied notes. Verify duplicate inspection, question-only fronts, answer-first backs, tags, saved IDs, and readback. Repeat the request and verify duplicate handling.
2. Study one test card with a supplied IANA timezone. Verify an attempt precedes answer reveal, then feedback, the announced rating, one acknowledged review, and the resulting schedule. Use the live guide's same-payload retry procedure for uncertain outcomes.
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
