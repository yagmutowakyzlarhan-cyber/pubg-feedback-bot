import os
import base64
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

@app.route("/send_feedback_custom_your_url_here", methods=["POST"])
def receive_feedback():
    try:
        base64_image = request.form.get("base64_image", "")
        caption = request.form.get("caption", "")

        if not base64_image:
            return jsonify({"status": False, "error": "no image"}), 400

        image_bytes = base64.b64decode(base64_image)

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {"photo": ("screenshot.jpg", image_bytes)}
        data = {
            "chat_id": CHANNEL_ID,
            "caption": caption,
            "parse_mode": "HTML"
        }

        resp = requests.post(url, files=files, data=data, timeout=30)

        if resp.status_code == 200:
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "error": resp.text}), 500

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500


@app.route("/")
def health():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
