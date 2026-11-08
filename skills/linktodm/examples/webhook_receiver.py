"""Minimal LinktoDM webhook receiver (standard library only).

Subscribe it first (see ../references/webhooks.md), pointing target_url at
a public HTTPS URL that forwards to this server, with a long random path
segment because the signing secret isn't exposed by the API yet:

    LINKTODM_WEBHOOK_PATH=/hooks/linktodm-7f3k9q python webhook_receiver.py

Replies 200 straight away, de-duplicates on the event id (deliveries can
repeat), then handles the event.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

WEBHOOK_PATH = os.environ.get("LINKTODM_WEBHOOK_PATH", "/hooks/linktodm")
seen_event_ids: set[str] = set()  # use your database in production


def handle(event: dict) -> None:
    contact = event.get("contact") or {}
    changed = event.get("changed") or {}
    kind = event.get("event")
    if kind == "contact.email_set":
        print(f"New email for @{contact.get('username')}: {changed.get('new_value')}")
    elif kind == "contact.tag_added":
        print(f"@{contact.get('username')} tagged {changed.get('tag_name')}")
    elif kind == "flow.custom":
        print(f"Flow event {event.get('event_name')} for @{contact.get('username')}")
    else:
        print(f"{kind} for contact {contact.get('id')}")


class Receiver(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != WEBHOOK_PATH:
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length") or 0)
        try:
            event = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        # Acknowledge first: LinktoDM waits at most 15 seconds.
        self.send_response(200)
        self.end_headers()

        event_id = str(event.get("id"))
        if event_id in seen_event_ids:
            return
        seen_event_ids.add(event_id)
        handle(event)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"Listening on :{port}{WEBHOOK_PATH}")
    HTTPServer(("", port), Receiver).serve_forever()
