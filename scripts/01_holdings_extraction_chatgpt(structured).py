# =====================================
# IMPORT LIBRARIES
# =====================================

import pandas as pd
import ast


# =====================================
# LOAD RAW DATASET
# =====================================

df = pd.read_csv(
    r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\raw\Mutual Funds Indian Market.csv"
)


# =====================================
# PARSE STOCK HOLDINGS COLUMN
# Convert string -> Python list
# =====================================

df['stock_holdings'] = df['stock_holdings'].apply(ast.literal_eval)


# =====================================
# EXPLODE HOLDINGS
# One stock holding -> one row
# =====================================

df = df.explode('stock_holdings')


# =====================================
# REMOVE NULL HOLDINGS
# =====================================

df = df[df['stock_holdings'].notna()]


# =====================================
# NORMALIZE HOLDINGS DICTIONARY
# Dict keys -> columns
# =====================================

holdings_expanded = pd.json_normalize(df['stock_holdings'])


# =====================================
# PRESERVE FUND INFORMATION
# =====================================

final_holdings = pd.concat(
    [df[['basic_info']], holdings_expanded],
    axis=1
)


# =====================================
# PARSE BASIC INFO
# String -> Dictionary
# =====================================

final_holdings['basic_info'] = final_holdings['basic_info'].apply(ast.literal_eval)


# =====================================
# NORMALIZE BASIC INFO
# =====================================

basic_info_expanded = pd.json_normalize(final_holdings['basic_info'])


# =====================================
# CREATE FINAL ANALYTICAL TABLE
# =====================================

final_holdings = pd.concat(
    [basic_info_expanded, holdings_expanded],
    axis=1
)


# =====================================
# CLEAN ASSETS COLUMN
# Remove % sign and convert to float
# =====================================

final_holdings['assets'] = final_holdings['assets'].str.replace('%', '')
final_holdings['assets'] = final_holdings['assets'].astype(float)


# =====================================
# EXPORT CLEAN DATASET
# =====================================

final_holdings.to_csv(
    r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\data\cleaned\clean_holdings.csv",
    index=False
)


# =====================================
# PREVIEW FINAL DATA
# =====================================

print(final_holdings.head())