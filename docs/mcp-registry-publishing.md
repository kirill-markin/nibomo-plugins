# Publishing to the MCP Registry

This repository owns the official MCP Registry manifest
[`server.json`](../server.json), validation, and manual publisher. Backend source
and deployment remain in
[`flashcards-open-source-app`](https://github.com/kirill-markin/flashcards-open-source-app),
so the manifest's `repository.url` points there. Plugin package and provider
publication follow [Publishing Nibomo plugins](publishing.md).

The registry entry publishes under `com.nibomo/flashcards`. For a product
release, follow the [MCP release procedure](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/mcp-and-plugins.md#mcp).
This document covers publisher setup and troubleshooting.

## What is published

`server.json` describes the hosted remote MCP server (a `streamable-http` remote
at `https://mcp.nibomo.com/mcp`). The canonical tool inventory lives in
[connector-directory-submission.md](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/connector-directory-submission.md).

The `name` uses the DNS-based namespace `com.nibomo/...`, which we can verify
because we control `nibomo.com`. The registry verifies the namespace against
`name` only and never compares it with the remote URL.

`mcp.flashcards-open-source-app.com` keeps serving the same server on the same
routes, so client configurations that already point at it keep working. The
published `com.flashcards-open-source-app/flashcards` record keeps advertising
that address rather than the new one, because the registry rejects a publish
whose remote URL already belongs to another record and treats a `deprecated`
record as still holding its URL.

## Prerequisites

- Control of DNS for `nibomo.com` (for namespace verification).
- The Ed25519 namespace private key stored as the `MCP_PRIVATE_KEY` Actions
  secret in `kirill-markin/nibomo-plugins`.
- For one-time credential setup, the core main checkout's root `.env` must
  contain `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ZONE_ID`. Both values must
  resolve to the `nibomo.com` zone while the helper runs. The helper reads and
  writes in the configured zone; `--domain` sets the record name.
- The same Cloudflare values serve other core DNS helpers. Restore their
  `flashcards-open-source-app.com` zone values immediately after setup. Keep
  this canonical `.env` in the core main checkout; do not copy credentials or
  DNS utilities into this repository.

## Validate the manifest

The [MCP Registry Validate workflow](https://github.com/kirill-markin/nibomo-plugins/actions/workflows/mcp-registry-validate.yml)
validates `server.json` against the official MCP Registry schema on pull
requests and pushes to `main` that touch the manifest or registry workflows.
It does not need `MCP_PRIVATE_KEY` and never publishes. The
[Plugin packages workflow](https://github.com/kirill-markin/nibomo-plugins/actions/workflows/packages.yml)
checks that `server.json.version` matches the portable, Claude, and Gemini
plugin versions using only this repository's files. Require both workflows to
pass for changed release inputs before publication.

## One-time credential setup

Use the core-owned
[credential helper](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/scripts/setup/setup-mcp-registry-credential.sh)
from the core main checkout. It generates a fresh Ed25519 keypair, creates the root Cloudflare TXT record for the public key,
stores the private key as this repository's `MCP_PRIVATE_KEY` Actions secret, and then
deletes the temporary local key file.

```sh
bash "$HOME/_my_local/code-local/personal/flashcards-open-source-app/scripts/setup/setup-mcp-registry-credential.sh" \
  --domain nibomo.com \
  --repo kirill-markin/nibomo-plugins
```

Always pass both `--domain nibomo.com` and `--repo kirill-markin/nibomo-plugins`
explicitly; core defaults are not the publisher destination.

Point `CLOUDFLARE_ZONE_ID` and `CLOUDFLARE_API_TOKEN` at the `nibomo.com` zone
before running it, and put the `flashcards-open-source-app.com` values back in
`.env` as soon as it finishes. With the old zone still in `.env`, the script
looks for the `nibomo.com` TXT record in the wrong zone and reports a false
mismatch.

The script is idempotent when both the MCP Registry TXT record and
`MCP_PRIVATE_KEY` already exist. If only one side exists, it fails with an
explicit recovery message instead of silently rotating the namespace key.

If `MCP_PRIVATE_KEY` exists but the TXT record is missing, check the selected
Cloudflare zone, explicit `--domain nibomo.com`, and whether the record was
deleted. Do not remove the existing secret to bypass this error.

## Publish flow

For an authorized release of an unpublished shared version, dispatch
[MCP Registry Publish](https://github.com/kirill-markin/nibomo-plugins/actions/workflows/mcp-registry-publish.yml)
on companion `main`:

```sh
gh workflow run mcp-registry-publish.yml \
  --repo kirill-markin/nibomo-plugins \
  --ref main
```

Follow [the MCP release gate](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/mcp-and-plugins.md#mcp). The workflow
performs validation, duplicate-version checks, authentication, publication, and
verification. Do not run local validation or credential bootstrap for every
release; use the setup sections only when investigating a configuration failure.

## Local manual publish fallback

Use the official `mcp-publisher` CLI only when debugging an authorized publish
outside GitHub Actions. From the companion repo root, confirm cloud validation
passed and the exact version is unpublished, then authenticate with a securely
retained namespace private key supplied as `MCP_PRIVATE_KEY` and publish. GitHub
Actions secrets cannot be read back:

```sh
mcp-publisher login dns --domain nibomo.com --private-key "$MCP_PRIVATE_KEY"
mcp-publisher publish
```

The CLI reads `server.json` from the current directory and submits it.

## Refreshing the entry

Publish the current shared `server.json.version` from `main` during the platform
release stage of [the full release runbook](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/README.md), before
release closeout. For a separate metadata refresh of an already published
version, complete [release preparation](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/release/versioning.md#release-preparation)
with a user-selected new shared version before publishing; registry versions cannot be overwritten. The remote URL only
changes if the hosted MCP domain changes.

## Manual workflow

[MCP Registry Publish](https://github.com/kirill-markin/nibomo-plugins/actions/workflows/mcp-registry-publish.yml)
is manual-only through `workflow_dispatch` and rejects any ref other than
`main`. It validates the manifest, rejects an existing exact registry version,
authenticates with the DNS namespace, publishes, and verifies the exact version
endpoint. See [Publish flow](#publish-flow) for the dispatch command.

### Required GitHub secret

The workflow reads `MCP_PRIVATE_KEY` from `kirill-markin/nibomo-plugins` and
uses `mcp-publisher login dns --domain nibomo.com --private-key` to authenticate.
See [One-time credential setup](#one-time-credential-setup); provision the
namespace key operationally, never in source. A secret in the core repository
does not make it available to this workflow.

## Previous namespace

`com.flashcards-open-source-app/flashcards` is a separate registry record with
its own version history. Changing `name` creates a new record and never moves
the old one, so the old entry is deprecated by hand with a message pointing at
`com.nibomo/flashcards`.

That deprecation authenticates against the old namespace, so it needs an
Ed25519 key for `flashcards-open-source-app.com`, and it needs the opposite
Cloudflare zone from the publish flow above: `CLOUDFLARE_ZONE_ID` and
`CLOUDFLARE_API_TOKEN` in `.env` must point at the
`flashcards-open-source-app.com` zone in the core main checkout while this
runs, which is also their normal resting value.

`MCP_PRIVATE_KEY` now holds the `nibomo.com` key and GitHub secrets cannot be
read back, so generate a fresh key on demand and replace the existing
`v=MCPv1; k=ed25519; p=...` TXT record on the `flashcards-open-source-app.com`
root with the new public key instead of adding a second one. Do not use
`setup-mcp-registry-credential.sh` for this step: it never rotates an existing
key and hard-fails when a domain carries more than one matching TXT record.
Then authenticate with
`mcp-publisher login dns --domain flashcards-open-source-app.com --private-key "$OLD_NAMESPACE_KEY"`
and deprecate the old record.
