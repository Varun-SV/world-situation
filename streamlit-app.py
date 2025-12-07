import streamlit as st
import feedparser
import requests
import pandas as pd
import plotly.graph_objects as go
import random
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pulse • World Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ENHANCED THEME ENGINE
# -----------------------------------------------------------------------------
THEMES = {
    "Aurora Night": {
        "bg_gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "card_bg": "rgba(255, 255, 255, 0.05)",
        "card_border": "rgba(94, 217, 217, 0.3)",
        "text": "#e8f1f5",
        "text_secondary": "#a0b8c7",
        "accent": "#5ed9d9",
        "accent_glow": "rgba(94, 217, 217, 0.4)",
        "success": "#4ade80",
        "danger": "#f87171",
        "warning": "#fbbf24",
        "font": "'Inter', 'Segoe UI', system-ui, sans-serif"
    },
    "Cyber Neon": {
        "bg_gradient": "linear-gradient(135deg, #0a0e27 0%, #1a1a40 50%, #2d2d5f 100%)",
        "card_bg": "rgba(138, 43, 226, 0.08)",
        "card_border": "rgba(138, 43, 226, 0.5)",
        "text": "#f0f0ff",
        "text_secondary": "#b8b8d4",
        "accent": "#9d4edd",
        "accent_glow": "rgba(157, 78, 221, 0.6)",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "font": "'Roboto Mono', 'Courier New', monospace"
    },
    "Solar Flare": {
        "bg_gradient": "linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 50%, #3d3d3d 100%)",
        "card_bg": "rgba(251, 146, 60, 0.08)",
        "card_border": "rgba(251, 146, 60, 0.4)",
        "text": "#fef3c7",
        "text_secondary": "#d4c5a0",
        "accent": "#fb923c",
        "accent_glow": "rgba(251, 146, 60, 0.5)",
        "success": "#34d399",
        "danger": "#f87171",
        "warning": "#fbbf24",
        "font": "'Inter', 'Segoe UI', system-ui, sans-serif"
    },
    "Ocean Deep": {
        "bg_gradient": "linear-gradient(135deg, #001f3f 0%, #003d5c 50%, #006494 100%)",
        "card_bg": "rgba(255, 255, 255, 0.06)",
        "card_border": "rgba(0, 191, 255, 0.3)",
        "text": "#e0f2fe",
        "text_secondary": "#b3d9ef",
        "accent": "#00bfff",
        "accent_glow": "rgba(0, 191, 255, 0.4)",
        "success": "#10b981",
        "danger": "#f43f5e",
        "warning": "#f59e0b",
        "font": "'Inter', 'Segoe UI', system-ui, sans-serif"
    }
}

