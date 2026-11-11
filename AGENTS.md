# Claude directory source

- Keep the existing Claude directory listing pointed at the repository root on `main`. The portal scans every tracked file there.
- Use only Markdown, UTF-8 text, JSON, YAML, PNG, JPEG, GIF, WebP, and ICO. Keep text UTF-8 without shebangs or NUL bytes. Keep programs and package-manager configuration out of the scanned tree, including packaging tools and Executor code, which belong in `kirill-markin/flashcards-open-source-app`.
- Use configuration keys the Claude directory supports and keep `.mcp.json` on the hosted HTTPS endpoint `https://mcp.nibomo.com/mcp`. Omit extra dependency fields from Claude configuration and preserve listing metadata the portal marks no-action.
- In the portal’s Versions / Review record, confirm the exact updated `main` commit clears `LOCAL_CODE_FILE_TYPE` and `LOCAL_CODE_UNKNOWN_KEY`. `claude plugin validate .` covers only part of the directory checks. See the [Anthropic publishing guide](https://github.com/kirill-markin/flashcards-open-source-app/blob/main/docs/plugin-publishing.md#anthropic).
