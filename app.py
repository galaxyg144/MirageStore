from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__)

# Mounted path to your Deploy Disk on Render
APP_DIR = "/mnt/data/mapps"

# Ensure directory exists
os.makedirs(APP_DIR, exist_ok=True)

# List all .mapp files
@app.route("/apps", methods=["GET"])
def list_apps():
    files = [f for f in os.listdir(APP_DIR) if f.endswith(".mapp")]
    return jsonify(files)

# Download a specific app
@app.route("/apps/<filename>", methods=["GET"])
def get_app(filename):
    file_path = os.path.join(APP_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(APP_DIR, filename, as_attachment=True)
    return jsonify({"error": "App not found"}), 404

# Optional: simple upload endpoint (for admin/testing)
@app.route("/upload", methods=["POST"])
def upload_app():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if not file.filename.endswith(".mapp"):
        return jsonify({"error": "Only .mapp files allowed"}), 400
    file.save(os.path.join(APP_DIR, file.filename))
    return jsonify({"success": True, "filename": file.filename})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
