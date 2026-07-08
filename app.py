import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

BASE = os.path.dirname(__file__)

st.set_page_config(
    page_title="Mutual Fund X-Ray | Sarthak Gothwal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# THEME — fintech: deep navy + warm gold, paper-white accents
# ---------------------------------------------------------------------------
NAVY_DARK = "#0b1220"
NAVY_PANEL = "#121b2e"
NAVY_LINE = "#22314a"
GOLD = "#d4a94f"
GOLD_SOFT = "#e8cd8a"
PAPER = "#eee9df"
SLATE = "#8593a8"
GOOD = "#4fbf8f"
WARN = "#d4a94f"
BAD = "#d9645f"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {NAVY_DARK};
    color: {PAPER};
}}
.stApp {{ background: linear-gradient(180deg, {NAVY_DARK} 0%, #080d17 100%); }}
#MainMenu, header, footer {{ visibility:hidden; }}
section[data-testid="stSidebar"] {{ background: {NAVY_PANEL}; border-right: 1px solid {NAVY_LINE}; }}

.eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    color: {GOLD};
    letter-spacing: 0.18em;
    font-size: 0.75rem;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}}
.hero-title {{
    font-family: 'Fraunces', serif;
    font-size: 2.9rem;
    font-weight: 600;
    line-height: 1.08;
    margin: 0;
    color: {PAPER};
}}
.hero-title em {{ color: {GOLD_SOFT}; font-style: italic; }}
.hero-sub {{
    color: {SLATE};
    font-size: 1.03rem;
    max-width: 660px;
    margin-top: 0.9rem;
    line-height: 1.6;
}}

.section-label {{
    font-family: 'IBM Plex Mono', monospace;
    color: {GOLD};
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin: 2.2rem 0 0.3rem 0;
    border-left: 3px solid {GOLD};
    padding-left: 0.6rem;
}}
.section-title {{
    font-family: 'Fraunces', serif;
    font-size: 1.55rem;
    font-weight: 600;
    margin: 0.2rem 0 1rem 0;
    color: {PAPER};
}}

.card {{
    background: {NAVY_PANEL};
    border: 1px solid {NAVY_LINE};
    border-radius: 6px;
    padding: 1.1rem 1.3rem;
    height: 100%;
}}
.kpi-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: {GOLD_SOFT};
}}
.kpi-label {{ color: {SLATE}; font-size: 0.8rem; margin-top: 0.3rem; }}

.finding {{
    border-left: 2px solid {NAVY_LINE};
    padding: 0.15rem 0 0.15rem 1rem;
    margin-bottom: 1rem;
}}
.finding-title {{ font-weight:600; font-size:1rem; margin-bottom: 0.2rem; }}
.finding-body {{ color:{SLATE}; font-size:0.88rem; line-height:1.5; }}

.demo-box {{
    background: {NAVY_PANEL};
    border: 1px solid {GOLD};
    border-radius: 8px;
    padding: 1.4rem;
    margin-top: 1rem;
}}

