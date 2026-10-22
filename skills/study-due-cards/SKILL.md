---
name: study-due-cards
description: Run a conversational spaced-repetition study session with existing Nibomo cards. Use when the user asks to study, review due cards, or be quizzed from a Nibomo deck or tag; not for creating cards or a quiz from unrelated material.
---

# Study due cards

1. Use the Nibomo connector; if it is disconnected, ask the user to connect it in their host app. Call `list_workspaces`; use the workspace the user named or agreed on, else the one marked `isSelected`. Name it and pass its `workspaceId` on every call.
2. Read the bundled [review reference](../../references/nibomo-review.md), and the [API reference](../../references/nibomo-api.md) when resolving a deck or tag or practising without grading needs a query.
3. Use the requested deck or tags, resolved from workspace data, and honor a requested session length or manual ratings. Ask for the learner's IANA timezone before the first save if it is unknown.
4. Run the reference's loop one card at a time, keeping feedback short enough to hold the study rhythm.
5. Stop when the user asks, the session length is reached, or nothing is due; for an empty queue, follow the reference.
6. End with this session's confirmed reviews and recurring gaps. During a study-only request, do not edit or create cards unless the user asks; offer a targeted follow-up instead.
