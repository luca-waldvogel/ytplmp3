# 🎵 ytplmp3 – YouTube Playlist & Video to MP3 Converter

A simple **Flask-based web application** that converts entire **YouTube playlists or single videos** into MP3 files.
I built this tool so I can easily download tracks and **burn them onto CDs for my car** 🚗💿.

---

## ✨ Features
- Convert a **single YouTube video** to an MP3 file
- Convert a **YouTube playlist** to a ZIP archive containing all MP3s
- Clean file naming (playlist index + title for playlists)
- Web UI with **Bootstrap** and a loading spinner
- Helpful error messages and basic input validation
- **Privacy-friendly**: no user data is stored on the server

---

## 🧰 Tech Stack
- **Python** (Flask)
- **yt-dlp** for media extraction
- **FFmpeg** for audio conversion (required)
- **Bootstrap 4** for the UI

---

## ✅ Prerequisites
- **Python 3.9+**
- **FFmpeg** installed and available in your PATH
  - macOS: `brew install ffmpeg`
  - Windows (PowerShell as Admin): `choco install ffmpeg` *(or use the official build from Gyan.dev and add to PATH)*
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
- (Optional) **Firefox** if you keep `cookiesfrombrowser=('firefox',)` in `yt-dlp` options

> ℹ️ If you don’t want/need authenticated playback, you can remove the `cookiesfrombrowser` option from `ydl_opts`.

---

## ⚖️ Legal & Disclaimer
This tool is provided for personal use only.
Ensure that you only download content you have the rights to. Respect YouTube’s Terms of Service and local copyright laws.
