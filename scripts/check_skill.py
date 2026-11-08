"""Static checks for the LinktoDM skill. No network, no credentials.

    python3 scripts/check_skill.py

Fails (exit 1) when:
- SKILL.md frontmatter lacks `name` or `description`, or the name doesn't
  match its folder;
- a relative Markdown link points at a missing file;
- a backticked MCP tool name isn't in references/mcp-tools.json;
- a backticked public API path isn't in references/public-api-openapi.json;
- a Python example doesn't compile.

Refresh the two snapshots with scripts/refresh_snapshots.py whenever the
MCP server or public API changes.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "linktodm"
REFS = SKILL / "references"

LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
CODE = re.compile(r"`([^`\n]+)`")
API_PATH = re.compile(r"^(?:GET|POST|PATCH|PUT|DELETE)?\s*(/v1/[A-Za-z0-9_{}/]+)")
TOOL_LIKE = re.compile(r"^[a-z]+(?:_[a-z]+)+$")


def main() -> int:
    problems: list[str] = []
    tools = {tool["name"] for tool in json.loads((REFS / "mcp-tools.json").read_text())}
    spec = json.loads((REFS / "public-api-openapi.json").read_text())
    api_paths = set(spec["paths"])
    # Words that look like tool names but are fields, enums or examples.
    not_tools = _field_names(spec) | {
        "media_id", "channel_id", "automation_id", "flow_automation_id",
        "editor_url", "is_universal", "use_next_post", "use_next_story",
        "is_story", "trigger_type", "trigger_ai_prompt", "keyword_trigger_type",
        "dm_message", "dm_quick_replies", "addition_buttons", "product_links",
        "auto_reply_messages", "dm_variations", "media_selection_type",
        "media_ids", "action_limit", "action_limit_value", "delay_in_seconds",
        "ai_prompt", "is_active", "new_email", "source_handle", "save_to_field_key",
        "include_keywords", "exclude_keywords", "keywords_checks", "error_message",
        "auto_reply_limit", "one_dm_per_user", "one_dm_per_user_window_hours",
        "step_delays", "follow_up_messages", "ask_to_follow", "disable_auto_reply",
        "enable_auto_reply", "one_trigger_per_user", "one_trigger_per_user_window_hours",
        "media_url", "image_url", "url_label", "carousel_item_index", "field_key",
        "tag_names", "pass_email", "pass_phone", "pass_username",
        "pass_instagram_user_id", "response_mappings", "json_path", "is_draft",
        "node_types", "user_fields", "automation_schema", "is_inbox_automation",
        "event_type", "event_name", "field_slug", "tag_name", "target_url",
        "previous_value", "new_value", "occurred_at", "recipient_id",
        "custom_fields", "phone_number", "has_email", "has_phone", "order_by",
        "key_prefix", "api_key", "contact_id", "field_id", "subscription_id",
        "auto_reply_delay_in_seconds", "connection_label", "channels_count",
        "profile_picture_url", "created_at", "updated_at",
        "send_message", "node_schemas",
    }

    skill_md = SKILL / "SKILL.md"
    front = skill_md.read_text().split("---")
    if len(front) < 3:
        problems.append("SKILL.md: missing frontmatter")
    else:
        if f"name: {SKILL.name}" not in front[1]:
            problems.append(f"SKILL.md: frontmatter name must be '{SKILL.name}'")
        if "description:" not in front[1]:
            problems.append("SKILL.md: frontmatter description missing")

    for md in sorted([ROOT / "README.md", *SKILL.rglob("*.md")]):
        rel = md.relative_to(ROOT)
        text = md.read_text()
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (md.parent / target).exists():
                problems.append(f"{rel}: broken link {target}")
        for code in CODE.findall(text):
            path = API_PATH.match(code)
            if path:
                bare = path.group(1).split("?")[0].rstrip("/")
                if not _api_path_known(bare, api_paths):
                    problems.append(f"{rel}: unknown API path {bare}")
                continue
            name = code.split("(")[0].strip()
            if TOOL_LIKE.match(name) and name not in not_tools and name not in tools:
                problems.append(f"{rel}: unknown MCP tool `{name}`")

    for example in sorted(SKILL.rglob("*.py")):
        try:
            compile(example.read_text(), str(example), "exec")
        except SyntaxError as error:
            problems.append(f"{example.relative_to(ROOT)}: {error}")

    for problem in problems:
        print(problem)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def _api_path_known(path: str, api_paths: set[str]) -> bool:
    """Compare with every `{param}` placeholder normalised to `{}`."""

    def normalise(value: str) -> str:
        return re.sub(r"\{[^}]+\}", "{}", value)

    return normalise(path) in {normalise(known) for known in api_paths}


def _field_names(spec: dict) -> set[str]:
    names = set()
    for schema in spec.get("components", {}).get("schemas", {}).values():
        names.update(schema.get("properties", {}))
    return names


if __name__ == "__main__":
    sys.exit(main())
