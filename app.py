from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Other routes...

@app.route("/capsule-timeline")
def capsule_timeline():
    try:
        import json
        from flask import jsonify

        with open("reflex_capsules.json") as f:
            capsules = json.load(f)

        # Optional: Convert heatmap path to full URL if needed
        def get_heatmap_url(path):
            return f"/{path}" if not path.startswith("/") else path

        for c in capsules:
            c["heatmap"] = get_heatmap_url(c["heatmap"])

        # Sort capsules by timestamp (descending)
        timeline = sorted(capsules, key=lambda x: x.get("timestamp", ""), reverse=True)

        return jsonify({
            "timeline": timeline,
            "status": "timeline-ready"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "timeline-failed"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
