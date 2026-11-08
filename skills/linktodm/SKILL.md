---
name: linktodm
description: Build and run Instagram and Facebook DM automations with LinktoDM. Covers comment-to-DM and story automations, multi-step flows, AI agents that like or hide comments, contacts, tags, custom fields, sending DMs, webhooks and account settings, through the LinktoDM MCP server or the LinktoDM public API. Use when the user mentions LinktoDM, or wants to automate Instagram/Facebook DMs, comments, leads or contacts.
metadata:
  version: "0.1.0"
---

# LinktoDM

LinktoDM automates Instagram and Facebook direct messages for creators and
businesses. Every automation and contact belongs to a **channel**: an
Instagram account or Facebook Page the user connected in the LinktoDM
dashboard (https://console.linktodm.com). Channel ids look like `ig-<id>`,
`ig-business-<id>` or `fb-page-<id>`.

This skill teaches the workflow. It does not install tools or grant access:
the agent needs the LinktoDM MCP server connected or a LinktoDM API key. See
[connect.md](references/connect.md).

## Two ways in: pick one per task

| Use | When | Access |
| --- | --- | --- |
| **MCP server** `https://api.linktodm.com/v1/mcp/` | The user wants you to build or manage things for them in this conversation: automations, flows, agents, settings, analytics | User signs in to LinktoDM in the browser (OAuth). Any plan |
| **Public API** `https://api.linktodm.com/api/public/v1/` | The user wants code: a script, website backend, CRM sync or no-code integration that runs without you | `X-API-Key` header. **Pro+ plan** |

Only the MCP server can create or change automations, flows and agents. Only
the public API is meant for code that runs unattended (sending DMs from a
form, syncing contacts, webhooks). Contacts, tags and custom fields exist in
both.

## Route the request

| The user wants | Read |
| --- | --- |
| One DM when someone comments a keyword or replies to a story | [simple-automations.md](references/simple-automations.md) |
| Several steps: conditions, delays, collecting an email, tags, webhooks, DM keyword replies | [flow-automations.md](references/flow-automations.md) |
| Auto-like or auto-hide comments that match a description | [ai-agents.md](references/ai-agents.md) |
| Profile, email, team, API keys, queue, conversation starters, accounts | [account-settings.md](references/account-settings.md) |
| Code that reads/updates contacts, tags, custom fields or sends DMs | [public-api.md](references/public-api.md) |
| React to contact changes in another system (webhooks, Zapier-style) | [webhooks.md](references/webhooks.md) |
| How automations performed, who was captured | MCP `get_top_automations_by_activity`, `get_event_analytics_summary`, `list_contacts` |

Between a simple automation and a flow: one reply is a simple automation;
anything with a branch, a wait or a second step is a flow.

## Rules that always apply

1. **Start with the channel.** MCP: `list_channels`. API:
   `GET /v1/channels`. If there are several and the user did not say which,
   ask.
2. **Drafts first.** MCP-created automations are inactive drafts and agents
   start switched off. Give the user the `editor_url` to review.
3. **Confirm anything that reaches people or removes access**, one item at a
   time, after saying what will happen: publishing, toggling on, rewinding,
   deleting, disconnecting an account, clearing the queue, team or API key
   changes, email changes, and every `send_message` call in code you run.
4. **Never invent** URLs, post ids, webhook endpoints, API keys or contact
   ids. Ask, or look them up.
5. **Meta's 24-hour rule.** A DM can only reach someone who messaged the
   account in the last 24 hours. Automations triggered by a comment or DM are
   inside the window; a DM sent from your own code later may be rejected by
   Instagram/Facebook even though the API accepted it.
6. **Never put API keys in code, prompts or logs.** Read them from an
   environment variable such as `LINKTODM_API_KEY`.

## Not available to agents

Billing, subscriptions, payments and deleting the LinktoDM account: dashboard
only. Creating contacts: contacts appear when someone messages a connected
account. Bulk "DM all my followers": not supported by Instagram/Facebook.

## Known limits

- MCP activity analytics count simple automations; flow activity is not
  included yet.
- You cannot see the user's posts. For a trigger on one specific post, save
  the draft and ask the user to pick the post in the editor.
- Webhook deliveries are signed, but the signing secret is not yet exposed;
  see [webhooks.md](references/webhooks.md).