a {{ color: {GOLD_SOFT}; }}
.footer-cta {{
    margin-top: 3rem;
    padding: 1.6rem;
    background: {NAVY_PANEL};
    border: 1px solid {NAVY_LINE};
    border-radius: 8px;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

def plotly_theme(fig, height=380):
    fig.update_layout(
        paper_bgcolor=NAVY_PANEL,
        plot_bgcolor=NAVY_PANEL,
        font=dict(family="Inter, sans-serif", color=PAPER, size=12),
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=NAVY_LINE, zerolinecolor=NAVY_LINE)
    fig.update_yaxes(gridcolor=NAVY_LINE, zerolinecolor=NAVY_LINE)
    return fig

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
st.markdown('<div class="eyebrow">Portfolio Diversification & Overlap Risk</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Mutual Fund <em>X-Ray</em><br>Analyzer</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Most investors hold multiple mutual funds believing they\'re diversified — '
    'but those funds often quietly hold the same top stocks. This system X-rays a combined portfolio '
    'to expose real stock exposure, sector concentration, and fund overlap, and compresses it into a '
    'single 0–100 <b>Portfolio Health Score</b>. Built by <b>Sarthak Gothwal</b>.</div>',
    unsafe_allow_html=True,
)
st.link_button("View full source on GitHub →", "https://github.com/saarthak19s/Mutual-Fund-XRay-Analyzer")

# ---------------------------------------------------------------------------
# WHY IT MATTERS
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Why This Matters</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The diversification illusion</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card"><b style="color:#e8cd8a">Hidden overlap</b>'
                '<div class="kpi-label" style="margin-top:0.5rem;">Two funds marketed as "diversified" can '
                'share 60–70% of their top 10 holdings.</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><b style="color:#e8cd8a">Sector bias</b>'
                '<div class="kpi-label" style="margin-top:0.5rem;">A portfolio spread across 5 funds can '
                'still carry 50%+ exposure to one sector.</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><b style="color:#e8cd8a">One number, not 500 rows</b>'
                '<div class="kpi-label" style="margin-top:0.5rem;">The Health Score summarizes risk without '
                'reading a single holdings sheet.</div></div>', unsafe_allow_html=True)

st.markdown(
    f"<p style='color:{SLATE}; margin-top:1rem;'>This replicates the kind of X-Ray analysis tools that "
    f"platforms like Morningstar and Value Research offer — built from scratch in Python, on real Indian "
    f"mutual fund holdings data from Kaggle (77,000+ holdings rows across 1,400+ funds), relevant to BFSI "
    f"roles at platforms like Groww, Zerodha, and Paytm Money.</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# HOW THE SCORE WORKS
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Methodology</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">How the Portfolio Health Score works</div>', unsafe_allow_html=True)

left, right = st.columns([1.1, 1])
with left:
    st.markdown("""
| Signal | Weight | Logic |
|---|---|---|
| Diversification index | 40% | Wider stock spread → higher score |
| Sector concentration | 35% | Penalizes heavy single-sector bets |
| Overlap intensity | 25% | Penalizes holdings shared across funds |
""")
    st.caption("Score above 70 = healthy, well-diversified portfolio. Below 50 flags significant concentration risk.")
with right:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=80,
        title={"text": "Example: a well-diversified portfolio"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": GOLD},
            "steps": [
                {"range": [0, 50], "color": "#3a2530"},
                {"range": [50, 70], "color": "#3a3320"},
                {"range": [70, 100], "color": "#20362c"},
            ],
        },
    ))
    st.plotly_chart(plotly_theme(fig, 280), use_container_width=True)

# ---------------------------------------------------------------------------
# LIVE DEMO — the real, working analyzer
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Try It Live</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Run the actual analyzer</div>', unsafe_allow_html=True)

st.markdown(
    f"<p style='color:{SLATE};'>This isn't a mockup — it's the real engine from the GitHub repo, running on "
    f"77,000+ real holdings rows. Upload your own portfolio CSV, or click below to load a demo portfolio "
    f"instantly.</p>",
    unsafe_allow_html=True,
)

@st.cache_data
def load_holdings():
    return pd.read_csv(f"{BASE}/cleaned/clean_holdings.csv")

mf = load_holdings()

if "demo_loaded" not in st.session_state:
    st.session_state.demo_loaded = False

col_a, col_b = st.columns([1, 3])
with col_a:
    if st.button("▶ Load demo portfolio", use_container_width=True):
        st.session_state.demo_loaded = True

st.sidebar.header("Upload Your Portfolio")
uploaded_file = st.sidebar.file_uploader("Upload Portfolio CSV", type=["csv"])
st.sidebar.caption("Expected columns: Mutual_Fund_Name, Investment_Amount_INR")

portfolio = None
if uploaded_file is not None:
    portfolio = pd.read_csv(uploaded_file)
    st.session_state.demo_loaded = False
elif st.session_state.demo_loaded:
    portfolio = pd.read_csv(f"{BASE}/cleaned/sample_portfolio.csv")

