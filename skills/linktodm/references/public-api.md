# LinktoDM public API

For code that runs without the agent: scripts, website backends, CRM syncs.
Exact request/response schemas: [public-api-openapi.json](public-api-openapi.json)
(OpenAPI 3; also served live at `https://api.linktodm.com/api/public/openapi.json`).

## Basics

| | |
| --- | --- |
| Base URL | `https://api.linktodm.com/api/public/v1` |
| Auth | `X-API-Key: <key>` (or `Authorization: Bearer <oauth token>`) |
| Plan | Pro+ only; otherwise `403` |
| Rate limit | 120 requests per minute per key; over it you get `429` with `Retry-After` (seconds) |
| Errors | JSON `{"detail": ...}`; `422` for invalid input, `404` for ids that aren't yours |
| Pagination | `limit` (1-100, default 20) and `offset`; responses are `{data, total, limit, offset}` |

Read the key from the environment (`LINKTODM_API_KEY`). Retry `429` after
`Retry-After` and `5xx` with backoff; never retry `4xx` blindly.

## Endpoints

| Method and path | Does |
| --- | --- |
| `GET /v1/me` | Account: `id`, `name`, `email`, `plan`, `channels_count` |
| `GET /v1/channels` | Connected channels: `id`, `channel_type`, `name`, `username`, `profile_picture_url` |
| `GET /v1/contacts` | List contacts. Filters: `search` (name, username, email, phone), `channel_id`, `has_email`, `has_phone`, `tag` (repeatable, any of), `order_by` (`-created_at` default or `created_at`) |
| `GET /v1/contacts/{contact_id}` | One contact |
| `PATCH /v1/contacts/{contact_id}` | Set `email`, `phone_number`, and custom field values in `fields` (`{slug: value}`, `null` clears, max 50). Any other key is `422` |
| `DELETE /v1/contacts/{contact_id}` | **Permanent**: removes the contact with its tags and field values |
| `POST /v1/contacts/{contact_id}/tags` | Add tags: `{"tag_names": ["lead"]}` |
| `POST /v1/contacts/{contact_id}/tags/remove` | Remove tags: `{"tag_names": ["lead"]}` |
| `GET /v1/tags` | All tag names in use |
| `POST /v1/contacts/{contact_id}/send_message` | Queue a text DM: `{"text": "..."}` (1-1000 chars). Returns `202` `{status: "queued", contact_id, recipient_id}` |
| `GET /v1/custom_fields` | Custom field definitions: `id`, `name`, `slug`, `type`, `description`, `folder` |
| `POST /v1/custom_fields` | Create: `name` (required), `type` (TEXT default, NUMBER, DATE, DATETIME, BOOLEAN, ARRAY), `description`, `folder`. The `slug` is generated |
| `PATCH /v1/custom_fields/{field_id}` | Change `name`, `description`, `folder` (slug and type never change) |
| `DELETE /v1/custom_fields/{field_id}` | Delete a definition (values stay, hidden) |
| `POST /v1/webhooks`, `GET /v1/webhooks`, `DELETE /v1/webhooks/{id}` | Webhook subscriptions, see [webhooks.md](webhooks.md) |
| `GET /v1/events` | Recent contact events in webhook format; filter by `event_type`, `tag_name`, `field_slug`, `event_name`. Only events with a webhook subscription are recorded |

## The contact object

```json
{
  "id": 4821,
  "recipient_id": "17841400000000000",
  "username": "ada.lovelace",
  "name": "Ada",
  "email": "ada@example.com",
  "phone_number": null,
  "picture": "https://...",
  "tags": ["lead", "webinar"],
  "fields": {"plan": "pro"},
  "custom_fields": [{"slug": "plan", "name": "Plan", "value": "pro"}],
  "created_at": "2026-10-01T09:30:00",
  "updated_at": "2026-10-02T11:00:00"
}
```

`name`, `username` and `picture` come from Instagram/Facebook and are
read-only. `fields` holds stored values only; `custom_fields` lists every
live field, with `""` when unset.

## Things that trip people up

- **Contacts can't be created.** They appear when someone comments on or
  messages a connected account. To act on a person, find them first:
  `GET /v1/contacts?search=<username or email>`.
- **The 24-hour window.** `send_message` returns `202` once queued, but
  Instagram/Facebook only deliver if the contact messaged the account in the
  last 24 hours. Use it to answer recent conversations, not cold outreach.
- **Retries.** Send an `Idempotency-Key` header (a unique string per
  intended message, max 200 chars) on `send_message`. Requests with the same
  key are de-duplicated for about an hour, so a timed-out request can be
  retried without DMing twice.
- **Custom fields need a definition.** `PATCH ... {"fields": {"budget": "500"}}`
  only works if a field with slug `budget` exists; create it first with
  `POST /v1/custom_fields` and use the returned `slug`.
- **Channel ids** from `GET /v1/channels` are the values for the
  `channel_id` filter.

## Examples

- [examples/curl.md](../examples/curl.md): one call per endpoint.
- [examples/tag_and_message_lead.py](../examples/tag_and_message_lead.py):
  find a contact, save their email and a custom field, tag them, send a DM.
- [examples/webhook_receiver.py](../examples/webhook_receiver.py): receive
  contact events.