def inject_modern_css(theme_name):
    theme = THEMES[theme_name]
    
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Roboto+Mono:wght@400;700&display=swap');
        
        /* Global Styling */
        .stApp {{
            background: {theme['bg_gradient']};
            background-attachment: fixed;
            font-family: {theme['font']};
            color: {theme['text']};
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Glass Morphism Cards */
        .glass-card {{
            background: {theme['card_bg']};
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid {theme['card_border']};
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .glass-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, {theme['accent']}, transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .glass-card:hover {{
            transform: translateY(-4px);
            border-color: {theme['accent']};
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4), 0 0 0 1px {theme['accent_glow']};
        }}
        
        .glass-card:hover::before {{
            opacity: 1;
        }}
        
        /* News Card */
        .news-card {{
            background: {theme['card_bg']};
            backdrop-filter: blur(20px);
            border: 1px solid {theme['card_border']};
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .news-card::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: {theme['accent']};
            transform: translateX(-4px);
            transition: transform 0.3s;
        }}
        
        .news-card:hover {{
            border-color: {theme['accent']};
            transform: translateX(4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }}
        
        .news-card:hover::after {{
            transform: translateX(0);
        }}
        
        .news-source {{
            font-size: 0.75rem;
            color: {theme['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .news-title {{
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 12px;
            line-height: 1.5;
            color: {theme['text']};
        }}
        
        .news-title a {{
            color: {theme['text']};
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .news-title a:hover {{
            color: {theme['accent']};
        }}
        
        .news-summary {{
            font-size: 0.9rem;
            color: {theme['text_secondary']};
            line-height: 1.6;
        }}
        
        /* Metric Cards */
        .metric-card {{
            background: {theme['card_bg']};
            backdrop-filter: blur(20px);
            border: 1px solid {theme['card_border']};
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
            position: relative;
        }}
        
        .metric-card:hover {{
            border-color: {theme['accent']};
            box-shadow: 0 0 30px {theme['accent_glow']};
        }}
        
        .metric-value {{
            font-size: 3rem;
            font-weight: 900;
            color: {theme['accent']};
            margin: 16px 0;
            text-shadow: 0 0 20px {theme['accent_glow']};
        }}
        
        .metric-label {{
            font-size: 0.85rem;
            color: {theme['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
        }}
        
        /* Headers */
        h1, h2, h3, h4 {{
            color: {theme['text']} !important;
            font-weight: 800 !important;
        }}
        
        h1 {{
            font-size: 3.5rem !important;
            margin-bottom: 0 !important;
            background: linear-gradient(135deg, {theme['text']}, {theme['accent']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .section-header {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {theme['accent']};
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-header::before {{
            content: '';
            width: 4px;
            height: 24px;
            background: {theme['accent']};
            border-radius: 2px;
        }}
        
        /* Status Badges */
        .status-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            color: {theme['accent']};
            backdrop-filter: blur(10px);
        }}
        
        .badge-success {{ 
            color: {theme['success']}; 
            border-color: {theme['success']};
            box-shadow: 0 0 15px rgba(74, 222, 128, 0.2);
        }}
        
        .badge-danger {{ 
            color: {theme['danger']}; 
            border-color: {theme['danger']};
            box-shadow: 0 0 15px rgba(248, 113, 113, 0.2);
        }}
        
        .badge-warning {{ 
            color: {theme['warning']}; 
            border-color: {theme['warning']};
            box-shadow: 0 0 15px rgba(251, 191, 36, 0.2);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: {theme['card_bg']};
            padding: 8px;
            border-radius: 12px;
            backdrop-filter: blur(20px);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border-radius: 8px;
            color: {theme['text_secondary']};
            font-weight: 600;
            padding: 12px 24px;
            border: 1px solid transparent;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {theme['accent']} !important;
            color: #000 !important;
            box-shadow: 0 0 20px {theme['accent_glow']};
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: {theme['bg_gradient']};
            border-right: 1px solid {theme['card_border']};
        }}
        
        [data-testid="stSidebar"] .glass-card {{
            background: {theme['card_bg']};
            backdrop-filter: blur(10px);
        }}
        
        /* Animations */
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}
        
        .pulse {{
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.2);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {theme['accent']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {theme['accent_glow']};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA FETCHING
# -----------------------------------------------------------------------------

@st.cache_data(ttl=300)
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
            for entry in feed.entries[:3]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Just now"),
                    "source": feed.feed.get("title", "Unknown Source"),
                    "summary": entry.get("summary", "")[:150] + "..."
                })
        except:
            continue
            
    random.shuffle(articles)
    return articles[:10]

@st.cache_data(ttl=900)
def fetch_weather(lat, lon, city_name):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        current = data.get("current_weather", {})
        
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
# MODERN COMPONENTS
# -----------------------------------------------------------------------------

def render_news_card(article, theme):
    st.markdown(f"""
    <div class="news-card">
        <div class="news-source">
            <span>📡</span>
            <span>{article['source']}</span>
            <span style="margin-left: auto; opacity: 0.6;">•</span>
            <span style="opacity: 0.6;">{article['published'][:16]}</span>
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
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div class="metric-label">CURRENT CONDITIONS</div>
        <div style="font-size: 5rem; margin: 20px 0;">{weather['icon']}</div>
        <div class="metric-value">{weather['temp']}°</div>
        <h3 style="margin: 12px 0; font-size: 1.5rem;">{weather['city']}</h3>
        <div style="color: {theme['text_secondary']}; margin-top: 16px; display: flex; justify-content: center; gap: 20px;">
            <div>💨 {weather['speed']} km/h</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_market_card(name, data, theme):
    color = theme['success'] if data['change'] >= 0 else theme['danger']
    arrow = "↗" if data['change'] >= 0 else "↘"
    
    # Convert hex to rgba for fill
    if data['change'] >= 0:
        fill_color = 'rgba(74, 222, 128, 0.1)'  # success with opacity
    else:
        fill_color = 'rgba(248, 113, 113, 0.1)'  # danger with opacity
    
    fig = go.Figure(data=go.Scatter(
        y=data['history'],
        mode='lines',
        line=dict(color=color, width=3),
        fill='tozeroy',
        fillcolor=fill_color
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=60,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        hovermode=False
    )
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-weight: 700; font-size: 0.95rem; color: {theme['text_secondary']};">{name}</span>
            <span class="status-badge" style="color: {color}; border-color: {color};">
                {arrow} {abs(data['change']):.2f}%
            </span>
        </div>
        <div style="font-size: 1.8rem; font-weight: 900; color: {theme['text']}; margin-bottom: 12px;">
            ${data['current']:,.2f}
        </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN APP
# -----------------------------------------------------------------------------

def main():
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="section-header">⚙️ CONTROL PANEL</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        selected_theme = st.selectbox("🎨 Theme", list(THEMES.keys()), index=0)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**📍 Location Settings**")
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
            custom_lat = st.number_input("Latitude", value=40.71)
            custom_lon = st.number_input("Longitude", value=-74.00)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**ℹ️ System Status**")
        st.markdown('<span class="status-badge badge-success">● ONLINE</span>', unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top: 12px; font-size: 0.8rem; opacity: 0.6;'>Last Update: {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Apply theme
    inject_modern_css(selected_theme)
    theme = THEMES[selected_theme]

    # Hero Section
    st.markdown(f"""
    <div style="margin-bottom: 40px;">
        <h1>🌐 PULSE</h1>
        <p style="font-size: 1.2rem; color: {theme['text_secondary']}; margin-top: 8px;">
            Real-time global intelligence dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chaos Meter
    chaos_options = [
        ("Tranquil", "✨", theme['success']),
        ("Active", "🌶️", theme['warning']),
        ("Volatile", "🌪️", theme['warning']),
        ("Critical", "💀", theme['danger'])
    ]
    chaos_label, chaos_icon, chaos_color = random.choice(chaos_options)
    
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 30px; margin-bottom: 30px;">
        <div class="metric-label">GLOBAL SITUATION INDEX</div>
        <div style="font-size: 4rem; margin: 20px 0;">{chaos_icon}</div>
        <div style="font-size: 2.5rem; font-weight: 900; color: {chaos_color}; text-shadow: 0 0 30px {chaos_color}50;">
            {chaos_label.upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Content Grid
    col1, col2 = st.columns([2, 1])

    # Left Column: News Feed
    with col1:
        st.markdown('<div class="section-header">📰 LIVE FEED</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🌍 World", "💻 Tech", "🧬 Science"])
        
        with tab1:
            news = fetch_news("world")
            for article in news:
                render_news_card(article, theme)
        
        with tab2:
            news = fetch_news("tech")
            for article in news:
                render_news_card(article, theme)
        
        with tab3:
            news = fetch_news("science")
            for article in news:
                render_news_card(article, theme)

    # Right Column: Metrics
    with col2:
        st.markdown('<div class="section-header">🌡️ LOCAL CONDITIONS</div>', unsafe_allow_html=True)
        weather = fetch_weather(custom_lat, custom_lon, city_name)
        render_weather_card(weather, theme)
        
        st.markdown('<div class="section-header" style="margin-top: 30px;">📈 MARKET PULSE</div>', unsafe_allow_html=True)
        market_data = generate_market_data()
        for ticker, data in market_data.items():
            render_market_card(ticker, data, theme)
        
        # System Info
        st.markdown(f"""
        <div class="glass-card" style="margin-top: 20px;">
            <div class="metric-label" style="margin-bottom: 16px;">DIAGNOSTICS</div>
            <div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.9rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: {theme['text_secondary']};">AI Status</span>
                    <span class="status-badge badge-warning">Aware</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: {theme['text_secondary']};">Data Streams</span>
                    <span class="status-badge badge-success">Active</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: {theme['text_secondary']};">Threats</span>
                    <span class="status-badge">None Detected</span>
                </div>
            </div>
            <div style="margin-top: 20px; padding-top: 16px; border-top: 1px solid {theme['card_border']}; font-size: 0.75rem; color: {theme['text_secondary']};">
                📍 {custom_lat}, {custom_lon}<br>
                🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {theme['text_secondary']}; font-size: 0.85rem; padding: 20px 0;">
        <div style="margin-bottom: 8px;">⚡ Powered by Streamlit • Real-time data aggregation</div>
        <div style="opacity: 0.6;">Dashboard v2.0 • Updated {datetime.now().strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
