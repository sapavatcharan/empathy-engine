"""
Flask app for the Empathy Engine: API + web UI.
- POST /api/synthesize: JSON { "text": "..." } -> returns audio as base64 (MP3) + emotion/params
- GET /: Web UI with text area and embedded audio player
Uses Edge-TTS with real rate, pitch, and volume so the voice sounds emotional.
Set ELEVENLABS_API_KEY in .env for more natural voice (optional).
"""

import base64
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load API key: .env.example first (fallback), then .env overrides if present
_env_dir = Path(__file__).resolve().parent
load_dotenv(_env_dir / ".env.example")
load_dotenv(_env_dir / ".env")

from emotional_tts import synthesize_emotional

app = Flask(__name__)
APP_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = APP_ROOT / "static" / "output"


def _ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/api/synthesize", methods=["POST"])
def api_synthesize():
    """Accept JSON { "text": "..." } and return emotional MP3 as base64 plus emotion/parameters."""
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Missing or empty 'text' in request body"}), 400

    try:
        mp3_data, emotion, rate_str, pitch_str, volume_str = synthesize_emotional(text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    audio_b64 = base64.b64encode(mp3_data).decode("ascii")
    return jsonify({
        "audio_base64": audio_b64,
        "audio_type": "audio/mpeg",
        "emotion": emotion,
        "rate": rate_str,
        "pitch": pitch_str,
        "volume": volume_str,
    })


if __name__ == "__main__":
    _ensure_output_dir()
    app.run(debug=True, port=5000)
