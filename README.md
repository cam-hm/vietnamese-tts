# 🎤 Vietnamese TTS

Ứng dụng web chuyển văn bản thành giọng nói tiếng Việt sử dụng **Cartesia AI**.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🇻🇳 **Vietnamese Voices** - Linh (Female) & Minh (Male)
- 🎯 **Cartesia Sonic-3** - Model TTS mới nhất
- 🎚️ **Speed Control** - Điều chỉnh tốc độ đọc
- 🌙 **Modern Dark UI** - Giao diện đẹp, hiện đại
- ⚡ **Fast Generation** - Powered by Cartesia AI

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Cartesia API key từ [cartesia.ai](https://cartesia.ai)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/vietnamese-tts.git
cd vietnamese-tts

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
echo "CARTESIA_API_KEY=your-api-key" > .env
```

### Run

```bash
uvicorn main:app --reload --port 8001
```

Open http://localhost:8001 🎉

## 📁 Project Structure

```
vietnamese-tts/
├── main.py              # FastAPI app
├── tts_service.py       # Cartesia TTS wrapper
├── requirements.txt
├── .env                 # CARTESIA_API_KEY
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## 🎤 Available Voices

| Voice | Gender | ID |
|-------|--------|-----|
| Linh ⭐ | Female | `935a9060-373c-49e4-b078-f4ea6326987a` |
| Minh ⭐ | Male | `0e58d60a-2f1a-4252-81bd-3db6af45fb41` |

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/voices` | Danh sách voices |
| POST | `/api/synthesize` | Tạo giọng nói từ văn bản |

### Example Request

```bash
curl -X POST http://localhost:8001/api/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào Việt Nam!",
    "voice": "935a9060-373c-49e4-b078-f4ea6326987a",
    "speaking_rate": 1.0
  }' \
  --output output.mp3
```

## 📄 License

MIT License

---

Made with ❤️ using Cartesia AI
