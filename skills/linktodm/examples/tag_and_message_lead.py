"""Find a LinktoDM contact, save their email and plan, tag them, send a DM.

Typical use: your website's signup form knows the person's Instagram
username. This marks them as a lead in LinktoDM and thanks them in the DM
thread they already have open with you.

    export LINKTODM_API_KEY=...       # Settings → API (Pro+)
    python tag_and_message_lead.py ada.lovelace ada@example.com pro

Standard library only. Pass --dry-run to see what would happen without
changing anything.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.linktodm.com/api/public/v1"
PLAN_FIELD_SLUG = "plan"  # must exist: create it once with POST /v1/custom_fields


def call(method: str, path: str, body: dict | None = None, headers: dict | None = None):
    """One API request with the key from the environment. Retries 429/5xx."""
    key = os.environ["LINKTODM_API_KEY"]
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(4):
        request = urllib.request.Request(
            f"{API}{path}",
            data=data,
            method=method,
            headers={
                "X-API-Key": key,
                "Content-Type": "application/json",
                **(headers or {}),
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read() or b"null")
        except urllib.error.HTTPError as error:
            if error.code == 429 or error.code >= 500:
                wait = float(error.headers.get("Retry-After") or 2**attempt)
                time.sleep(wait)
                continue
            raise SystemExit(f"{method} {path} failed: {error.code} {error.read().decode()}")
    raise SystemExit(f"{method} {path} failed after retries")


def find_contact(username: str) -> dict:
    query = urllib.parse.urlencode({"search": username, "limit": 20})
    matches = call("GET", f"/contacts?{query}")["data"]
    exact = [c for c in matches if (c.get("username") or "").lower() == username.lower()]
    if not exact:
        raise SystemExit(
            f"No contact @{username}. Contacts appear once they message or "
            "comment on a connected account; they can't be created via the API.",
        )
    return exact[0]


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry_run = "--dry-run" in sys.argv
    if len(args) != 3:
        raise SystemExit(__doc__)
    username, email, plan = args

    contact = find_contact(username)
    print(f"Found contact {contact['id']} (@{contact['username']})")
    if dry_run:
        print("Dry run: would save email/plan, tag 'lead' and send a DM.")
        return

    call(
        "PATCH",
        f"/contacts/{contact['id']}",
        {"email": email, "fields": {PLAN_FIELD_SLUG: plan}},
    )
    call("POST", f"/contacts/{contact['id']}/tags", {"tag_names": ["lead"]})
    queued = call(
        "POST",
        f"/contacts/{contact['id']}/send_message",
        {"text": f"Thanks for signing up for the {plan} plan! Reply here with any questions."},
        # Same key on a retry = no second DM.
        headers={"Idempotency-Key": f"signup-{contact['id']}-{plan}"},
    )
    print(f"Tagged and saved. DM {queued['status']} (delivered only within Meta's 24h window).")


if __name__ == "__main__":
    main()
