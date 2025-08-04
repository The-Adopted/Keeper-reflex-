from flask import Flask, jsonify
import os
import logging

app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Health check route
@app.route('/health')
def health():
    app.logger.info("Health check accessed")
    return jsonify({"status": "ok"}), 200

# Homepage or root route
@app.route('/')
def home():
    app.logger.info("Homepage accessed")
    return jsonify({
        "message": "Welcome to Keeper Reflex Dashboard",
        "status": "running"
    })

# Reflex capsule preview route (placeholder)
@app.route('/capsule-preview')
def capsule_preview():
    app.logger.info("Capsule preview accessed")
    return jsonify({
        "capsule": "Reflex Capsule Timeline",
        "status": "preview-ready"
    })

# Run the app with Railway-compatible port binding
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
