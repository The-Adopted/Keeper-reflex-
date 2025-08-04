from flask import Flask, render_template, jsonify
import json
import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

app = Flask(__name__)

def load_capsules():
    try:
        with open('runtime/reflex_capsules.json') as f:
            capsules = json.load(f)
            print(f"🧠 Loaded {len(capsules)} capsules")
            for c in capsules:
                print(f"📦 Capsule: {c['title']} | Reflex Weight: {c['reflex_weight']}")
            return capsules
    except Exception as e:
        print(f"⚠️ Capsule load error: {e}")
        return []

@app.route('/')
def index():
    capsules = load_capsules()
    return render_template('index.html', capsules=capsules)

@app.route('/api/capsules')
def api_capsules():
    return jsonify(load_capsules())

if __name__ == '__main__':
import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

