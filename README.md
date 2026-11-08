<p align="center">
  <a href="https://linktodm.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="assets/logo-light.svg">
      <img alt="LinktoDM" src="assets/logo-light.svg" width="320">
    </picture>
  </a>
</p>

<h1 align="center">LinktoDM Skill: Instagram & Facebook DM Automation for AI Agents</h1>

<p align="center">
  Teach Claude Code, Codex, Cursor, ChatGPT and any agent that loads Agent Skills<br>
  to build and run Instagram and Facebook DM automations with <a href="https://linktodm.com">LinktoDM</a>.
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-0b57d0?style=flat-square"></a>
  <a href="skills/linktodm/SKILL.md"><img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-linktodm-14b8a6?style=flat-square"></a>
  <a href="skills/linktodm/references/connect.md"><img alt="MCP server" src="https://img.shields.io/badge/MCP-supported-0b57d0?style=flat-square"></a>
  <img alt="Instagram and Facebook" src="https://img.shields.io/badge/Instagram%20%C2%B7%20Facebook-DMs-14b8a6?style=flat-square">
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#what-your-agent-can-do">Capabilities</a> ·
  <a href="#try-asking">Examples</a> ·
  <a href="#whats-inside">What's inside</a> ·
  <a href="https://linktodm.com">linktodm.com</a>
</p>

---

## Install

With the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add LinktoDM/linktodm-dm-automation-skill --skill linktodm
```

Or copy the whole `skills/linktodm/` folder into your agent's skills
directory (for Claude Code: `~/.claude/skills/linktodm/`). Keep its
`references/` and `examples/` folders with it.

> [!IMPORTANT]
> Installing the skill grants no access by itself. Your agent also needs the
> **LinktoDM MCP server** connected, or a **LinktoDM API key** for code that
> uses the public API. See [connect.md](skills/linktodm/references/connect.md).

For Claude Code, connecting the MCP server is one command, then run `/mcp`
to sign in:

```sh
claude mcp add --transport http linktodm https://api.linktodm.com/v1/mcp/
```

## What your agent can do

| | |
| --- | --- |
| 💬 **Comment & story to DM** | Reply to comments and story replies with an automatic DM |
| 🔀 **Multi-step flows** | Build branching conversations that collect info and qualify leads |
| 🤖 **AI agents** | Auto-like comments and hide abusive or harassing ones |
| 👥 **Contacts & tags** | Find, tag and segment leads; manage custom fields |
| ✉️ **Send DMs** | Message contacts from scripts, forms or a CRM via the public API |
| 🔔 **Webhooks** | Receive events reliably in your own backend |
| ⚙️ **Account settings** | Profile, team, API keys, queue speed, conversation starters |

## Two ways in

| | MCP server | Public API |
| --- | --- | --- |
| **Use it when** | You want the agent to build or manage things for you, in the conversation | You want code that runs on its own: a backend, CRM sync or no-code integration |
| **Endpoint** | `https://api.linktodm.com/v1/mcp/` | `https://api.linktodm.com/api/public/v1/` |
| **Access** | Sign in to LinktoDM in the browser (OAuth). Any plan | `X-API-Key` header. Pro+ plan |

Only the MCP server can create or change automations, flows and agents. The
skill teaches the agent which one to pick for each task.

## Try asking

Once the skill and MCP server are connected:

- *"When someone comments **GUIDE** on my latest reel, DM them the download link."*
- *"Build a flow that asks new followers for their email and tags them as leads."*
- *"Turn on an agent that hides abusive comments on my Instagram posts."*
- *"Write a webhook receiver that adds every new LinktoDM contact to my CRM."*

## What's inside

```text
skills/linktodm/
├── SKILL.md          # start here: MCP vs API, routing, rules that always apply
├── references/       # one guide per area, plus API and MCP snapshots
└── examples/         # curl for every endpoint, lead tagging, webhook receiver
```

| Path | Contents |
| --- | --- |
| [SKILL.md](skills/linktodm/SKILL.md) | When to use the MCP server vs the public API, routing to the right reference, rules that always apply |
| [connect.md](skills/linktodm/references/connect.md) | Connecting the MCP server per agent; getting an API key |
| [simple-automations.md](skills/linktodm/references/simple-automations.md) | Comment/story-to-DM automations (MCP) |
| [flow-automations.md](skills/linktodm/references/flow-automations.md) | Multi-step flows (MCP) |
| [ai-agents.md](skills/linktodm/references/ai-agents.md) | Auto-like and comment-moderation agents (MCP) |
| [account-settings.md](skills/linktodm/references/account-settings.md) | Profile, email, team, API keys, queue, conversation starters (MCP) |
| [public-api.md](skills/linktodm/references/public-api.md) | Public API: auth, limits, endpoints, gotchas |
| [webhooks.md](skills/linktodm/references/webhooks.md) | Webhook events, payloads, reliable receiving |
| [public-api-openapi.json](skills/linktodm/references/public-api-openapi.json) | Exact public API schema (snapshot) |
| [mcp-tools.json](skills/linktodm/references/mcp-tools.json) | MCP tool names and read/destructive hints (snapshot) |
| [examples/](skills/linktodm/examples/curl.md) | curl for every endpoint, a lead-tagging script, a webhook receiver |

The detailed rules for building automations live on the MCP server itself
(`get_flow_builder_guide`, `get_simple_automation_guide`), so the skill
teaches workflow and judgment and stays correct when those rules change.

## Checks

Python 3.10+, no dependencies, no network or credentials:

```sh
python3 scripts/check_skill.py
```

It verifies frontmatter, links, that every MCP tool and API path the docs
mention exists in the snapshots, and that the Python examples compile.
Maintainers refresh the snapshots with `scripts/refresh_snapshots.py` when
the MCP server or public API changes.

---

<p align="center">
  <a href="https://linktodm.com">Website</a> ·
  <a href="https://console.linktodm.com">Dashboard</a> ·
  <a href="https://linktodm.com/support-center/integrations/connect-linktodm-mcp">MCP setup guide</a> ·
  <a href="https://api.linktodm.com/api/public/docs">API docs</a>
  <br><br>
  <sub><a href="LICENSE">MIT License</a> · Made by <a href="https://linktodm.com">LinktoDM</a></sub>
</p>
