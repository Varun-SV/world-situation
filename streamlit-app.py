import streamlit as st
import feedparser
import requests
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="World Situation Command Center",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# THEMES & STYLING
# -----------------------------------------------------------------------------
THEMES = {
    "Neo Noir": {
        "bg": "#050814",
        "accent": "#ff4c8b",
        "accent_soft": "rgba(255, 76, 139, 0.18)",
        "card_bg": "rgba(9, 12, 30, 0.95)",
        "border": "rgba(255, 255, 255, 0.06)",
        "text": "#f5f5ff",
        "muted": "#9ca3af",
        "font": "system-ui, -apple-system, BlinkMacSystemFont, 'SF Pro', sans-serif",
    },
    "Daylight": {
        "bg": "#f5f7fb",
        "accent": "#2563eb",
        "accent_soft": "rgba(37, 99, 235, 0.08)",
        "card_bg": "rgba(255, 255, 255, 0.96)",
        "border": "rgba(15, 23, 42, 0.06)",
        "text": "#020617",
        "muted": "#6b7280",
        "font": "system-ui, -apple-system, BlinkMacSystemFont, 'SF Pro', sans-serif",
    },
    "Retro Green": {
        "bg": "#020712",
        "accent": "#22c55e",
        "accent_soft": "rgba(34, 197, 94, 0.12)",
        "card_bg": "rgba(3, 10, 20, 0.96)",
        "border": "rgba(34, 197, 94, 0.25)",
        "text": "#e5ffe9",
        "muted": "#86efac",
        "font": "'JetBrains Mono', Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
    },
}


