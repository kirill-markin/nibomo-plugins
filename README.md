# Nibomo

Turn notes into clear flashcards, study due cards one question at a time, and improve your collection with Nibomo. This plugin combines three study skills with the existing Nibomo MCP connector. Your cards and confirmed review progress are saved to Nibomo, where you can continue in the web, iOS, or Android app.

## Get started

You need a Nibomo account and a host app that supports plugins and remote MCP connections. Connect Nibomo through OAuth and choose a workspace when asked. The plugin uses `https://mcp.nibomo.com/mcp`, the same URL as the directory-listed Nibomo connector.

For Claude chat, Cowork, and Claude Code, the bundle includes Anthropic's plugin format. For a private preview in Claude, upload the Claude package through Customize > Plugins > Add > Upload plugin and connect Nibomo from its Connectors tab. See Anthropic's [installation and testing guide](https://claude.com/docs/plugins/build).

For ChatGPT and Codex, the bundle includes the portable Agent Plugins format and OpenAI metadata. Public availability requires OpenAI's separate review and publication. See OpenAI's [plugin guide](https://developers.openai.com/plugins/build/plugins). Having this source package does not mean the plugin is published in either directory.

For Gemini CLI, install with `gemini extensions install https://github.com/kirill-markin/nibomo-plugins`, restart the CLI, and run `/mcp auth nibomo` to connect your account through browser OAuth. The extension uses automatic OAuth discovery and includes the same three skills.

For Antigravity, download `nibomo-1.29.0-antigravity.zip` from the successful **Plugin packages** workflow artifact, extract it into a `nibomo` directory, then run `/plugin install /absolute/path/to/nibomo` in Antigravity CLI. Use the Antigravity archive because the repository root `plugin.json` targets the portable format. See [Google installation and publishing details](docs/publishing.md#google).

Google packages can be installed directly; that does not confirm a public gallery or Marketplace listing. Nibomo OAuth and study workflows in Gemini CLI and Antigravity still require end-to-end verification.

The separate [Nibomo app for Executor](https://github.com/kirill-markin/nibomo-plugins/tree/main/executor) connects each installer’s own account to the hosted MCP through OAuth. Its source and publication instructions are maintained separately from these plugin archives.

## Try it

- **Create flashcards:** “Turn these notes into five Nibomo cards. Check for duplicates and use the style of my existing cards.”
- **Study due cards:** “Quiz me on due cards in my SQL deck, one question at a time. My timezone is Europe/Madrid.” The assistant waits for your attempt, reveals the reference, explains its assessment, and saves the review. You can request manual ratings or stop at any time.
- **Improve flashcards:** “Audit my networking cards for ambiguous prompts and duplicates. Show suggested changes before editing.” You can also request tag cleanup and saved deck organization.

The plugin reads live Nibomo guides for current authoring and review rules. It does not provide image generation or an interactive MCP App UI.

## Data and privacy

The declared connector can read and write cards, tags, saved decks, and review progress in workspaces your account can access. Content you explicitly provide for card creation or editing can be stored in Nibomo. The skills do not direct the assistant to transmit study content to another service. The installable packages contain no executable scripts or credentials.

Nibomo's hosted service uses operational telemetry and diagnostic providers. Processing by your external AI client is governed separately by that client's terms and privacy policy. Retention varies by data type; cards and workspace data can remain while the account or shared workspace is active, and some operational logs have no automatic expiry. See the [Nibomo privacy policy](https://nibomo.com/privacy/) for retention, recipients, deletion, and account controls.

The hosted service is for users aged 13 or older, subject to a higher local minimum where applicable. Users under 18 need a parent or legal guardian's permission under Nibomo's policy.

## About Nibomo

Created by Kirill Markin and operated by SAMO DANNI EOOD. The plugin is licensed under MIT.

- [Nibomo](https://nibomo.com)
- [Connector documentation](https://nibomo.com/docs/mcp-connector/)
- [Support](https://nibomo.com/support/)
- [Privacy](https://nibomo.com/privacy/)
- [Terms](https://nibomo.com/terms/)
- [Source and publishing instructions](https://github.com/kirill-markin/nibomo-plugins/tree/main/docs)
