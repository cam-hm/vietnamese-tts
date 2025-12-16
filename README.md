# 🎬 BBC Documentary TTS

A simple web app that converts text to speech with **BBC documentary-style narrator voices** using Google Cloud Text-to-Speech.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🇬🇧 **15+ Narrator Voices** - British & American accents
- 🎬 **Studio Quality** - Broadcast-ready voices for documentaries
- 🎚️ **Speed & Pitch Control** - Fine-tune your narration
- 🌙 **Modern Dark UI** - Beautiful glassmorphism design
- ⚡ **Fast Generation** - Powered by Google Cloud TTS

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Cloud account with Text-to-Speech API enabled

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/bbc-documentary-tts.git
cd bbc-documentary-tts

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Login to Google Cloud
gcloud auth application-default login
```

### Run

```bash
uvicorn main:app --reload --port 8001
```

Open http://localhost:8001 🎉

## 📁 Project Structure

```
bbc-documentary-tts/
├── main.py              # FastAPI app
├── tts_service.py       # Google Cloud TTS wrapper
├── requirements.txt
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## 🎤 Available Voices

| Type | Description |
|------|-------------|
| 🎬 **Studio** | Designed for broadcast/documentary |
| 🌟 **Chirp3-HD** | Ultra-natural, latest AI voices |
| 📻 **Neural2** | Standard high-quality voices |

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/voices` | List available voices |
| POST | `/api/synthesize` | Generate speech from text |

### Example Request

```bash
curl -X POST http://localhost:8001/api/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "In the heart of the African savanna...",
    "voice": "en-GB-Studio-B",
    "speaking_rate": 0.9,
    "pitch": -2.0
  }' \
  --output narration.mp3
```

## 📄 License

MIT License - feel free to use for any project!

---

Made with ❤️ for nature documentary enthusiasts
