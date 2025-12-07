import streamlit as st
import feedparser
import requests
import pandas as pd
import plotly.graph_objects as go
import random
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIGURATION & SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="World Situation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# THEME ENGINE
# -----------------------------------------------------------------------------
THEMES = {
    "Midnight Matrix": {
        "bg_gradient": "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        "card_bg": "rgba(10, 25, 40, 0.75)",
        "text": "#e8f6f5",
        "accent": "#7CFC00",
        "font": "sans-serif"
    },
    "Serene Dawn": {
        "bg_gradient": "linear-gradient(135deg, #fce38a, #f38181)",
        "card_bg": "rgba(255, 255, 255, 0.85)",
        "text": "#3a3a3a",
        "accent": "#f38181",
        "font": "sans-serif"
    },
    "Retro Terminal": {
        "bg_gradient": "linear-gradient(135deg, #0b1b0b, #183018)",
        "card_bg": "rgba(0, 20, 0, 0.9)",
        "text": "#33ff33",
        "accent": "#33ff33",
        "font": "monospace"
    },
    "Sahara Sunset": {
        "bg_gradient": "linear-gradient(135deg, #FFD194, #D1913C, #F6D365)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "text": "#4d3e2f",
        "accent": "#D1913C",
        "font": "sans-serif"
    }
}

def inject_custom_css(theme_name):
    theme = THEMES[theme_name]
    
    css = f"""
    <style>
        /* Global App Styling */
        .stApp {{
            background: {theme['bg_gradient']};
            background-attachment: fixed;
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            font-family: {theme['font']};
            color: {theme['text']};
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* Card/Widget Styling */
        .css-1r6slb0, .css-12w0qpk, .stColumn {{
            background-color: transparent;
        }}
        
        .custom-card {{
            background: {theme['card_bg']};
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            transition: transform 0.3s ease;
            color: {theme['text']};
        }}
        
        .custom-card:hover {{
            transform: translateY(-5px);
        }}

        /* Text Highlights */
        h1, h2, h3 {{
            color: {theme['text']} !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .accent-text {{
            color: {theme['accent']};
            font-weight: bold;
        }}
        
        a {{
            color: {theme['accent']} !important;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Streamlit UI overrides */
        .stButton>button {{
            background-color: {theme['accent']};
            color: #000;
            border: none;
            font-weight: bold;
        }}
        
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA FETCHING FUNCTIONS (Cached)
# -----------------------------------------------------------------------------

@st.cache_data(ttl=300)  # Cache news for 5 minutes
def fetch_news(category="world"):
    feeds = {
        "world": [
            "https://feeds.reuters.com/Reuters/worldNews",
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.apnews.com/AP-Top-News"
        ],
        "tech": [
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.theverge.com/rss/index.xml"
        ],
        "science": [
            "https://www.sciencedaily.com/rss/top/science.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml"
        ]
    }
    
    articles = []
    selected_feeds = feeds.get(category, feeds["world"])
    
    for url in selected_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:  # Top 3 from each
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Just now"),
                    "source": feed.feed.get("title", "Unknown Source"),
                    "summary": entry.get("summary", "")[:150] + "..."
                })
        except Exception:
            continue
            
    random.shuffle(articles) # Mix them up
    return articles[:10]

@st.cache_data(ttl=900) # Cache weather for 15 mins
def fetch_weather(lat, lon, city_name):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        current = data.get("current_weather", {})
        
        # Map wmo codes to emojis
        wcode = current.get("weathercode", 0)
        icon = "☀️"
        if wcode > 2: icon = "⛅"
        if wcode > 45: icon = "🌫️"
        if wcode > 50: icon = "🌧️"
        if wcode > 70: icon = "❄️"
        if wcode > 95: icon = "⛈️"
        
        return {
            "temp": current.get("temperature"),
            "speed": current.get("windspeed"),
            "icon": icon,
            "city": city_name
        }
    except:
        return {"temp": "--", "speed": "--", "icon": "❓", "city": city_name}

def generate_market_data():
    # Simulate a market random walk for sparklines
    tickers = ["S&P 500", "NASDAQ", "BTC-USD", "GOLD"]
    data = {}
    
    for ticker in tickers:
        base_price = random.uniform(1000, 50000)
        volatility = base_price * 0.02
        prices = [base_price]
        for _ in range(20):
            change = random.uniform(-volatility, volatility)
            prices.append(prices[-1] + change)
        
        change_pct = ((prices[-1] - prices[0]) / prices[0]) * 100
        data[ticker] = {
            "history": prices,
            "current": prices[-1],
            "change": change_pct
        }
    return data

# -----------------------------------------------------------------------------
# LAYOUT & COMPONENTS
# -----------------------------------------------------------------------------

def render_news_card(article, theme_accent):
    st.markdown(f"""
    <div class="custom-card">
        <div style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 5px;">
            {article['source']} • {article['published'][:16]}
        </div>
        <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 10px; line-height: 1.4;">
            <a href="{article['link']}" target="_blank">{article['title']}</a>
        </div>
        <div style="font-size: 0.9rem; opacity: 0.9;">
            {article['summary']}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_weather_widget(weather_data):
    st.markdown(f"""
    <div class="custom-card" style="text-align: center;">
        <h3 style="margin-top:0;">{weather_data['city']}</h3>
        <div style="font-size: 4rem; margin: 10px 0;">{weather_data['icon']}</div>
        <div style="font-size: 2.5rem; font-weight: 900;">{weather_data['temp']}°C</div>
        <div style="opacity: 0.7;">Wind: {weather_data['speed']} km/h</div>
    </div>
    """, unsafe_allow_html=True)

