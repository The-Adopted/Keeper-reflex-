from flask import Flask, jsonify, request
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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

        app.logger.info(f"Capsule preview accessed with filters: overlay_type={overlay_type}, phase={phase}, min_weight={min_weight}")

        return jsonify({
            "capsules": filtered,
            "status": "preview-ready",
            "filters": {
                "overlay_type": overlay_type,
                "phase": phase,
                "min_weight": min_weight
            }
        })

    except Exception as e:
        app.logger.error(f"Error loading capsules: {str(e)}")
        return jsonify({"error": str(e), "status": "preview-failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
