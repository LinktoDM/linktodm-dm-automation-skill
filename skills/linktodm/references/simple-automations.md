<!-- MCP server tools. Connect first: see connect.md -->
# Simple automations

## Steps

1. Call `get_simple_automation_guide` once per conversation. Its
   `automation_schema` is the source of truth for field names and limits.
2. `list_channels`, then pick the channel (ask if there are several).
3. Collect in one short batch:
   - **Which posts**: every post (`is_universal: true`), the next post they
     publish (`use_next_post: true`), story replies (`is_story: true`), story
     mentions (`trigger_type: "STORY_MENTION"`), or one specific post (save the
     draft; the user picks it in the editor).
   - **Which comments**: keywords (`EXACT_MATCH`), any comment (`ANY`),
     everything except keywords (`EXCLUDE`), or AI-matched intent
     (`AI_INTENT` + `trigger_ai_prompt`, at most 300 characters).
   - **The DM**: the text, and every link. Never invent URLs.
   - **Public reply** to the comment: yes (2-3 variations) or no.
4. `create_simple_automation` with `channel_id` and the fields. It is always an
   inactive draft. Share `editor_url`.
5. To change it: `get_simple_automation`, then `update_simple_automation`
   with only the fields that change.

## Choosing the DM type

| Content | `type` | Fields |
| --- | --- | --- |
| Text only (links allowed inline) | `Auto DM Link` | `dm_message`, optional `dm_quick_replies` |
| Text with up to 3 link buttons | `Button Text` | `dm_message`, `addition_buttons: [{url, url_label}]` |
| Product or link cards | `Auto DM Products` | `product_links: [{url, title, image_url, url_label}]`, no `dm_message` |

Attachments (files, images) are dashboard-only. Personalise with
`{{username}}`.

## Going live

Only when the user explicitly asks: `update_simple_automation` with
`publish: true`. It is refused when the automation has no post to watch; fix
that first. Editing an already-live automation takes effect immediately; say
so before saving. To pause one, use `toggle_automation` with
`is_active: false`.

## Rewind

`start_simple_automation_rewind` DMs everyone who already commented on the
automation's post. It needs a live automation on one specific post (not a
story, not "every post"). DMs can't be unsent: tell the user how it works and
get a clear yes first.

## Delete

`delete_automation` with `kind: "simple"`. Confirm first; one at a time.

## Example

"When someone comments PRICE on any post, DM them our pricing page and reply
'Sent you a DM!' publicly":

```json
{
  "channel_id": "ig-business-17841400000000000",
  "automation": {
    "name": "PRICE → pricing DM",
    "type": "Button Text",
    "is_universal": true,
    "keywords": ["price"],
    "dm_message": "Hey {{username}}! Here's our pricing 👇",
    "addition_buttons": [{"url": "https://example.com/pricing", "url_label": "See pricing"}],
    "auto_reply_messages": ["Sent you a DM!", "Check your DMs 📩", "Just DMed you!"]
  }
}
```
