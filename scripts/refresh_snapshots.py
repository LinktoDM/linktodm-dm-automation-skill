"""Regenerate the MCP tool list and public API spec the skill ships with.

Run from a LinktoDM backend checkout (its Python environment active), passing
this repo's path:

    cd /path/to/backend
    python /path/to/linktodm-skill/scripts/refresh_snapshots.py /path/to/linktodm-skill

Then run scripts/check_skill.py: it flags docs that mention tools or
endpoints that no longer exist.
"""

import asyncio
import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    refs = Path(sys.argv[1]) / "skills" / "linktodm" / "references"
    sys.path.insert(0, str(Path.cwd()))

    from app.api.public.app import public_app
    from app.api.v1.mcp.server import mcp

    (refs / "public-api-openapi.json").write_text(
        json.dumps(public_app.openapi(), indent=1) + "\n",
    )
    tools = asyncio.run(mcp.list_tools())
    (refs / "mcp-tools.json").write_text(
        json.dumps(
            [
                {
                    "name": tool.name,
                    "readOnly": tool.annotations.readOnlyHint,
                    "destructive": tool.annotations.destructiveHint,
                }
                for tool in tools
            ],
            indent=1,
        )
        + "\n",
    )
    print(f"Wrote {len(tools)} tools and the public API spec to {refs}")


if __name__ == "__main__":
    main()
