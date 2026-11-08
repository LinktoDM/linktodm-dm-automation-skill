<!-- MCP server tools. Connect first: see connect.md -->
# Build a LinktoDM flow automation

You build flows with the LinktoDM MCP tools. A flow is a graph of nodes and
edges on one channel (an Instagram account or a Facebook Page). The server
holds the authoritative rules and schemas, so read them first.

## Steps

1. **Load the rules.** Call `get_flow_builder_guide` with the node types you
   expect to use, for example
   `node_types: ["USER_COMMENT_TRIGGER", "MESSAGE_GROUP", "BUTTON_TEXT_MESSAGE", "MESSAGE_BUTTON"]`.
   Follow its `guide` and use its `node_schemas` for exact field names and
   enums. Its `user_fields` are the custom contact fields you may reference.
2. **Pick the channel.** Call `list_channels`. If the user has more than one
   channel and did not say which, ask. Facebook Page channels support only
   comment and DM triggers.
3. **Collect what you cannot guess.** Before writing anything, make sure you
   know the trigger (comment, DM, story reply, story mention, share), which
   posts it watches (all, next post, a specific post), the keywords (or "any"),
   the message text, and every URL. Never invent URLs, image URLs or
   webhook endpoints. Ask in one short batch rather than one question at a
   time.
4. **Write the whole graph.**
   - New flow: `create_flow_automation` with `channel_id`, `name`, all
     `nodes` and all `edges`.
   - Existing flow: `list_flow_automations` to find it, `get_flow_automation`
     to load it, edit the returned nodes and edges, then
     `update_flow_automation` with the complete lists. Nodes and edges you
     leave out are deleted. For a rename or status change only, omit `nodes`
     and `edges`.
   - Omit `position` and edge `id`s; the server and editor fill them in.
5. **Fix and retry.** If the result has `error` and `details`, fix exactly
   what the details name and call again. Do not resend the same graph.
6. **Hand over.** Explain the flow in plain words (what fires it, what the
   contact receives, what happens on each branch), then share `editor_url`.

## Going live

`create_flow_automation` always saves an inactive draft that sends nothing.
A live flow sends real DMs to real people, so call `update_flow_automation`
with `publish: true` only when the user clearly asks for the flow to go live
now. Otherwise tell them to review it in the editor and press Publish.
Editing an already-live flow with `update_flow_automation` takes effect
immediately; say so before you do it.

A trigger watching a specific post needs that post's `media_id`, which you
cannot see. Save the flow as a draft with `media_id: null` and tell the user
to pick the post in the editor.

## Rewind and delete

- **Rewind** runs a live flow for everyone who already commented on its
  specific posts. Call `get_flow_rewind_status` to see whether it can be
  rewound and which posts it covers, explain that past commenters will be
  messaged now (it can't be undone), and only on a clear yes call
  `start_flow_automation_rewind`.
- **Delete**: `delete_automation` with `kind: "flow"`, after the user
  confirms. To stop a flow without deleting it, `update_flow_automation` with
  `publish: false`.

## Example: comment "guide" on any post, DM a link

```json
{
  "channel_id": "ig-business-17841400000000000",
  "name": "Guide on comment",
  "nodes": [
    {"id": "root", "type": "TRIGGER_GROUP", "data": {}},
    {"id": "t1", "type": "USER_COMMENT_TRIGGER", "parentId": "root",
     "data": {"is_story": false, "media_selection_type": "ALL",
              "trigger_type": "SPECIFIC_KEYWORDS", "include_keywords": ["guide"]}},
    {"id": "g1", "type": "MESSAGE_GROUP", "data": {}},
    {"id": "m1", "type": "BUTTON_TEXT_MESSAGE", "parentId": "g1",
     "data": {"message": "Hey {{system.username}}! Here's the guide you asked for 👇"}},
    {"id": "b1", "type": "MESSAGE_BUTTON", "parentId": "m1",
     "data": {"label": "Get the guide",
              "action": {"type": "OPEN_WEBSITE", "url": "https://example.com/guide"}}}
  ],
  "edges": [{"source": "root", "target": "g1"}]
}
```

## Example: ask for an email, then thank them and tag them

The follow-up hangs off the COLLECT_USER_INFO node's `SUCCESS` handle, not
off its message group, because the flow waits for the contact's reply there.

```json
{
  "nodes": [
    {"id": "root", "type": "TRIGGER_GROUP", "data": {}},
    {"id": "t1", "type": "USER_SENDS_MESSAGE", "parentId": "root",
     "data": {"trigger_type": "SPECIFIC_KEYWORDS",
              "keywords_checks": [{"type": "CONTAINS", "keywords": ["freebie"]}]}},
    {"id": "g1", "type": "MESSAGE_GROUP", "data": {}},
    {"id": "ask", "type": "COLLECT_USER_INFO", "parentId": "g1",
     "data": {"type": "EMAIL", "message": "What's your email? I'll send it over 🎁",
              "error_message": "That doesn't look like an email, could you try again?"}},
    {"id": "g2", "type": "MESSAGE_GROUP", "data": {}},
    {"id": "thanks", "type": "PLAIN_TEXT_MESSAGE", "parentId": "g2",
     "data": {"message": "Done! Check your inbox 📩"}},
    {"id": "tag", "type": "ACTION",
     "data": {"actions": [{"type": "ADD_CONTACT_TAG", "data": {"tag_names": ["freebie-lead"]}}]}}
  ],
  "edges": [
    {"source": "root", "target": "g1"},
    {"source": "ask", "target": "g2", "sourceHandle": "SUCCESS"},
    {"source": "g2", "target": "tag"}
  ]
}
```

## Example: only followers get the DM

```json
{"id": "c1", "type": "CONDITION",
 "data": {"conditions": [{"type": "IF_USER_FOLLOWED_ME", "source_handle": "SUCCESS",
                          "response_type": "BOOLEAN", "check": "EQUALS", "value": true}]}}
```

Edges: `root → c1`, then `c1 → <message group>` with `"sourceHandle": "SUCCESS"`.
Add a `"sourceHandle": "FAILED"` edge only if the user wants something for
non-followers. Follower conditions are Instagram-only.
