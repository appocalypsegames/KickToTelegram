# 📺 Kick to Telegram

**Kick to Telegram** is a lightweight Python tool that monitors a [Kick.com](https://kick.com) channel and automatically restreams its live broadcasts to a Telegram chat or channel — with a real-time overlay of the Kick chat embedded directly into the video stream.

---

## ✨ Features

- ✅ Automatically detects when a Kick channel goes live  
- 📡 Restreams the live broadcast to Telegram via RTMP  
- 💬 Adds a real-time chat overlay from Kick onto the video  
- ⚙️ Simple and minimal configuration via `config.py`  
- 🪶 Lightweight, efficient, and easy to deploy

---

## 📦 Requirements

Before getting started, ensure the following are installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [FFmpeg](https://ffmpeg.org/download.html) — must be accessible via your system terminal

---

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/appocalypsegames/KickToTelegram.git
   cd KickToTelegram
   ```
2. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
---

## ⚙️ Configuration

Edit the `config.py` file and set your own parameters:

```python
# config.py

# RTMP endpoint provided by Telegram (@livegrambot)
TELEGRAM_RTMP_URL = "rtmps://dc4-1.rtmp.t.me/s/"

# Your Telegram stream key (keep this private!)
TELEGRAM_STREAM_KEY = "your_stream_key_here"

# Kick.com channel username to monitor (without URL)
KICK_CHANNEL = "your_kick_channel"
```

> 🔐 **Note:** Do **not** share your `TELEGRAM_STREAM_KEY` publicly — it can be used to broadcast to your Telegram channel without permission.

---

## ▶️ Usage

Run the main script with:

```bash
python main.py
```
## 🔄 What the Script Does

1. 🔍 Continuously monitors the Kick channel defined in `KICK_CHANNEL`
2. 📡 When the channel goes live:
   - 🎥 Captures the live stream using **FFmpeg**
   - 💬 Adds a **real-time overlay** of the Kick chat onto the video
   - 🚀 Restreams the final video output to **Telegram via RTMP**

---

## ⚠️ Compatibility Notice

This tool is confirmed to be **working as of July 16, 2025**.

Please note that it relies on the current public-facing infrastructure of [Kick.com](https://kick.com), including access to stream URLs and chat endpoints.  
Should Kick update or restrict access to these components in the future, the script may **require modifications** or **cease to function** until patched.

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute the code with proper attribution.  
For more details, see the [MIT License](https://opensource.org/licenses/MIT).

---

## 🙋 Support

If you encounter any issues or have feature requests, feel free to open an [issue](https://github.com/appocalypsegames/KickToTelegram/issues) on this repository.

