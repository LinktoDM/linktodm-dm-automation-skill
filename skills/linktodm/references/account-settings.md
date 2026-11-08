<!-- MCP server tools. Connect first: see connect.md -->
# Managing a LinktoDM account

Everything here acts on the signed-in user's own account. Billing,
subscriptions, payments and deleting the LinktoDM account are dashboard-only:
point the user to https://console.linktodm.com.

## Profile and sign-in

- Name, country, creator types: `update_profile`.
- Email (two steps, never skip): `start_email_change(new_email)` sends a code
  to the new address. Ask the user for it, then
  `verify_email_change(new_email, code)`. The email changes only then.
- Primary account: `set_primary_account` with an `ig-...` channel id.
- `logout_all_devices` signs the user out of the dashboard everywhere (this agent's
  MCP connection keeps working). Confirm first.

## Team

- `list_team_members` first. Roles: `ADMIN` (full access), `EDITOR`, `VIEWER`.
- `invite_team_member` grants access to the account and emails an invite:
  confirm the email and role with the user. `resend_team_invitation` if it
  was missed.
- `update_team_member` changes name, email or role; `remove_team_member`
  revokes access. Confirm both.

## API keys

- `list_api_keys` shows names and prefixes only.
- `create_api_key(name)` returns the full key **once**. Show it and tell the
  user to store it securely; it can't be shown again.
- `revoke_api_key` breaks every integration using it. Confirm first.

## Custom contact fields

Typed per-contact variables (TEXT, NUMBER, DATE, DATETIME, BOOLEAN, ARRAY)
used as `{{user.<slug>}}` in messages and saved by flows.
`list_contact_fields` before `create_contact_field` to avoid duplicates.
`update_contact_field` renames (the slug stays, so messages keep working).
`delete_contact_field` makes messages using it render empty: confirm.

## Conversation starters (ice breakers)

Up to 4 questions shown when someone opens a new DM with the account.

1. `get_conversation_starter(channel_id)`.
2. `set_conversation_starter` with the full list. Keep each existing `id`.
   Each item: `question` plus `action` `SEND_MESSAGE` (with `answer`),
   `CONNECT_AUTOMATION` (with `automation_id` or `flow_automation_id`), or
   `NOTHING`. Remove one by sending its `id` with an empty `question`.
3. It is pushed to Instagram immediately; `is_active: false` takes them down.

## DM queue and accounts

| Request | Tool | Notes |
| --- | --- | --- |
| Is anything waiting to send? | `get_message_queue` | |
| Pause / resume sending | `set_message_queue_paused` | Pending DMs are kept |
| Change sending speed | `set_message_queue_speed` | 1-10; each step is 6 DMs a minute |
| Drop pending DMs | `clear_message_queue` | They are never sent: confirm |
| Stop every automation on an account | `deactivate_all_automations` | Reversible one by one |
| Remove an account from LinktoDM | `disconnect_channel` with `confirm: "disconnect"` | Automations stop; reconnecting happens in the dashboard. Prefer `deactivate_all_automations` if the user only wants to pause |
