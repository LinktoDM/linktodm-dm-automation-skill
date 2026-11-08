# Public API with curl

```sh
export LINKTODM_API_KEY="..."            # Settings → API in the dashboard (Pro+)
API=https://api.linktodm.com/api/public/v1
H="X-API-Key: $LINKTODM_API_KEY"
```

## Account and channels

```sh
curl -s "$API/me" -H "$H"
curl -s "$API/channels" -H "$H"
```

## Contacts

```sh
# Find someone (name, username, email or phone), newest first
curl -s "$API/contacts?search=ada&limit=5" -H "$H"

# Contacts tagged lead OR webinar on one channel
curl -s "$API/contacts?tag=lead&tag=webinar&channel_id=ig-business-17841400000000000" -H "$H"

curl -s "$API/contacts/4821" -H "$H"

# Save email and a custom field value (the field must exist; null clears)
curl -s -X PATCH "$API/contacts/4821" -H "$H" -H "Content-Type: application/json" \
  -d '{"email": "ada@example.com", "fields": {"plan": "pro"}}'

# Permanent: removes the contact, its tags and field values
curl -s -X DELETE "$API/contacts/4821" -H "$H"
```

## Tags

```sh
curl -s -X POST "$API/contacts/4821/tags" -H "$H" -H "Content-Type: application/json" \
  -d '{"tag_names": ["lead"]}'
curl -s -X POST "$API/contacts/4821/tags/remove" -H "$H" -H "Content-Type: application/json" \
  -d '{"tag_names": ["lead"]}'
curl -s "$API/tags" -H "$H"
```

## Custom fields

```sh
curl -s "$API/custom_fields" -H "$H"
curl -s -X POST "$API/custom_fields" -H "$H" -H "Content-Type: application/json" \
  -d '{"name": "Plan", "type": "TEXT"}'          # returns the generated slug
curl -s -X PATCH "$API/custom_fields/12" -H "$H" -H "Content-Type: application/json" \
  -d '{"name": "Plan tier"}'
curl -s -X DELETE "$API/custom_fields/12" -H "$H"
```

## Send a DM

Only delivered if the contact messaged the account in the last 24 hours.

```sh
curl -s -X POST "$API/contacts/4821/send_message" -H "$H" \
  -H "Content-Type: application/json" -H "Idempotency-Key: order-1042-thanks" \
  -d '{"text": "Thanks for your order! Here is your guide: https://example.com/guide"}'
```

## Webhooks and events

```sh
curl -s -X POST "$API/webhooks" -H "$H" -H "Content-Type: application/json" \
  -d '{"event_type": "contact.email_set", "target_url": "https://example.com/hooks/linktodm-7f3k9q"}'
curl -s "$API/webhooks" -H "$H"
curl -s "$API/events?event_type=contact.email_set&limit=5" -H "$H"
curl -s -X DELETE "$API/webhooks/31" -H "$H"
```
