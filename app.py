from flask import Flask, jsonify, request
import json
import os
import logging
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Emoji tags for overlay types
EMOJI_TAGS = {
    "sentiment": "🧠",
    "volatility": "⚡",
    "correlation": "🔗"
}

# Telegram credentials
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route('/health')
def health():
    app.logger.info("Health check accessed")
    return jsonify({"status": "ok"}), 200

@app.route('/')
def home():
    app.logger.info("Homepage accessed")
    return jsonify({
        "message": "Welcome to Keeper Reflex Dashboard",
        "status": "running"
    })

@app.route('/capsule-preview', methods=['GET'])
def capsule_preview():
    try:
        with open('reflex_capsules.json') as f:
            capsules = json.load(f)

        overlay_type = request.args.get('overlay_type')
        phase = request.args.get('phase')
        min_weight = float(request.args.get('min_weight', 0))

        filtered = [
            c for c in capsules
            if (not overlay_type or c['overlay_type'] == overlay_type)
            and (not phase or c['phase'] == phase)
            and c['reflex_weight'] >= min_weight
        ]

        # Inject emoji tags
        for c in filtered:
            c["emoji"] = EMOJI_TAGS.get(c["overlay_type"], "🧩")

        # Digest bundling
        digest = {}
        for capsule in filtered:
            key = capsule["overlay_type"]
            if key not in digest:
                digest[key] = {
                    "count": 0,
                    "total_weight": 0,
                    "top_capsule": capsule["capsule_id"],
                    "max_weight": capsule["reflex_weight"]
                }
            digest[key]["count"] += 1
            digest[key]["total_weight"] += capsule["reflex_weight"]
            if capsule["reflex_weight"] > digest[key]["max_weight"]:
                digest[key]["top_capsule"] = capsule["capsule_id"]
                digest[key]["max_weight"] = capsule["reflex_weight"]

        for key in digest:
            digest[key]["avg_weight"] = round(digest[key]["total_weight"] / digest[key]["count"], 2)

        # Telegram alerts
        for capsule in filtered:
            if capsule["reflex_weight"] > 0.85:
                message = f"📡 Reflex Alert: {capsule['capsule_id']} ({capsule['overlay_type']})\nWeight: {capsule['reflex_weight']}\nCommentary: {capsule['commentary']}"
                send_telegram_alert(message)

        return jsonify({
            "capsules": filtered,
            "digest": digest,
            "filters": {
                "overlay_type": overlay_type,
                "phase": phase,
                "min_weight": min_weight
            },
            "status": "preview-ready"
        })

    except Exception as e:
        app.logger.error(f"Error loading capsules: {str(e)}")
        return jsonify({"error": str(e), "status": "preview-failed"}), 500

def send_telegram_alert(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            requests.post(url, json=payload)
            app.logger.info("Telegram alert sent")
        except Exception as e:
            app.logger.error(f"Telegram alert failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
