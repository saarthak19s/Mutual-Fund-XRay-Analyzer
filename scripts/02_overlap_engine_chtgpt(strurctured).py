# ============================================
# MUTUAL FUND X-RAY : PORTFOLIO SCORING ENGINE
# ============================================

import pandas as pd


# ============================================
# SECTION 1 : LOAD DATA
# ============================================

mf = pd.read_csv(
    r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\cleaned\clean_holdings.csv"
)

us = pd.read_csv(
    r"c:\Users\HP\Downloads\indian_unbalanced_portfolio.csv"
)


# ============================================
# SECTION 2 : DATA PREPARATION
# ============================================

merged = us.merge(
    mf,
    how='inner',
    left_on='Mutual_Fund_Name',
    right_on='fund_name'
)

merged['Investment_Amount_INR'] = merged['Investment_Amount_INR'].astype(float)

merged['assets'] = merged['assets'].astype(float)


# ============================================
# SECTION 3 : EFFECTIVE EXPOSURE ENGINE
# ============================================

merged['effective_exposure'] = (
    merged['Investment_Amount_INR']
    * merged['assets']
    / 100
)


# ============================================
# SECTION 4 : TOTAL PORTFOLIO VALUE
# ============================================

total_portfolio_amount = us['Investment_Amount_INR'].sum()


# ============================================
# SECTION 5 : STOCK OVERLAP ENGINE
# ============================================

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
    .sort_values(by='exposure_pct', ascending=False)
)

exposure_filter = final_overlap['exposure_pct'] > 0.1

top_exposure_stocks = (
    final_overlap[exposure_filter]
    .head(10)
)


# ============================================
# SECTION 6 : SECTOR CONCENTRATION ENGINE
# ============================================

sectors = (
    merged
    .groupby('sector')['effective_exposure']
    .sum()
    .reset_index()
    .sort_values(by='effective_exposure', ascending=False)
)

sectors['sector_pct'] = (
    sectors['effective_exposure']
    / total_portfolio_amount
    * 100
)

sector_filter = sectors['sector_pct'] > 0

final_sectors = sectors[sector_filter]


# ============================================
# SECTION 7 : METRIC EXTRACTION
# ============================================

# TOP 5 STOCK CONCENTRATION

top_5_stock_conc = (
    top_exposure_stocks
    .head(5)['exposure_pct']
    .sum()
)


# TOP STOCK EXPOSURE

top_stock_exposure = (
    top_exposure_stocks
    .iloc[0]['exposure_pct']
)


# TOP SECTOR EXPOSURE

top_sector_exposure = (
    final_sectors
    .iloc[0]['sector_pct']
)


# OVERLAP INTENSITY

overlap_table = (
    merged
    .groupby('stock_name')['Mutual_Fund_Name']
    .nunique()
    .reset_index()
    .sort_values(by='Mutual_Fund_Name', ascending=False)
)

overlap_intensity = (
    overlap_table
    .iloc[0]['Mutual_Fund_Name']
)


# ============================================
# SECTION 8 : PENALTY ENGINE
# ============================================

# --------------------------------------------
# FACTOR 1 : TOP STOCK CONCENTRATION
# --------------------------------------------

if top_stock_exposure < 5:
    top_stock_penalty = 0

elif top_stock_exposure < 10:
    top_stock_penalty = 5

elif top_stock_exposure < 15:
    top_stock_penalty = 10

else:
    top_stock_penalty = 20


# --------------------------------------------
# FACTOR 2 : TOP 5 STOCK CONCENTRATION
# --------------------------------------------

if top_5_stock_conc < 25:
    top5_penalty = 0

elif top_5_stock_conc < 40:
    top5_penalty = 5

elif top_5_stock_conc < 60:
    top5_penalty = 10

else:
    top5_penalty = 20


# --------------------------------------------
# FACTOR 3 : TOP SECTOR CONCENTRATION
# --------------------------------------------

if top_sector_exposure < 20:
    sector_penalty = 0

elif top_sector_exposure < 35:
    sector_penalty = 5

elif top_sector_exposure < 50:
    sector_penalty = 10

else:
    sector_penalty = 20


# --------------------------------------------
# FACTOR 4 : OVERLAP INTENSITY
# --------------------------------------------

if overlap_intensity == 1:
    overlap_penalty = 0

elif overlap_intensity <= 3:
    overlap_penalty = 5

elif overlap_intensity <= 5:
    overlap_penalty = 10

else:
    overlap_penalty = 20


# ============================================
# SECTION 9 : FINAL PORTFOLIO HEALTH SCORE
# ============================================

final_score = 100 - (
    top_stock_penalty
    + top5_penalty
    + sector_penalty
    + overlap_penalty
)


# ============================================
# SECTION 10 : FINAL OUTPUTS
# ============================================

print("\n====================================")
print("PORTFOLIO HEALTH SCORE")
print("====================================")

print(f"Portfolio Health Score : {final_score}/100")


print("\n====================================")
print("TOP STOCK EXPOSURES")
print("====================================")

print(top_exposure_stocks)


print("\n====================================")
print("SECTOR CONCENTRATION")
print("====================================")

print(final_sectors)


print("\n====================================")
print("KEY METRICS")
print("====================================")

print(f"Top Stock Exposure        : {top_stock_exposure:.2f}%")

print(f"Top 5 Stock Concentration : {top_5_stock_conc:.2f}%")

print(f"Top Sector Exposure       : {top_sector_exposure:.2f}%")

print(f"Overlap Intensity         : {overlap_intensity}")

# ============================================
# SECTION 9 : FINAL PORTFOLIO HEALTH SCORE
# ============================================

final_score = 100 - (
    top_stock_penalty
    + top5_penalty
    + sector_penalty
    + overlap_penalty
)

print("\n====================================")
print("PORTFOLIO HEALTH SCORE")
print("====================================")

print(f"Portfolio Health Score : {final_score}/100")