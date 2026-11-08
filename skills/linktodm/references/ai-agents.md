<!-- MCP server tools. Connect first: see connect.md -->
# AI agents

An agent judges every new comment on the chosen posts against its
`ai_prompt` and acts on the ones that fit:

- `LIKE` likes the comment as the account.
- `COMMENT_MODERATION` hides it. A hidden comment also gets no automation, DM
  or like.

## Steps

1. `list_channels`, pick the channel. `list_agents` with that `channel_id` to
   see what already runs there.
2. Agree with the user on:
   - **Type**: like or hide.
   - **Prompt**: written like an instruction to a teammate, at most 300
     characters. Say what to act on **and what to skip**: "Like comments that
     ask about price, availability or where to buy. Skip anything critical or
     promotional." / "Hide abusive or harassing comments and ads for other
     accounts. Leave criticism and complaints alone."
   - **Posts**: every post (`media_selection_type: "ALL"`) or specific posts
     (`"SPECIFIC"` with `media_ids`; you can't see post ids, so ask the user
     or use ALL).
   - Optional: a daily cap (`action_limit: "PER_DAY"`,
     `action_limit_value`) and a delay before acting (`delay_in_seconds`, up
     to 86400).
3. `create_agent`. It starts **switched off**. Share what it will do, then
   `toggle_agent` with `is_active: true` only when the user says to start.
4. Changes: `update_agent` with only the changed fields. On/off:
   `toggle_agent`. Removal: `delete_agent` after the user confirms.

## Rules the server enforces

- One all-posts agent per type per account. An agent on specific posts wins
  over the all-posts agent on those posts. If create fails for this reason,
  offer to edit the existing agent instead.
- A LIKE agent on an Instagram-login channel (`ig-...`) needs Facebook linked
  in the dashboard first. If create says so, send the user to the LinktoDM
  dashboard to link Facebook.

## Tips

- A wrong hide silences a real customer and stops their automations. Keep
  moderation prompts specific and suggest starting narrow.
- To check an agent, ask the user to watch a few comments in the first hour
  and adjust the prompt with `update_agent`.
