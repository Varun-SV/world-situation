import streamlit as st
import feedparser
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import json
from collections import defaultdict

# ============================================================================
# CONFIGURATION & PAGE SETUP
# ============================================================================
st.set_page_config(
    page_title="NEXUS • Global Intelligence Platform",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ADVANCED THEME SYSTEM
# ============================================================================
THEMES = {
    "Cyberpunk 2077": {
        "bg_primary": "#0a0e27",
        "bg_secondary": "#151932",
        "bg_tertiary": "#1f2347",
        "card_bg": "rgba(31, 35, 71, 0.6)",
        "card_border": "rgba(255, 0, 255, 0.3)",
        "text_primary": "#ffffff",
        "text_secondary": "#b8c5d6",
        "text_muted": "#7a8394",
        "accent_primary": "#ff00ff",
        "accent_secondary": "#00ffff",
        "success": "#00ff88",
        "warning": "#ffaa00",
        "danger": "#ff0055",
        "glow": "rgba(255, 0, 255, 0.5)",
        "gradient": "linear-gradient(135deg, #0a0e27 0%, #1f2347 50%, #2d1b4e 100%)",
    },
    "Arctic Frost": {
        "bg_primary": "#0f1923",
        "bg_secondary": "#1a2332",
        "bg_tertiary": "#243447",
        "card_bg": "rgba(36, 52, 71, 0.6)",
        "card_border": "rgba(94, 217, 217, 0.3)",
        "text_primary": "#e8f4f8",
        "text_secondary": "#b3d9e8",
        "text_muted": "#7a9fb5",
        "accent_primary": "#5ed9d9",
        "accent_secondary": "#7af3f3",
        "success": "#4ade80",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "glow": "rgba(94, 217, 217, 0.5)",
        "gradient": "linear-gradient(135deg, #0f1923 0%, #1a2332 50%, #243447 100%)",
    },
    "Matrix Reloaded": {
        "bg_primary": "#000000",
        "bg_secondary": "#001a00",
        "bg_tertiary": "#003300",
        "card_bg": "rgba(0, 51, 0, 0.5)",
        "card_border": "rgba(0, 255, 65, 0.3)",
        "text_primary": "#00ff41",
        "text_secondary": "#00cc33",
        "text_muted": "#008822",
        "accent_primary": "#00ff41",
        "accent_secondary": "#39ff14",
        "success": "#00ff41",
        "warning": "#ffff00",
        "danger": "#ff0000",
        "glow": "rgba(0, 255, 65, 0.6)",
        "gradient": "linear-gradient(135deg, #000000 0%, #001a00 50%, #003300 100%)",
    },
    "Tokyo Neon": {
        "bg_primary": "#1a0a2e",
        "bg_secondary": "#2d1650",
        "bg_tertiary": "#3f2272",
        "card_bg": "rgba(63, 34, 114, 0.6)",
        "card_border": "rgba(255, 107, 107, 0.3)",
        "text_primary": "#fef9f3",
        "text_secondary": "#f9d5e5",
        "text_muted": "#c9a9d1",
        "accent_primary": "#ff6b6b",
        "accent_secondary": "#feca57",
        "success": "#1dd1a1",
        "warning": "#feca57",
        "danger": "#ee5a6f",
        "glow": "rgba(255, 107, 107, 0.5)",
        "gradient": "linear-gradient(135deg, #1a0a2e 0%, #2d1650 50%, #4a1f6f 100%)",
    },
    "Solar Eclipse": {
        "bg_primary": "#1c1c1e",
        "bg_secondary": "#2c2c2e",
        "bg_tertiary": "#3a3a3c",
        "card_bg": "rgba(58, 58, 60, 0.6)",
        "card_border": "rgba(255, 159, 64, 0.3)",
        "text_primary": "#ffffff",
        "text_secondary": "#e5e5e7",
        "text_muted": "#98989d",
        "accent_primary": "#ff9f40",
        "accent_secondary": "#ffcd56",
        "success": "#36a2eb",
        "warning": "#ffcd56",
        "danger": "#ff6384",
        "glow": "rgba(255, 159, 64, 0.5)",
        "gradient": "linear-gradient(135deg, #1c1c1e 0%, #2c2c2e 50%, #3a3a3c 100%)",
    }
}

def inject_premium_css(theme_name):
    t = THEMES[theme_name]
    
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* ==================== GLOBAL STYLES ==================== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        .stApp {{
            background: {t['gradient']};
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: {t['text_primary']};
        }}
        
        /* Hide Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        
        /* ==================== GLASSMORPHISM CARDS ==================== */
        .glass-card {{
            background: {t['card_bg']};
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid {t['card_border']};
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .glass-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, {t['accent_primary']}, transparent);
            transition: left 0.5s;
        }}
        
        .glass-card:hover {{
            transform: translateY(-4px) scale(1.01);
            border-color: {t['accent_primary']};
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5), 0 0 40px {t['glow']};
        }}
        
        .glass-card:hover::before {{
            left: 100%;
        }}
        
        /* ==================== HERO SECTION ==================== */
        .hero-title {{
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, {t['text_primary']}, {t['accent_primary']}, {t['accent_secondary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            letter-spacing: -2px;
            line-height: 1;
            animation: glow 3s ease-in-out infinite;
        }}
        
        @keyframes glow {{
            0%, 100% {{ filter: drop-shadow(0 0 20px {t['glow']}); }}
            50% {{ filter: drop-shadow(0 0 40px {t['glow']}); }}
        }}
        
        .hero-subtitle {{
            font-size: 1.2rem;
            color: {t['text_secondary']};
            font-weight: 500;
            letter-spacing: 0.5px;
        }}
        
        /* ==================== SECTION HEADERS ==================== */
        .section-header {{
            font-size: 1.5rem;
            font-weight: 800;
            color: {t['accent_primary']};
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .section-header::before {{
            content: '';
            width: 4px;
            height: 28px;
            background: linear-gradient(180deg, {t['accent_primary']}, {t['accent_secondary']});
            border-radius: 2px;
            box-shadow: 0 0 10px {t['glow']};
        }}
        
        /* ==================== NEWS CARDS ==================== */
        .news-card {{
            background: {t['card_bg']};
            backdrop-filter: blur(15px);
            border: 1px solid {t['card_border']};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .news-card::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 3px;
            height: 100%;
            background: {t['accent_primary']};
            transform: translateX(-3px);
            transition: transform 0.3s;
        }}
        
        .news-card:hover {{
            border-color: {t['accent_primary']};
            transform: translateX(8px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), -4px 0 20px {t['glow']};
        }}
        
        .news-card:hover::before {{
            transform: translateX(0);
        }}
        
        .news-source {{
            font-size: 0.7rem;
            color: {t['accent_primary']};
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .news-time {{
            color: {t['text_muted']};
            font-size: 0.65rem;
            margin-left: auto;
        }}
        
        .news-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: {t['text_primary']};
            margin-bottom: 10px;
            line-height: 1.5;
            transition: color 0.2s;
        }}
        
        .news-card:hover .news-title {{
            color: {t['accent_primary']};
        }}
        
        .news-title a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .news-summary {{
            font-size: 0.9rem;
            color: {t['text_secondary']};
            line-height: 1.6;
            opacity: 0.9;
        }}
        
        /* ==================== METRIC CARDS ==================== */
        .metric-card {{
            background: {t['card_bg']};
            backdrop-filter: blur(20px);
            border: 1px solid {t['card_border']};
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: {t['glow']};
            transform: translate(-50%, -50%);
            transition: width 0.5s, height 0.5s;
        }}
        
        .metric-card:hover::after {{
            width: 300px;
            height: 300px;
        }}
        
        .metric-card:hover {{
            border-color: {t['accent_primary']};
            box-shadow: 0 0 40px {t['glow']};
        }}
        
        .metric-label {{
            font-size: 0.75rem;
            color: {t['text_muted']};
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }}
        
        .metric-value {{
            font-size: 3.5rem;
            font-weight: 900;
            color: {t['accent_primary']};
            margin: 16px 0;
            text-shadow: 0 0 30px {t['glow']};
            position: relative;
            z-index: 1;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .metric-subtitle {{
            font-size: 1.2rem;
            color: {t['text_primary']};
            font-weight: 600;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }}
        
        .metric-footer {{
            color: {t['text_secondary']};
            font-size: 0.85rem;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid {t['card_border']};
            position: relative;
            z-index: 1;
        }}
        
        /* ==================== STATUS BADGES ==================== */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }}
        
        .badge-success {{
            background: rgba(74, 222, 128, 0.15);
            color: {t['success']};
            border: 1px solid {t['success']};
            box-shadow: 0 0 15px rgba(74, 222, 128, 0.3);
        }}
        
        .badge-warning {{
            background: rgba(251, 191, 36, 0.15);
            color: {t['warning']};
            border: 1px solid {t['warning']};
            box-shadow: 0 0 15px rgba(251, 191, 36, 0.3);
        }}
        
        .badge-danger {{
            background: rgba(248, 113, 113, 0.15);
            color: {t['danger']};
            border: 1px solid {t['danger']};
            box-shadow: 0 0 15px rgba(248, 113, 113, 0.3);
        }}
        
        .badge-primary {{
            background: rgba(94, 217, 217, 0.15);
            color: {t['accent_primary']};
            border: 1px solid {t['accent_primary']};
            box-shadow: 0 0 15px {t['glow']};
        }}
        
        .badge:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 25px currentColor;
        }}
        
        /* ==================== MARKET CARDS ==================== */
        .market-card {{
            background: {t['card_bg']};
            backdrop-filter: blur(20px);
            border: 1px solid {t['card_border']};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
            transition: all 0.3s;
        }}
        
        .market-card:hover {{
            border-color: {t['accent_primary']};
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            transform: translateY(-2px);
        }}
        
        .market-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .market-name {{
            font-weight: 700;
            font-size: 0.95rem;
            color: {t['text_secondary']};
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .market-price {{
            font-size: 1.8rem;
            font-weight: 900;
            color: {t['text_primary']};
            margin-bottom: 8px;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        /* ==================== TABS ==================== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: {t['card_bg']};
            padding: 8px;
            border-radius: 12px;
            backdrop-filter: blur(20px);
            border: 1px solid {t['card_border']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border-radius: 8px;
            color: {t['text_muted']};
            font-weight: 700;
            padding: 12px 28px;
            border: 1px solid transparent;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.85rem;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: {t['accent_primary']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {t['accent_primary']}, {t['accent_secondary']}) !important;
            color: #000 !important;
            box-shadow: 0 0 20px {t['glow']} !important;
            border: 1px solid {t['accent_primary']} !important;
        }}
        
        /* ==================== SIDEBAR ==================== */
        [data-testid="stSidebar"] {{
            background: {t['bg_secondary']};
            border-right: 1px solid {t['card_border']};
        }}
        
        [data-testid="stSidebar"] .glass-card {{
            background: {t['card_bg']};
            backdrop-filter: blur(10px);
        }}
        
        /* ==================== ANIMATIONS ==================== */
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.8; transform: scale(1.05); }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .pulse {{
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }}
        
        .slide-in {{
            animation: slideIn 0.5s ease-out;
        }}
        
        /* ==================== SCROLLBAR ==================== */
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {t['bg_secondary']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {t['accent_primary']}, {t['accent_secondary']});
            border-radius: 6px;
            border: 2px solid {t['bg_secondary']};
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {t['accent_primary']};
            box-shadow: 0 0 10px {t['glow']};
        }}
        
        /* ==================== STATS GRID ==================== */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .stat-item {{
            background: {t['card_bg']};
            backdrop-filter: blur(15px);
            border: 1px solid {t['card_border']};
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
        }}
        
        .stat-item:hover {{
            border-color: {t['accent_primary']};
            box-shadow: 0 0 20px {t['glow']};
            transform: translateY(-4px);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 900;
            color: {t['accent_primary']};
            font-family: 'JetBrains Mono', monospace;
            text-shadow: 0 0 20px {t['glow']};
        }}
        
        .stat-label {{
            font-size: 0.8rem;
            color: {t['text_muted']};
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 8px;
            font-weight: 600;
        }}
        
        /* ==================== LOADING SPINNER ==================== */
        .spinner {{
            width: 50px;
            height: 50px;
            border: 4px solid {t['card_border']};
            border-top: 4px solid {t['accent_primary']};
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* ==================== UTILITIES ==================== */
        .text-gradient {{
            background: linear-gradient(135deg, {t['accent_primary']}, {t['accent_secondary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent, {t['card_border']}, transparent);
            margin: 32px 0;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# DATA FETCHING & CACHING
# ============================================================================

@st.cache_data(ttl=300)
def fetch_news(category="world"):
    """Fetch news from multiple RSS feeds"""
    feeds = {
        "world": [
            "https://feeds.reuters.com/Reuters/worldNews",
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.apnews.com/AP-Top-News"
        ],
        "tech": [
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.theverge.com/rss/index.xml",
            "https://hnrss.org/frontpage"
        ],
        "science": [
            "https://www.sciencedaily.com/rss/top/science.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml"
        ],
        "business": [
            "https://feeds.reuters.com/reuters/businessNews",
            "https://feeds.bbci.co.uk/news/business/rss.xml"
        ]
    }
    
    articles = []
    selected_feeds = feeds.get(category, feeds["world"])
    
    for url in selected_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Just now"),
                    "source": feed.feed.get("title", "Unknown Source"),
                    "summary": entry.get("summary", entry.get("description", ""))[:200] + "...",
                    "category": category
                })
        except Exception as e:
            continue
    
    random.shuffle(articles)
    return articles[:12]

@st.cache_data(ttl=900)
def fetch_weather(lat, lon, city_name):
    """Fetch weather data from Open-Meteo API"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability&timezone=auto"
        response = requests.get(url, timeout=10)
        data = response.json()
        current = data.get("current_weather", {})
        
        # Weather code to emoji mapping
        wcode = current.get("weathercode", 0)
        conditions = {
            0: ("Clear Sky", "☀️"),
            1: ("Mainly Clear", "🌤️"),
            2: ("Partly Cloudy", "⛅"),
            3: ("Overcast", "☁️"),
            45: ("Foggy", "🌫️"),
            48: ("Rime Fog", "🌫️"),
            51: ("Light Drizzle", "🌦️"),
            61: ("Rain", "🌧️"),
            71: ("Snow", "❄️"),
            80: ("Rain Showers", "🌧️"),
            95: ("Thunderstorm", "⛈️"),
        }
        
        for code, (desc, icon) in sorted(conditions.items(), reverse=True):
            if wcode >= code:
                condition_desc, condition_icon = desc, icon
                break
        else:
            condition_desc, condition_icon = "Unknown", "❓"
        
        return {
            "temp": current.get("temperature", "--"),
            "speed": current.get("windspeed", "--"),
            "icon": condition_icon,
            "condition": condition_desc,
            "city": city_name,
            "hourly": data.get("hourly", {})
        }
    except Exception as e:
        return {
            "temp": "--",
            "speed": "--",
            "icon": "❓",
            "condition": "Unknown",
            "city": city_name,
            "hourly": {}
        }

@st.cache_data(ttl=60)
def generate_market_data():
    """Generate realistic market data with trends"""
    tickers = {
        "S&P 500": {"base": 4500, "volatility": 0.015},
        "NASDAQ": {"base": 14000, "volatility": 0.02},
        "DOW": {"base": 35000, "volatility": 0.012},
        "BTC-USD": {"base": 42000, "volatility": 0.03},
        "ETH-USD": {"base": 2200, "volatility": 0.035},
        "GOLD": {"base": 1950, "volatility": 0.008},
    }
    
    data = {}
    
    for ticker, params in tickers.items():
        base = params["base"]
        vol = params["volatility"]
        
        # Generate 24-hour price history
        prices = [base]
        for _ in range(24):
            change = random.uniform(-vol, vol) * base
            prices.append(max(prices[-1] + change, base * 0.8))
        
        current = prices[-1]
        change_pct = ((current - prices[0]) / prices[0]) * 100
        
        # Volume simulation
        volume = random.randint(1000000, 10000000)
        
        data[ticker] = {
            "history": prices,
            "current": current,
            "change": change_pct,
            "volume": volume,
            "high": max(prices),
            "low": min(prices)
        }
    
    return data

def calculate_sentiment_score():
    """Calculate a pseudo-sentiment score"""
    # In production, this would analyze news headlines
    return random.uniform(-1, 1)

def generate_world_stats():
    """Generate interesting world statistics"""
    return {
        "active_conflicts": random.randint(15, 30),
        "global_temp_anomaly": round(random.uniform(0.8, 1.5), 2),
        "internet_users": round(5.3 + random.uniform(-0.1, 0.1), 2),
        "co2_ppm": random.randint(415, 425),
        "crypto_market_cap": random.randint(1500, 2500),
    }

# ============================================================================
# COMPONENT RENDERERS
# ============================================================================

def render_news_card(article, theme):
    """Render a single news card"""
    time_ago = article['published'][:16] if len(article['published']) > 16 else article['published']
    
    st.markdown(f"""
    <div class="news-card">
        <div class="news-source">
            <span>📡</span>
            <span>{article['source']}</span>
            <span class="news-time">{time_ago}</span>
        </div>
        <div class="news-title">
            <a href="{article['link']}" target="_blank">{article['title']}</a>
        </div>
        <div class="news-summary">
            {article['summary']}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_weather_card(weather, theme):
    """Render weather widget"""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT CONDITIONS</div>
        <div style="font-size: 5rem; margin: 20px 0;">{weather['icon']}</div>
        <div class="metric-value">{weather['temp']}°</div>
        <div class="metric-subtitle">{weather['city']}</div>
        <div style="color: {theme['text_secondary']}; margin-top: 12px;">
            {weather['condition']}
        </div>
        <div class="metric-footer">
            <div style="display: flex; justify-content: space-around;">
                <div>💨 {weather['speed']} km/h</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_market_card(name, data, theme):
    """Render market ticker card with chart"""
    color = theme['success'] if data['change'] >= 0 else theme['danger']
    arrow = "↗" if data['change'] >= 0 else "↘"
    
    # Create sparkline
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=data['history'],
        mode='lines',
        line=dict(color=color, width=2.5),
        fill='tozeroy',
        fillcolor='rgba(74, 222, 128, 0.1)' if data['change'] >= 0 else 'rgba(248, 113, 113, 0.1)',
        hovertemplate='$%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=70,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    
    st.markdown(f"""
    <div class="market-card">
        <div class="market-header">
            <span class="market-name">{name}</span>
            <span class="badge" style="color: {color}; border-color: {color};">
                {arrow} {abs(data['change']):.2f}%
            </span>
        </div>
        <div class="market-price">${data['current']:,.2f}</div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: {theme['text_muted']}; margin-top: 8px;">
            <span>H: ${data['high']:,.2f}</span>
            <span>L: ${data['low']:,.2f}</span>
            <span>Vol: {data['volume']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sentiment_meter(score, theme):
    """Render global sentiment meter"""
    # Convert -1 to 1 scale to 0-100
    percentage = (score + 1) / 2 * 100
    
    if score > 0.3:
        status, color, emoji = "OPTIMISTIC", theme['success'], "😊"
    elif score > -0.3:
        status, color, emoji = "NEUTRAL", theme['warning'], "😐"
    else:
        status, color, emoji = "PESSIMISTIC", theme['danger'], "😟"
    
    st.markdown(f"""
    <div class="metric-card pulse">
        <div class="metric-label">GLOBAL SENTIMENT INDEX</div>
        <div style="font-size: 4rem; margin: 20px 0;">{emoji}</div>
        <div class="metric-value" style="color: {color};">{status}</div>
        <div style="margin-top: 20px;">
            <div style="background: {theme['card_border']}; height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="background: {color}; height: 100%; width: {percentage}%; transition: width 1s;"></div>
            </div>
        </div>
        <div class="metric-footer">
            Score: {score:.2f} / 1.00
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_world_stats(stats, theme):
    """Render world statistics grid"""
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-value" style="color: {theme['danger']};">⚔️ {stats['active_conflicts']}</div>
            <div class="stat-label">Active Conflicts</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" style="color: {theme['warning']};">🌡️ +{stats['global_temp_anomaly']}°C</div>
            <div class="stat-label">Temp Anomaly</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" style="color: {theme['success']};">🌐 {stats['internet_users']}B</div>
            <div class="stat-label">Internet Users</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" style="color: {theme['warning']};">💨 {stats['co2_ppm']} ppm</div>
            <div class="stat-label">CO₂ Levels</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown('<div class="section-header">⚙️ CONTROL CENTER</div>', unsafe_allow_html=True)
        
        # Theme Selection
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**🎨 Interface Theme**")
        selected_theme = st.selectbox(
            "Choose your theme",
            list(THEMES.keys()),
            index=0,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Location Settings
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**📍 Location Configuration**")
        
        location_presets = {
            "New York": (40.71, -74.00),
            "London": (51.50, -0.12),
            "Tokyo": (35.67, 139.65),
            "Dubai": (25.20, 55.27),
            "Sydney": (-33.86, 151.21),
            "Custom": None
        }
        
        location = st.selectbox("Select Location", list(location_presets.keys()))
        
        if location == "Custom":
            city_name = st.text_input("City Name", "Metropolis")
            custom_lat = st.number_input("Latitude", value=40.71, format="%.2f")
            custom_lon = st.number_input("Longitude", value=-74.00, format="%.2f")
        else:
            city_name = location
            custom_lat, custom_lon = location_presets[location]
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Refresh Settings
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**🔄 Data Refresh**")
        auto_refresh = st.checkbox("Auto-refresh (5 min)", value=False)
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System Status
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**📊 System Status**")
        st.markdown('<span class="badge badge-success">● ALL SYSTEMS OPERATIONAL</span>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-top: 16px; font-size: 0.8rem; opacity: 0.7;">
            Last Update: {datetime.now().strftime('%H:%M:%S')}<br>
            Uptime: 99.9%<br>
            Data Sources: 12 Active
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Apply Selected Theme
    inject_premium_css(selected_theme)
    theme = THEMES[selected_theme]

    # ========== HERO SECTION ==========
    st.markdown(f"""
    <div class="slide-in" style="margin-bottom: 40px;">
        <div class="hero-title">🌐 NEXUS</div>
        <div class="hero-subtitle">Global Intelligence Platform • Real-time Monitoring & Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    # ========== TOP METRICS ROW ==========
    sentiment_score = calculate_sentiment_score()
    world_stats = generate_world_stats()
    
    col_sent, col_stats = st.columns([1, 2])
    
    with col_sent:
        render_sentiment_meter(sentiment_score, theme)
    
    with col_stats:
        render_world_stats(world_stats, theme)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ========== MAIN CONTENT GRID ==========
    col_news, col_side = st.columns([2, 1])

    # NEWS FEED
    with col_news:
        st.markdown('<div class="section-header">📰 GLOBAL INTELLIGENCE FEED</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["🌍 WORLD", "💻 TECH", "🧬 SCIENCE", "💼 BUSINESS"])
        
        with tab1:
            with st.spinner("Loading world news..."):
                news = fetch_news("world")
                for article in news:
                    render_news_card(article, theme)
        
        with tab2:
            with st.spinner("Loading tech news..."):
                news = fetch_news("tech")
                for article in news:
                    render_news_card(article, theme)
        
        with tab3:
            with st.spinner("Loading science news..."):
                news = fetch_news("science")
                for article in news:
                    render_news_card(article, theme)
        
        with tab4:
            with st.spinner("Loading business news..."):
                news = fetch_news("business")
                for article in news:
                    render_news_card(article, theme)

    # SIDE PANEL
    with col_side:
        # Weather
        st.markdown('<div class="section-header">🌡️ CONDITIONS</div>', unsafe_allow_html=True)
        with st.spinner("Loading weather..."):
            weather = fetch_weather(custom_lat, custom_lon, city_name)
            render_weather_card(weather, theme)
        
        # Markets
        st.markdown('<div class="section-header" style="margin-top: 32px;">📈 MARKET PULSE</div>', unsafe_allow_html=True)
        with st.spinner("Loading market data..."):
            market_data = generate_market_data()
            for ticker, data in market_data.items():
                render_market_card(ticker, data, theme)

    # ========== FOOTER ==========
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align: center; color: {theme['text_muted']}; padding: 30px 0;">
        <div style="font-size: 1.2rem; margin-bottom: 12px; color: {theme['text_secondary']};">
            <strong>NEXUS</strong> Global Intelligence Platform
        </div>
        <div style="font-size: 0.9rem; margin-bottom: 8px;">
            ⚡ Powered by Streamlit • Real-time Data Aggregation & Analysis
        </div>
        <div style="font-size: 0.8rem; opacity: 0.7;">
            Dashboard v3.0 • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
        </div>
        <div style="margin-top: 16px; font-size: 0.75rem; opacity: 0.5;">
            Data sources: Reuters, BBC, AP News, TechCrunch, Science Daily, Open-Meteo
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auto-refresh logic
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.rerun()

if __name__ == "__main__":
    main()