if portfolio is not None:
    st.markdown('<div class="demo-box">', unsafe_allow_html=True)
    st.subheader("Your Portfolio")
    st.dataframe(portfolio, use_container_width=True)

    merged = portfolio.merge(mf, how="inner", left_on="Mutual_Fund_Name", right_on="fund_name")

    if merged.empty:
        st.warning(
            "No matching funds found in the holdings database. Fund names must exactly match "
            "entries in the underlying dataset (1,405 Indian mutual funds covered) — try the demo "
            "portfolio button above to see it work end-to-end."
        )
    else:
        merged["Investment_Amount_INR"] = merged["Investment_Amount_INR"].astype(float)
        merged["assets"] = merged["assets"].astype(float)
        merged["effective_exposure"] = merged["Investment_Amount_INR"] * merged["assets"] / 100

        total_portfolio_amount = portfolio["Investment_Amount_INR"].sum()

        overlap = merged.groupby("stock_name")["effective_exposure"].sum().reset_index()
        overlap["exposure_pct"] = overlap["effective_exposure"] / total_portfolio_amount * 100
        final_overlap = overlap.sort_values(by="exposure_pct", ascending=False)

        sectors = (
            merged.groupby("sector")["effective_exposure"].sum().reset_index()
            .sort_values(by="effective_exposure", ascending=False)
        )
        sectors["sector_pct"] = sectors["effective_exposure"] / total_portfolio_amount * 100

        top_5_stock_conc = final_overlap.head(5)["exposure_pct"].sum()
        top_stock_exposure = final_overlap.iloc[0]["exposure_pct"]
        top_sector_exposure = sectors.iloc[0]["sector_pct"]

        overlap_table = (
            merged.groupby("stock_name")["Mutual_Fund_Name"].nunique().reset_index()
            .sort_values(by="Mutual_Fund_Name", ascending=False)
        )
        overlap_intensity = overlap_table.iloc[0]["Mutual_Fund_Name"]

        top_stock_penalty = 0 if top_stock_exposure < 5 else 5 if top_stock_exposure < 10 else 10 if top_stock_exposure < 15 else 20
        top5_penalty = 0 if top_5_stock_conc < 25 else 5 if top_5_stock_conc < 40 else 10 if top_5_stock_conc < 60 else 20
        sector_penalty = 0 if top_sector_exposure < 20 else 5 if top_sector_exposure < 35 else 10 if top_sector_exposure < 50 else 20
        overlap_penalty = 0 if overlap_intensity == 1 else 5 if overlap_intensity <= 3 else 10 if overlap_intensity <= 5 else 20

        final_score = 100 - (top_stock_penalty + top5_penalty + sector_penalty + overlap_penalty)

        st.subheader("Portfolio Health Metrics")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Portfolio Health Score", f"{final_score}/100")
        k2.metric("Top Stock Exposure", f"{top_stock_exposure:.2f}%")
        k3.metric("Top Sector Exposure", f"{top_sector_exposure:.2f}%")
        k4.metric("Overlap Intensity", int(overlap_intensity))

        d1, d2 = st.columns(2)
        with d1:
            fig = px.bar(final_overlap.head(10), x="stock_name", y="exposure_pct",
                         color_discrete_sequence=[GOLD], title="Top Stock Exposures")
            st.plotly_chart(plotly_theme(fig), use_container_width=True)
        with d2:
            fig2 = px.pie(sectors, names="sector", values="sector_pct", hole=0.5,
                          title="Sector Concentration",
                          color_discrete_sequence=px.colors.sequential.Sunset)
            st.plotly_chart(plotly_theme(fig2), use_container_width=True)

        t1, t2 = st.columns(2)
        with t1:
            st.subheader("Top Exposure Stocks")
            st.dataframe(final_overlap.head(10), use_container_width=True)
        with t2:
            st.subheader("Sector Breakdown")
            st.dataframe(sectors, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Click **Load demo portfolio** above, or upload your own CSV in the sidebar, to run the analyzer.")

# ---------------------------------------------------------------------------
# DASHBOARD SCREENSHOTS
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Deliverable</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The Power BI dashboard</div>', unsafe_allow_html=True)
st.caption("Interactive visualizations with slicers for fund selection, sector filter, and overlap view.")

st.image(f"{BASE}/screenshots/dashboard2.png", use_container_width=True)

# ---------------------------------------------------------------------------
# TECH STACK
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Under the hood</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Pipeline &amp; stack</div>', unsafe_allow_html=True)

t1, t2 = st.columns(2)
with t1:
    st.markdown("""
```
Mutual-Fund-XRay-Analyzer/
├── raw/          Original Kaggle dataset files
├── cleaned/      Processed holdings, sector & stock exposure tables
├── scripts/
│   ├── 01_holdings_extraction.py
│   └── 02_overlap_engine.py
└── screenshots/  Power BI dashboard previews
```
""")
with t2:
    st.markdown("""
| Tool | Purpose |
|---|---|
| Python · Pandas | Data cleaning, transformation, aggregation |
| Kaggle dataset | 1,405 Indian mutual funds, 77K+ holdings rows |
| Power BI | Interactive dashboard, fund/sector slicers |
| Streamlit | This live, interactive demo |
""")

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown(
    f'<div class="footer-cta">'
    f'<b>Sarthak Gothwal</b><br>'
    f'<span style="color:{SLATE}">Full code, data, and dashboard files on GitHub</span><br><br>'
    f'</div>',
    unsafe_allow_html=True,
)
st.link_button("github.com/saarthak19s/Mutual-Fund-XRay-Analyzer",
                "https://github.com/saarthak19s/Mutual-Fund-XRay-Analyzer", use_container_width=True)
