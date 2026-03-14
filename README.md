# The Empathy Engine

A service that turns text into **emotion-aware speech**: it detects the sentiment of the input, then modulates **rate**, **pitch**, and **volume** of the synthesized voice so the delivery matches the emotion (positive, negative, or neutral). Output is playable **WAV** (CLI) or **MP3** (web/API) with an optional **web UI**.

---

## What It Does

- **Text input** via CLI, REST API, or web interface.
- **Emotion detection**: classifies text into **Positive**, **Negative**, or **Neutral** using VADER sentiment.
- **Vocal parameter modulation**: adjusts **rate** (speed), **pitch** (tone), and **volume** (amplitude) of the TTS output.
- **Emotion-to-voice mapping**: clear rules mapping each emotion (and intensity) to rate, pitch, and volume.
- **Audio output**: playable **.wav** (CLI) or **.mp3** (web/API) in the browser or any player.

---

## Setup

### 1. Python

Use **Python 3.10+** (or 3.8+; type hints use `tuple[str, float]` which is 3.9+; if you're on 3.8 we can use `Tuple` from `typing`—see note below).

### 2. Virtual environment (recommended)

```bash
cd empathy-engine
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. System TTS (for pyttsx3)

- **macOS**: Built-in. No extra install.
- **Windows**: SAPI is available by default.
- **Linux**: Install `espeak` or `festival`, e.g.  
  `sudo apt install espeak-ng` (Ubuntu/Debian).

---

## How to Run

### Option A: CLI

Pass the text as arguments:

```bash
python cli.py "This is the best day ever!"
```

Or run without arguments to be prompted for text:

```bash
python cli.py
```

The script prints the **detected emotion**, **rate** and **volume** used, and the **path to the generated WAV file**.

### Option B: Web UI and API

Start the Flask app:

```bash
python app.py
```

Then:

1. Open **http://127.0.0.1:5000** in your browser.
2. Type or paste text and click **Generate speech**.
3. The page shows the detected emotion and parameters and plays the audio.

**API** (e.g. for grading scripts):

```bash
curl -X POST http://127.0.0.1:5000/api/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so frustrated with this."}'
```

Response includes `audio_base64` (MP3), `emotion`, `rate`, `pitch`, and `volume`. The frontend plays the audio from the base64 data.

---

## Design Choices

### Emotion detection

- **VADER** (Valence Aware Dictionary and sEntiment Reasoner) is used for sentiment.
- **Three categories**: Positive (compound ≥ 0.05), Negative (compound ≤ -0.05), Neutral (otherwise).
- We also use the **compound magnitude** as an **intensity** (0–1) so stronger sentiment can drive stronger modulation (stretch goal: intensity scaling).

### Emotion-to-voice mapping

We modulate **rate**, **pitch**, and **volume** by emotion (intensity scales the effect):

| Emotion  | Rate   | Pitch   | Volume |
|----------|--------|---------|--------|
| Positive | +40%   | +18 Hz  | +8%    |
| Negative | −12%   | −14 Hz  | −6%    |
| Neutral  | 0%     | 0 Hz    | 0%     |

- **Baseline**: 175 wpm, volume 0.9.
- **Intensity**: For positive/negative, the strength of the sentiment scales how much we change rate and volume (e.g. “This is good” vs “This is the best news ever!”).
- **Rationale**: Positive → more energetic (faster, full volume). Negative → calmer and patient (slower, slightly lower volume). Neutral → default, clear delivery.

### TTS engine (web: natural voice + emotion)

- **Web/API**: **Edge-TTS** (voice `en-GB-RyanNeural`) with rate, pitch, volume; output **MP3**. Optional: set **`ELEVENLABS_API_KEY`** in `.env` for ElevenLabs (`pip install elevenlabs`).
- **CLI**: **pyttsx3** for offline **WAV** with rate/volume.

### API and UI

- **Flask** serves:
  - `GET /` → Web UI (text area + “Generate speech” + embedded audio player).
  - `POST /api/synthesize` → JSON with `audio_base64`, `emotion`, `rate`, `pitch`, `volume`.
- Audio is returned as base64 MP3 for in-browser playback.

---

## Project layout

```
empathy-engine/
├── README.md           # This file
├── requirements.txt    # flask, python-dotenv, vaderSentiment, pyttsx3, edge-tts
├── .env.example        # Optional: ELEVENLABS_API_KEY, EDGE_TTS_VOICE
├── emotion.py          # VADER emotion detection (positive/negative/neutral)
├── tts_engine.py       # pyttsx3 TTS for CLI (WAV)
├── emotional_tts.py    # Edge-TTS / ElevenLabs for web (MP3, rate/pitch/volume)
├── cli.py              # CLI (text → WAV)
├── app.py              # Flask app (API + web UI)
├── templates/index.html
└── static/output/
```

---

## More natural voice (optional)

Out of the box, the **web app** uses **Edge-TTS** with a natural voice and strong prosody so emotion is audible. For the **most natural, human-like** result:

1. Get a free API key from [ElevenLabs](https://elevenlabs.io/) (free tier available).
2. Install the client: `pip install elevenlabs`
3. Set your key: `export ELEVENLABS_API_KEY=your_key_here` (or `ELEVEN_API_KEY`)
4. Run the app as usual; it will use ElevenLabs when the key is set.

You can also set `ELEVENLABS_VOICE_ID` to use a different ElevenLabs voice.

---

## Optional: Python 3.8

If you must use Python 3.8, in `emotion.py` and `tts_engine.py` replace:

- `tuple[str, float]` with `Tuple[str, float]` and add `from typing import Tuple`.

---

## License

This project was built as an assignment (AI Intern assessment). Use and modify as needed for your submission.
