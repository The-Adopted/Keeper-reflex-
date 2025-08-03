from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def timeline():
    try:
        with open('dashboard/capsule_timeline.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return render_template('timeline.html', data=data)

@app.route('/api/capsules')
def api_capsules():
    with open('dashboard/capsule_timeline.json') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)
