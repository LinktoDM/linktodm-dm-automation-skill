# LinktoDM Skill: Instagram & Facebook DM Automation for AI Agents

Teaches AI agents (Claude Code, Codex, Cursor, ChatGPT and others that load
Agent Skills) to build and run Instagram and Facebook DM automations with
[LinktoDM](https://linktodm.com): comment-to-DM and story automations,
multi-step flows, AI agents that like or hide comments, contacts, tags,
custom fields, sending DMs, webhooks and account settings.

Start with [SKILL.md](skills/linktodm/SKILL.md). Installing the skill grants
no access by itself: the agent also needs the LinktoDM MCP server connected,
or a LinktoDM API key for code that uses the public API. See
[connect.md](skills/linktodm/references/connect.md).

## Install

With the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add LinktoDM/linktodm-dm-automation-skill --skill linktodm
```

Or copy the whole `skills/linktodm/` folder into your agent's skills
directory (for Claude Code: `~/.claude/skills/linktodm/`). Keep its
`references/` and `examples/` folders with it.

## What's inside

| Path | Contents |
| --- | --- |
| [skills/linktodm/SKILL.md](skills/linktodm/SKILL.md) | When to use the MCP server vs the public API, routing to the right reference, rules that always apply |
| [references/connect.md](skills/linktodm/references/connect.md) | Connecting the MCP server per agent; getting an API key |
| [references/simple-automations.md](skills/linktodm/references/simple-automations.md) | Comment/story-to-DM automations (MCP) |
| [references/flow-automations.md](skills/linktodm/references/flow-automations.md) | Multi-step flows (MCP) |
| [references/ai-agents.md](skills/linktodm/references/ai-agents.md) | Auto-like and comment-moderation agents (MCP) |
| [references/account-settings.md](skills/linktodm/references/account-settings.md) | Profile, email, team, API keys, queue, conversation starters (MCP) |
| [references/public-api.md](skills/linktodm/references/public-api.md) | Public API: auth, limits, endpoints, gotchas |
| [references/webhooks.md](skills/linktodm/references/webhooks.md) | Webhook events, payloads, reliable receiving |
| [references/public-api-openapi.json](skills/linktodm/references/public-api-openapi.json) | Exact public API schema (snapshot) |
| [references/mcp-tools.json](skills/linktodm/references/mcp-tools.json) | MCP tool names and read/destructive hints (snapshot) |
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

[MIT License](LICENSE) · LinktoDM
