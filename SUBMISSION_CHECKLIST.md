# Submission checklist – Challenge 1: The Empathy Engine

## Assignment requirements ✓

| # | Requirement | Status |
|---|-------------|--------|
| 1 | **Text input** (CLI or API) | ✓ CLI (`cli.py`), API (`POST /api/synthesize`), Web UI |
| 2 | **Emotion detection** (≥3 categories) | ✓ Positive, Negative, Neutral (VADER) |
| 3 | **Vocal parameter modulation** (≥2 params) | ✓ Rate, pitch, volume |
| 4 | **Emotion-to-voice mapping** (clear logic) | ✓ Documented in README + code |
| 5 | **Audio output** (playable .wav/.mp3) | ✓ WAV (CLI), MP3 (web/API) |

## Deliverables ✓

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | GitHub repo with runnable source code | ✓ Ready to push |
| 2 | README: description, setup, run instructions | ✓ |
| 3 | README: design choices (emotion → voice mapping) | ✓ |

## Before you push

- [x] API key removed from `.env.example` (use `.env` locally; `.env` is gitignored)
- [x] `venv/`, `.env`, `sample_outputs/`, `*.wav` in `.gitignore`

## After push

1. Open the repo on GitHub and confirm README renders.
2. Submit the **repository URL** as your deliverable.
