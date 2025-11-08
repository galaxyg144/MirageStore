from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)
APP_DIR = "mapps"  # will later mount your Render Deploy Disk here

# List all .mapp files
@app.route("/apps")
def list_apps():
    files = [f for f in os.listdir(APP_DIR) if f.endswith(".mapp")]
    return jsonify(files)

# Download a specific app
@app.route("/apps/<filename>")
def get_app(filename):
    if os.path.exists(os.path.join(APP_DIR, filename)):
        return send_from_directory(APP_DIR, filename, as_attachment=True)
    return {"error": "App not found"}, 404

if __name__ == "__main__":
    os.makedirs(APP_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=10000)
