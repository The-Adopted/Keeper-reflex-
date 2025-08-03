#!/data/data/com.termux/files/usr/bin/bash

# === CONFIG ===
CAPSULE_FILE="$HOME/reflex-auth/dashboard/reflex_capsules.json"
BOT_TOKEN="$TELEGRAM_TOKEN"
CHAT_ID="$TELEGRAM_CHAT_ID"
SYNC_ENABLED=true  # Set to false to disable Telegram sync

# === INPUTS ===
EVENT="$1"
COMMENTARY="$2"
PHASE="$3"
STATUS="$4"
TAGS="$5"  # Comma-separated tags: "reflex,resilience,offline-mode"

# === TIMESTAMP ===
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.%6N")

# === CAPSULE JSON ===
CAPSULE=$(jq -n \
  --arg ts "$TIMESTAMP" \
  --arg ev "Tunnel failed" \
  --arg cm "Fallback to local preview successful" \
  --arg ph "fallback-preview" \
  --arg st "success" \
  --arg tg "reflex,resilience,offline-mode" \
  '{
    timestamp: $ts,
    phase: $ph,
    status: $st,
    event: $ev,
    commentary: $cm,
    tags: ($tg | split(","))
  }')

# === CREATE DIRECTORY IF MISSING ===
mkdir -p "$(dirname "$CAPSULE_FILE")"

# === LOCAL LOGGING ===
echo "$CAPSULE" >> "$CAPSULE_FILE"
echo "[✓] Capsule logged locally."

# === TELEGRAM SYNC ===
if [ "$SYNC_ENABLED" = true ]; then
  MESSAGE=$(echo "$CAPSULE" | jq -r '
    "🧠 Reflex Capsule\n\n📅 \(.timestamp)\n📍 Phase: \(.phase)\n✅ Status: \(.status)\n⚠️ Event: \(.event)\n💬 \(.commentary)\n🏷️ Tags: \(.tags | join(", "))"
  ')

  RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$MESSAGE")

  if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "[✓] Capsule synced to Telegram."
  else
    echo "[!] Telegram sync failed. Capsule retained locally."
  fi
fi
