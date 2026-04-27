# 🌍 World Situation — Real-Time Global News Dashboard

**World Situation** is a free, live global news aggregator and dashboard that collects real-time world news from Reuters, BBC, AP News, Al Jazeera, and NPR — all in one beautifully designed, single-page web application.

🚀 **Live site:** [varun-sv.github.io/world-situation](https://varun-sv.github.io/world-situation/)

---

## ✨ Features

- 🔄 **Real-Time Global News Feed** — live headlines aggregated from Reuters, BBC, AP, Al Jazeera, and NPR via RSS
- 📍 **Location-Aware Local News** — local headlines based on your geolocation (India: Times of India, The Hindu; US: NYT, WSJ)
- ⛅ **Live Local Weather** — real-time temperature and conditions via Open-Meteo
- 📈 **Global Market Data** — Dow Jones, Nikkei 225, FTSE 100 tickers
- 🌡️ **Chaos Level Indicator** — a satirical real-time gauge of global weirdness
- 🎨 **5 Visual Themes** — Serene Dawn, Midnight Matrix, Retro Terminal, Sahara Sunset, Synthwave Grid
- ⚡ **Single-File App** — all HTML, CSS, and JavaScript in one file; no backend, no build step
- 🌐 **No Login Required** — completely free and open source

---

## 🛠️ Tech Stack

- **HTML5 + Vanilla JavaScript** — zero dependencies
- **Tailwind CSS** (CDN) — responsive utility-first styling
- **Google Fonts** — Inter & Roboto Mono
- **RSS via allorigins.win** — CORS-safe feed proxy
- **Open-Meteo API** — free weather data
- **OpenStreetMap Nominatim** — reverse geocoding for local news

---

## 📂 Project Structure

```
world-situation/
├── index.html        ← main web application (HTML + CSS + JS)
├── streamlit-app.py  ← alternative Streamlit dashboard (NEXUS)
├── manifest.json     ← PWA web app manifest
├── robots.txt        ← search engine crawl directives
├── sitemap.xml       ← sitemap for Google Search Console
├── og-image.svg      ← social preview card image
└── requirements.txt  ← Python dependencies for Streamlit app
```

---

## 🚀 Deployment

The site is hosted on **GitHub Pages** and deploys automatically on every push to `main`.

To run your own copy:
1. Fork this repository
2. Enable GitHub Pages in repo settings (branch: `main`, folder: `/root`)
3. Your live global news dashboard is online instantly

---

## 🤝 Credits

Built with **AI collaboration**:
- [Claude](https://claude.ai)
- [ChatGPT](https://chat.openai.com)

---

## 📜 License

MIT License — free to fork, remix, and build on.
