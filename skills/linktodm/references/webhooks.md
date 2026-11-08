# Webhooks: react to contact changes

LinktoDM POSTs an event to your HTTPS endpoint when something happens to a
contact. Requires a public API key (Pro+). This is how Zapier's LinktoDM
triggers work.

## Event types

| `event_type` | Fires when | Optional filter |
| --- | --- | --- |
| `contact.created` | A new person messages or comments for the first time | |
| `contact.email_set` | A contact's email is saved (e.g. a flow collected it) | |
| `contact.phone_set` | A contact's phone number is saved | |
| `contact.tag_added` | A tag is added | `tag_name` |
| `contact.tag_removed` | A tag is removed | `tag_name` |
| `contact.field_set` | A custom field value is saved | `field_slug` |
| `flow.custom` | A flow runs a "Send to Zapier" action | `event_name` (the name set on that action) |

`flow.custom` lets any flow step notify your system: add a Send to Zapier
action in the flow with an event name, then subscribe to that name.

## Subscribe

```sh
curl -s -X POST https://api.linktodm.com/api/public/v1/webhooks \
  -H "X-API-Key: $LINKTODM_API_KEY" -H "Content-Type: application/json" \
  -d '{"event_type": "contact.tag_added", "tag_name": "lead",
       "target_url": "https://example.com/hooks/linktodm"}'
```

`target_url` must be public HTTPS (no localhost or private addresses).
List with `GET /v1/webhooks`, remove with `DELETE /v1/webhooks/{id}`.

## Payload

The body is the same shape `GET /v1/events` returns. Events are only
recorded while a subscription for that event type exists: changes made before
you subscribe are never delivered, and `GET /v1/events` stays empty until
then. To get sample data, subscribe first, then trigger the event (e.g. tag a
test contact) and read `GET /v1/events`.

```json
{
  "id": "98213",
  "event": "contact.tag_added",
  "occurred_at": "2026-11-07T10:15:00Z",
  "changed": {"tag_name": "lead", "field_slug": null,
              "previous_value": null, "new_value": null},
  "event_name": null,
  "data": {},
  "contact": {"id": 4821, "username": "ada.lovelace", "email": "ada@example.com", "...": "..."}
}
```

`contact` is the full contact object as `GET /v1/contacts/{id}` returns it,
frozen at the time of the event.

Headers: `X-LinktoDM-Event` (the event type), `X-LinktoDM-Delivery` (unique
per delivery), `X-LinktoDM-Signature` (`t=<unix time>,v1=<hex HMAC-SHA256 of
"<t>.<body>">`).

## Receiving reliably

- Answer `2xx` within 15 seconds; do slow work after responding.
- Deliveries are retried on failure and can arrive more than once:
  de-duplicate on the payload `id`.
- Repeated failures switch the subscription off (`410 Gone` does so at once,
  as does a run of `404`s). Re-create it after fixing the endpoint.
- **Signature:** deliveries are signed per subscription, but the API does not
  yet return the signing secret, so you cannot verify it today. Until it
  does, use an unguessable `target_url` (include a long random path segment)
  and treat the payload as untrusted input.

Example receiver: [examples/webhook_receiver.py](../examples/webhook_receiver.py).
