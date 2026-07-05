import streamlit as st
import pandas as pd
import plotly.express as px


# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(
    page_title="Mutual Fund X-Ray",
    page_icon="📊",
    layout="wide"
)


# ===================================
# TITLE
# ===================================

st.title("📊 Mutual Fund X-Ray Analyzer")

st.write("Analyze portfolio diversification and overlap risk")


# ===================================
# LOAD HOLDINGS DATA
# ===================================

mf = pd.read_csv(
    r"cleaned/clean_holdings.csv"
)


# ===================================
# SIDEBAR
# ===================================

st.sidebar.header("Upload Portfolio")

uploaded_file = st.sidebar.file_uploader(
    "Upload Portfolio CSV",
    type=["csv"]
)


# ===================================
# PROCESS PORTFOLIO
# ===================================

if uploaded_file is not None:

    # ===================================
    # READ USER PORTFOLIO
    # ===================================

    portfolio = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Portfolio")

    st.dataframe(portfolio)


    # ===================================
    # MERGE DATA
    # ===================================

    merged = portfolio.merge(
        mf,
        how='inner',
        left_on='Mutual_Fund_Name',
        right_on='fund_name'
    )


    # ===================================
    # EFFECTIVE EXPOSURE
    # ===================================

    merged['Investment_Amount_INR'] = (
        merged['Investment_Amount_INR']
        .astype(float)
    )

    merged['assets'] = (
        merged['assets']
        .astype(float)
    )

    merged['effective_exposure'] = (
        merged['Investment_Amount_INR']
        * merged['assets']
        / 100
    )


    # ===================================
    # MERGED DATA DISPLAY
    # ===================================

    st.subheader("Merged Portfolio Data")

    st.dataframe(merged.head(20))


    # ===================================
    # TOTAL PORTFOLIO VALUE
    # ===================================

    total_portfolio_amount = (
        portfolio['Investment_Amount_INR']
        .sum()
    )


    # ===================================
    # STOCK OVERLAP ENGINE
    # ===================================

    overlap = (
        merged
        .groupby('stock_name')['effective_exposure']
        .sum()
        .reset_index()
    )

    overlap['exposure_pct'] = (
        overlap['effective_exposure']
        / total_portfolio_amount
        * 100
    )

    final_overlap = (
        overlap
        .sort_values(
            by='exposure_pct',
            ascending=False
        )
    )


    # ===================================
    # SECTOR ENGINE
    # ===================================

    sectors = (
        merged
        .groupby('sector')['effective_exposure']
        .sum()
        .reset_index()
        .sort_values(
            by='effective_exposure',
            ascending=False
        )
    )

    sectors['sector_pct'] = (
        sectors['effective_exposure']
        / total_portfolio_amount
        * 100
    )


    # ===================================
    # METRICS
    # ===================================

    top_5_stock_conc = (
        final_overlap
        .head(5)['exposure_pct']
        .sum()
    )

    top_stock_exposure = (
        final_overlap
        .iloc[0]['exposure_pct']
    )

    top_sector_exposure = (
        sectors
        .iloc[0]['sector_pct']
    )

    overlap_table = (
        merged
        .groupby('stock_name')['Mutual_Fund_Name']
        .nunique()
        .reset_index()
        .sort_values(
            by='Mutual_Fund_Name',
            ascending=False
        )
    )

    overlap_intensity = (
        overlap_table
        .iloc[0]['Mutual_Fund_Name']
    )


    # ===================================
    # PENALTY ENGINE
    # ===================================

    # TOP STOCK PENALTY

    if top_stock_exposure < 5:
        top_stock_penalty = 0

    elif top_stock_exposure < 10:
        top_stock_penalty = 5

    elif top_stock_exposure < 15:
        top_stock_penalty = 10

    else:
        top_stock_penalty = 20


    # TOP 5 PENALTY

    if top_5_stock_conc < 25:
        top5_penalty = 0

    elif top_5_stock_conc < 40:
        top5_penalty = 5

    elif top_5_stock_conc < 60:
        top5_penalty = 10

    else:
        top5_penalty = 20


    # SECTOR PENALTY

    if top_sector_exposure < 20:
        sector_penalty = 0

    elif top_sector_exposure < 35:
        sector_penalty = 5

    elif top_sector_exposure < 50:
        sector_penalty = 10

    else:
        sector_penalty = 20


    # OVERLAP PENALTY

    if overlap_intensity == 1:
        overlap_penalty = 0

    elif overlap_intensity <= 3:
        overlap_penalty = 5

    elif overlap_intensity <= 5:
        overlap_penalty = 10

    else:
        overlap_penalty = 20


    # ===================================
    # FINAL SCORE
    # ===================================

    final_score = 100 - (
        top_stock_penalty
        + top5_penalty
        + sector_penalty
        + overlap_penalty
    )


    # ===================================
    # KPI DISPLAY
    # ===================================

    st.subheader("Portfolio Health Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Portfolio Health Score",
        f"{final_score}/100"
    )

    col2.metric(
        "Top Stock Exposure",
        f"{top_stock_exposure:.2f}%"
    )

    col3.metric(
        "Top Sector Exposure",
        f"{top_sector_exposure:.2f}%"
    )

    col4.metric(
        "Overlap Intensity",
        overlap_intensity
    )


    # ===================================
    # TOP STOCK EXPOSURE CHART
    # ===================================

    st.subheader("Top Stock Exposures")

    fig = px.bar(
        final_overlap.head(10),
        y='exposure_pct',
        x='stock_name',
        orientation='v',
        title='Top Stock Exposures'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ===================================
    # SECTOR CONCENTRATION CHART
    # ===================================

    st.subheader("Sector Concentration")

    fig2 = px.pie(
        sectors,
        names='sector',
        values='sector_pct',
        hole=0.4,
        title='Sector Concentration'
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # ===================================
    # FINAL TABLES
    # ===================================

    st.subheader("Top Exposure Stocks")

    st.dataframe(
        final_overlap.head(10)
    )

    st.subheader("Sector Breakdown")

    st.dataframe(
        sectors
    )


else:

    st.info("Please upload a portfolio CSV file.")