def inject_base_css(theme_name: str):
    theme = THEMES[theme_name]
    css = f"""
    <style>
        .stApp {{
            background: radial-gradient(circle at top left, rgba(148, 163, 184, 0.16), transparent 55%),
                        radial-gradient(circle at bottom right, rgba(148, 163, 184, 0.12), transparent 55%),
                        {theme['bg']};
            color: {theme['text']};
            font-family: {theme['font']};
        }}

        /* Remove default Streamlit padding to get edge-to-edge sections */
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.5rem;
        }}

        .ws-shell {{
            padding: 0.8rem 0.8rem 2.5rem 0.8rem;
        }}

        .ws-topbar {{
            border-radius: 18px;
            padding: 1.2rem 1.6rem;
            background: linear-gradient(120deg, {theme['card_bg']}, rgba(15,23,42,0.92));
            border: 1px solid {theme['border']};
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
            position: sticky;
            top: 0.4rem;
            z-index: 10;
            backdrop-filter: blur(18px);
        }}

        .ws-title {{
            font-size: 1.9rem;
            font-weight: 700;
            letter-spacing: 0.03em;
        }}

        .ws-subtitle {{
            font-size: 0.9rem;
            color: {theme['muted']};
        }}

        .ws-chip-row {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 0.55rem;
        }}

        .ws-chip {{
            border-radius: 999px;
            border: 1px solid {theme['border']};
            padding: 0.15rem 0.8rem;
            font-size: 0.78rem;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            background: rgba(15,23,42,0.75);
        }}

        .ws-chip-dot {{
            width: 0.48rem;
            height: 0.48rem;
            border-radius: 999px;
            background: {theme['accent']};
            box-shadow: 0 0 8px {theme['accent']};
        }}

        .ws-metric-card {{
            border-radius: 18px;
            padding: 1rem 1.1rem;
            background: {theme['card_bg']};
            border: 1px solid {theme['border']};
            box-shadow: 0 14px 40px rgba(0,0,0,0.35);
            position: relative;
            overflow: hidden;
        }}

        .ws-metric-label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: {theme['muted']};
            margin-bottom: 0.25rem;
        }}

        .ws-metric-value {{
            font-size: 1.4rem;
            font-weight: 700;
        }}

        .ws-metric-pill {{
            font-size: 0.75rem;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            border: 1px solid {theme['border']};
            background: {theme['accent_soft']};
        }}

        .ws-chaos-ring {{
            width: 110px;
            height: 110px;
            border-radius: 999px;
            border: 2px dashed {theme['accent']};
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}

        .ws-chaos-core {{
            width: 78px;
            height: 78px;
            border-radius: 999px;
            background: radial-gradient(circle at top, {theme['accent']}, transparent 60%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            text-align: center;
            padding: 0.3rem;
            color: #020617;
            font-weight: 700;
        }}

        .ws-section-title {{
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {theme['muted']};
            margin-bottom: 0.4rem;
        }}

        .ws-card {{
            border-radius: 18px;
            padding: 0.9rem 1rem;
            background: {theme['card_bg']};
            border: 1px solid {theme['border']};
            box-shadow: 0 12px 34px rgba(0,0,0,0.32);
        }}

        .ws-news-item {{
            padding: 0.55rem 0.4rem 0.6rem 0.4rem;
            border-radius: 12px;
            border: 1px solid transparent;
            transition: background 0.15s ease, border 0.15s ease, transform 0.08s ease;
        }}
        .ws-news-item:hover {{
            background: {theme['accent_soft']};
            border-color: {theme['accent']};
            transform: translateY(-1px);
        }}

        .ws-news-source {{
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: {theme['muted']};
        }}

        .ws-news-title {{
            font-size: 0.95rem;
            font-weight: 600;
            margin-top: 0.15rem;
            margin-bottom: 0.15rem;
        }}

        .ws-news-meta {{
            font-size: 0.75rem;
            color: {theme['muted']};
        }}

        .ws-soft {{ color: {theme['muted']}; }}

        .ws-badge-accent {{
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.2rem 0.55rem;
            border-radius: 999px;
            background: {theme['accent_soft']};
            font-size: 0.7rem;
        }}

        .ws-footer {{
            font-size: 0.78rem;
            color: {theme['muted']};
            text-align: center;
            margin-top: 1.8rem;
        }}

        .ws-footer span {{ color: {theme['accent']}; }}

        /* Clean up default buttons */
        .stButton>button {{
            border-radius: 999px;
            border: 1px solid {theme['border']};
            background: {theme['accent_soft']};
            color: {theme['text']};
            font-size: 0.8rem;
            padding: 0.3rem 0.9rem;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DATA FETCHING (CACHED)
# -----------------------------------------------------------------------------

@st.cache_data(ttl=300)
def fetch_news(category="world"):
    feeds = {
        "world": [
            "https://feeds.reuters.com/Reuters/worldNews",
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.apnews.com/AP-Top-News",
        ],
        "tech": [
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.theverge.com/rss/index.xml",
        ],
        "science": [
            "https://www.sciencedaily.com/rss/top/science.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
        ],
    }

    articles = []
    selected_feeds = feeds.get(category, feeds["world"])

    for url in selected_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]:
                articles.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", "Just now"),
                        "source": feed.feed.get("title", "Unknown Source"),
                        "summary": entry.get("summary", "")[:180] + "...",
                    }
                )
        except Exception:
            continue

    random.shuffle(articles)
    return articles[:15]


@st.cache_data(ttl=900)
def fetch_weather(lat, lon, city_name):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        current = data.get("current_weather", {})

        wcode = current.get("weathercode", 0)
        icon = "☀️"
        label = "Clear"
        if wcode > 2:
            icon, label = "⛅", "Cloudy"
        if wcode > 45:
            icon, label = "🌫️", "Foggy"
        if wcode > 50:
            icon, label = "🌧️", "Rain"
        if wcode > 70:
            icon, label = "❄️", "Snow"
        if wcode > 95:
            icon, label = "⛈️", "Storm"

        return {
            "temp": current.get("temperature"),
            "speed": current.get("windspeed"),
            "icon": icon,
            "label": label,
            "city": city_name,
        }
    except Exception:
        return {"temp": "--", "speed": "--", "icon": "❓", "label": "Unknown", "city": city_name}


def generate_market_data():
    tickers = ["S&P 500", "NASDAQ", "BTC-USD", "GOLD"]
    data = {}

    for ticker in tickers:
        base_price = random.uniform(1000, 50000)
        volatility = base_price * 0.02
        prices = [base_price]
        for _ in range(32):
            change = random.uniform(-volatility, volatility)
            prices.append(prices[-1] + change)

        change_pct = ((prices[-1] - prices[0]) / prices[0]) * 100
        data[ticker] = {
            "history": prices,
            "current": prices[-1],
            "change": change_pct,
        }
    return data


# -----------------------------------------------------------------------------
# RENDER HELPERS
# -----------------------------------------------------------------------------

def render_news_stream(articles):
    for article in articles:
        st.markdown(
            f"""
            <div class="ws-news-item">
                <div class="ws-news-source">{article['source']} · {article['published'][:16]}</div>
                <div class="ws-news-title">
                    <a href="{article['link']}" target="_blank">{article['title']}</a>
                </div>
                <div class="ws-news-meta">{article['summary']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_weather_block(weather):
    st.markdown(
        f"""
        <div class="ws-metric-card">
            <div class="ws-metric-label">Local Atmosphere</div>
            <div style="display:flex; align-items:center; justify-content:space-between; gap:0.9rem;">
                <div>
                    <div style="font-size:0.9rem;" class="ws-soft">{weather['city']}</div>
                    <div class="ws-metric-value">{weather['temp']}°C {weather['icon']}</div>
                    <div class="ws-soft" style="margin-top:0.2rem; font-size:0.8rem;">
                        {weather['label']} · Wind {weather['speed']} km/h
                    </div>
                </div>
                <div class="ws-metric-pill">Weather feed: live pull</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_market_widget(name, data):
    color = "#22c55e" if data["change"] >= 0 else "#ef4444"
    fill_alpha = "0.16" if data["change"] >= 0 else "0.12"

    rgba_fill = (
        f"rgba(34, 197, 94, {fill_alpha})" if data["change"] >= 0 else f"rgba(248, 113, 113, {fill_alpha})"
    )

    fig = go.Figure(
        data=go.Scatter(
            y=data["history"],
            mode="lines",
            line=dict(width=2),
            fill="tozeroy",
            fillcolor=rgba_fill,
        )
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=70,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    st.markdown(
        f"""
        <div class="ws-card" style="padding:0.7rem 0.8rem 0.3rem 0.8rem; margin-bottom:0.45rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:0.85rem; font-weight:600;">{name}</div>
                <div style="font-size:0.85rem; font-weight:600; color:{color};">
                    {data['change']:.2f}%
                </div>
            </div>
            <div style="font-size:0.78rem; margin-top:0.15rem;" class="ws-soft">
                Spot ~ {data['current']:.2f}
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MAIN APP
# -----------------------------------------------------------------------------

def main():
    # SIDEBAR: CONTROL PANEL
    with st.sidebar:
        st.markdown("### 🧭 Control Panel")

        theme_choice = st.radio("Visual theme", list(THEMES.keys()), index=0)

        st.markdown("---")
        st.markdown("#### 📍 Focus Region")
        location_option = st.selectbox("Preset regions", ["North America", "Europe", "Asia", "Custom"])

        lat, lon, city_name = 40.71, -74.00, "New York"
        if location_option == "Europe":
            lat, lon, city_name = 51.50, -0.12, "London"
        elif location_option == "Asia":
            lat, lon, city_name = 35.67, 139.65, "Tokyo"
        elif location_option == "Custom":
            city_name = st.text_input("City name", "Metropolis")
            lat = st.number_input("Latitude", value=40.71)
            lon = st.number_input("Longitude", value=-74.00)

        st.markdown("---")
        st.markdown("#### 📰 News Streams")
        enabled_streams = st.multiselect(
            "Activate feeds", ["World", "Tech", "Science"], default=["World", "Tech"]
        )

        st.markdown("---")
        st.caption("Data refreshes on interaction. This is a read-only dashboard — no panic buttons.")

    # Apply theme
    inject_base_css(theme_choice)
    theme = THEMES[theme_choice]

    # Top shell layout
    st.markdown('<div class="ws-shell">', unsafe_allow_html=True)

    # TOPBAR / HEADER
    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.markdown(
            f"""
            <div class="ws-topbar">
                <div style="display:flex; justify-content:space-between; gap:1.5rem; align-items:flex-start;">
                    <div>
                        <div class="ws-title">World Situation · Command Center</div>
                        <div class="ws-subtitle">High-level signal from world news, markets, and your local weather feed.</div>
                        <div class="ws-chip-row">
                            <div class="ws-chip">
                                <div class="ws-chip-dot"></div>
                                Live snapshot · {datetime.now().strftime('%H:%M:%S')}
                            </div>
                            <div class="ws-chip">Viewport: {city_name}</div>
                            <div class="ws-chip">Theme: {theme_choice}</div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_r:
        chaos_level = random.choice(["Tranquil ✨", "Manageable ⚖️", "Spicy 🌶️", "Weird 🌪️", "Doomy-ish 💀"])
        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-end; margin-top:0.4rem;">
                <div class="ws-metric-card" style="max-width:230px;">
                    <div class="ws-metric-label">Global Vibes</div>
                    <div style="display:flex; justify-content:space-between; gap:0.8rem; align-items:center;">
                        <div>
                            <div class="ws-metric-value" style="font-size:1rem;">{chaos_level}</div>
                            <div class="ws-soft" style="font-size:0.8rem; margin-top:0.2rem;">
                                Not financial, political, or existential advice.
                            </div>
                        </div>
                        <div class="ws-chaos-ring">
                            <div class="ws-chaos-core">{chaos_level.split()[0]}</div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("\n")

    # MAIN BODY TABS
    overview_tab, news_tab, diagnostics_tab = st.tabs(["Overview", "News Stream", "Diagnostics"])

    # OVERVIEW TAB
    with overview_tab:
        # Top row: weather + key metrics + markets rollup
        c1, c2, c3 = st.columns([1.2, 1, 1])

        with c1:
            st.markdown('<div class="ws-section-title">Local Situation</div>', unsafe_allow_html=True)
            weather = fetch_weather(lat, lon, city_name)
            render_weather_block(weather)

        with c2:
            st.markdown('<div class="ws-section-title">Human Concerns</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="ws-metric-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div class="ws-metric-label">Coffee Supply</div>
                            <div class="ws-metric-value">Stable ☕</div>
                            <div class="ws-soft" style="font-size:0.8rem;">Critical systems remain online.</div>
                        </div>
                        <div class="ws-metric-pill">Priority: high</div>
                    </div>
                    <div style="margin-top:0.7rem; font-size:0.8rem;" class="ws-soft">
                        AI sentience: <span style="color:{theme['accent']}; font-weight:600;">debatable</span><br/>
                        Alien presence: not currently confirmed.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown('<div class="ws-section-title">Markets Pulse</div>', unsafe_allow_html=True)
            market_data = generate_market_data()
            # show two compact summaries
            for ticker in list(market_data.keys())[:2]:
                d = market_data[ticker]
                direction = "▲" if d["change"] >= 0 else "▼"
                color = "#22c55e" if d["change"] >= 0 else "#ef4444"
                st.markdown(
                    f"""
                    <div class="ws-card" style="margin-bottom:0.45rem;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                            <div style="font-weight:600;">{ticker}</div>
                            <div style="color:{color}; font-weight:600;">{direction} {d['change']:.2f}%</div>
                        </div>
                        <div class="ws-soft" style="font-size:0.78rem; margin-top:0.2rem;">
                            Spot ~ {d['current']:.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("\n")

        # Second row: news + detailed mini markets
        nc, mc = st.columns([2.2, 1])
        with nc:
            st.markdown('<div class="ws-section-title">Signal · Condensed Headlines</div>', unsafe_allow_html=True)

            world_news = fetch_news("world") if "World" in enabled_streams else []
            tech_news = fetch_news("tech") if "Tech" in enabled_streams else []
            sci_news = fetch_news("science") if "Science" in enabled_streams else []

            combined = world_news[:5] + tech_news[:4] + sci_news[:3]
            render_news_stream(combined)

        with mc:
            st.markdown('<div class="ws-section-title">Market Micrographs</div>', unsafe_allow_html=True)
            for ticker, d in market_data.items():
                render_market_widget(ticker, d)

    # NEWS TAB
    with news_tab:
        st.markdown('<div class="ws-section-title">Full Streams</div>', unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)

        with t1:
            st.markdown("##### 🌍 World", unsafe_allow_html=True)
            render_news_stream(fetch_news("world"))

        with t2:
            st.markdown("##### 💻 Tech", unsafe_allow_html=True)
            render_news_stream(fetch_news("tech"))

        with t3:
            st.markdown("##### 🧬 Science", unsafe_allow_html=True)
            render_news_stream(fetch_news("science"))

    # DIAGNOSTICS TAB
    with diagnostics_tab:
        st.markdown('<div class="ws-section-title">Telemetry & Debug</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="ws-card">
                <div style="display:flex; flex-wrap:wrap; gap:1.1rem; font-size:0.88rem;">
                    <div>
                        <div class="ws-soft">Lat / Lon</div>
                        <div style="font-weight:600;">{lat:.3f} · {lon:.3f}</div>
                    </div>
                    <div>
                        <div class="ws-soft">Viewport city</div>
                        <div style="font-weight:600;">{city_name}</div>
                    </div>
                    <div>
                        <div class="ws-soft">Active feeds</div>
                        <div style="font-weight:600;">{', '.join(enabled_streams) or 'None'}</div>
                    </div>
                    <div>
                        <div class="ws-soft">Render timestamp</div>
                        <div style="font-weight:600;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                </div>
                <div style="margin-top:1rem; font-size:0.8rem;" class="ws-soft">
                    This panel exists purely for the engineers and the curious.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # FOOTER
    st.markdown(
        f"""
        <div class="ws-footer">
            Snapshot generated at <span>{datetime.now().strftime('%H:%M:%S')}</span> ·
            built with Streamlit, public APIs, and a healthy respect for uncertainty.
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
