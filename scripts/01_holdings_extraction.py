import pandas as pd
import ast 

df=pd.read_csv(r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\raw\Mutual Funds Indian Market.csv")



df['stock_holdings']=df['stock_holdings'].apply(ast.literal_eval)
df['basic_info']=df['basic_info'].apply(ast.literal_eval)

df=df.explode('stock_holdings')

df=df[df['stock_holdings'].notna()]
holdings_expanded=pd.json_normalize(df['stock_holdings'])

final_holdings = pd.concat(
    [df[['basic_info']], holdings_expanded],
    axis=1
)

basic_info_expanded = pd.json_normalize(final_holdings['basic_info'])
print(basic_info_expanded.head(2))

final_holdings = pd.concat(
    [basic_info_expanded, holdings_expanded],
    axis=1
)

final_holdings['assets']=final_holdings['assets'].str.replace('%','')
final_holdings['assets']=final_holdings['assets'].astype(float)

print(final_holdings.head(4))

final_holdings.to_csv(
    r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\cleaned\clean_holdings.csv",
    index=False
)