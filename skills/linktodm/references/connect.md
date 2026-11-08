# Connecting an agent to LinktoDM

The skill only teaches; it needs one of these to act.

## MCP server (build and manage from a conversation)

URL: `https://api.linktodm.com/v1/mcp/` (remote, streamable HTTP, OAuth).

The first tool call opens a LinktoDM sign-in page in the browser. Sign in
with the LinktoDM account whose automations you want managed, then approve.
No API key is involved.

| Agent | How to add it |
| --- | --- |
| Claude Code | `claude mcp add --transport http linktodm https://api.linktodm.com/v1/mcp/`, then run `/mcp` to sign in |
| Claude (claude.ai) | Settings → Connectors → Add custom connector → paste the URL |
| ChatGPT | Install LinktoDM from the plugin directory, or add a custom MCP server with the URL and OAuth |
| Other agents | Add a remote / streamable-HTTP MCP server with the URL in the agent's MCP settings; OAuth discovery is automatic |

Setup guide: https://linktodm.com/support-center/integrations/connect-linktodm-mcp

Check the connection with `get_account_info` and `list_channels`.

## Public API (code that runs on its own)

Base URL: `https://api.linktodm.com/api/public/v1`
Interactive docs: `https://api.linktodm.com/api/public/docs`

1. The account must be on the **Pro+** plan; other plans get `403`.
2. Create a key in the dashboard: **Settings → API**. It is shown once.
3. Store it as an environment variable, never in code:

   ```sh
   export LINKTODM_API_KEY="..."
   curl -s https://api.linktodm.com/api/public/v1/me \
     -H "X-API-Key: $LINKTODM_API_KEY"
   ```

Apps acting for other LinktoDM users use OAuth 2.0 instead
(`Authorization: Bearer <token>`, scopes `contacts:read`, `contacts:write`,
`messages:send`, `webhooks:manage`); registering such an app needs LinktoDM
support.

An agent with the MCP server connected can create a key for the user with
`create_api_key`; the full key appears once in that response.