def render_market_sparkline(name, data, theme_accent):
    color = "#00ff00" if data['change'] >= 0 else "#ff0000"
    
    fig = go.Figure(data=go.Scatter(
        y=data['history'],
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f"rgba({(0 if data['change'] < 0 else 0)}, {(255 if data['change'] >= 0 else 0)}, 0, 0.1)"
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    
    st.markdown(f"""
    <div class="custom-card" style="padding: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
            <span style="font-weight: bold;">{name}</span>
            <span style="color: {color}; font-weight: bold; font-family: monospace;">
                {data['change']:.2f}%
            </span>
        </div>
        <div style="font-size: 1.2rem; font-weight: 900; margin-bottom: 5px;">
            {data['current']:.2f}
        </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN APP LOOP
# -----------------------------------------------------------------------------

def main():
    # Sidebar Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        selected_theme = st.selectbox("Theme", list(THEMES.keys()), index=0)
        
        st.subheader("📍 Location")
        location_option = st.selectbox("Region", ["North America", "Europe", "Asia", "Custom"])
        
        custom_lat = 40.71
        custom_lon = -74.00
        city_name = "New York"
        
        if location_option == "Europe":
            custom_lat, custom_lon, city_name = 51.50, -0.12, "London"
        elif location_option == "Asia":
            custom_lat, custom_lon, city_name = 35.67, 139.65, "Tokyo"
        elif location_option == "Custom":
            city_name = st.text_input("City Name", "Metropolis")
            custom_lat = st.number_input("Lat", value=40.71)
            custom_lon = st.number_input("Lon", value=-74.00)

        st.divider()
        st.info("Data refreshed automatically on interaction.")

    # Inject CSS
    inject_custom_css(selected_theme)
    theme_accent = THEMES[selected_theme]['accent']

    # Header
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"""
        <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🌍 World Situation</h1>
        <p style='opacity: 0.7; font-size: 1.2rem;'>Things are getting weird.</p>
        """, unsafe_allow_html=True)
    with col_h2:
        # Chaos Meter
        chaos_level = random.choice(["Tranquil ✨", "Spicy 🌶️", "Weird 🌪️", "Doomed 💀"])
        st.markdown(f"""
        <div class="custom-card" style="text-align: center; padding: 10px;">
            <small>GLOBAL CHAOS LEVEL</small>
            <h2 style="color: {theme_accent}; margin: 0;">{chaos_level}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Main Grid
    col1, col2, col3 = st.columns([2, 1, 1])

    # COLUMN 1: NEWS FEED
    with col1:
        st.subheader("📰 Global Feed")
        
        # Category Tabs
        tab1, tab2, tab3 = st.tabs(["🌍 World", "💻 Tech", "🧬 Science"])
        
        with tab1:
            news = fetch_news("world")
            for article in news:
                render_news_card(article, theme_accent)
        with tab2:
            news = fetch_news("tech")
            for article in news:
                render_news_card(article, theme_accent)
        with tab3:
            news = fetch_news("science")
            for article in news:
                render_news_card(article, theme_accent)

    # COLUMN 2: LOCAL INTEL & WEATHER
    with col2:
        st.subheader("📡 Local Intel")
        
        # Weather
        weather = fetch_weather(custom_lat, custom_lon, city_name)
        render_weather_widget(weather)
        
        # Local Status (Satirical)
        st.markdown(f"""
        <div class="custom-card">
            <h4 style="margin-top:0;">Status Report</h4>
            <p><strong>AI Sentience:</strong> <span style="color: {theme_accent}">Debatable</span></p>
            <p><strong>Coffee Supply:</strong> <span style="color: green">Stable</span></p>
            <p><strong>Aliens:</strong> Not currently detected</p>
            <hr style="border-color: rgba(255,255,255,0.1)">
            <small style="opacity: 0.6">Lat: {custom_lat} | Lon: {custom_lon}</small>
        </div>
        """, unsafe_allow_html=True)

    # COLUMN 3: MARKETS
    with col3:
        st.subheader("📈 Markets")
        market_data = generate_market_data()
        for ticker, data in market_data.items():
            render_market_sparkline(ticker, data, theme_accent)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; opacity: 0.5; font-size: 0.8rem;">
        Dashboard updated: {datetime.now().strftime('%H:%M:%S')} | Powered by Streamlit & Coffee
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
