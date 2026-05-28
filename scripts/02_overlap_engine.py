import pandas as pd

mf=pd.read_csv(r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\cleaned\clean_holdings.csv")
us=pd.read_csv(r"c:\Users\HP\Downloads\indian_unbalanced_portfolio.csv")



merged=us.merge(mf,how='inner',left_on='Mutual_Fund_Name',right_on='fund_name')
merged['Investment_Amount_INR']=merged['Investment_Amount_INR'].astype(float)
merged['assets']=merged['assets'].astype(float)
merged['effective_exposure']=(merged['Investment_Amount_INR']*merged['assets']/100)
print(merged[['Mutual_Fund_Name','stock_name','assets','effective_exposure']].head(20))

overlap=merged.groupby('stock_name')['effective_exposure'].sum().reset_index()
overlap['exposure_pct']=(overlap['effective_exposure']/us['Investment_Amount_INR'].sum()*100)
final_overlap=overlap.sort_values(by='exposure_pct',ascending=False)
mask=final_overlap['exposure_pct']>0.1
top_exp=final_overlap[mask].head(10)
print(top_exp)

#now we will do sector concentration #
sectors=merged.groupby('sector')['effective_exposure'].sum().reset_index().sort_values(by='effective_exposure',ascending=False)
sectors['sector_pct']=(sectors['effective_exposure']/us['Investment_Amount_INR'].sum()*100)
mask2=sectors['sector_pct']>0
final_sectors=sectors[mask2]
print(final_sectors)

#SCORE CALCULAIION
#METRIC 1 - TOp 5 STOCK CONC.
print('*+*+*+*+**++*++*+*+*+*+')
top_exp=final_overlap[mask].head(5)
top_5_stock_conc=top_exp['exposure_pct'].sum()
print(top_5_stock_conc)

#METRIC2 - Top Stock Exposure
top_stock_exposure= top_exp['exposure_pct'].iloc[0]
print(top_stock_exposure)

#METRIC 3 - Top Sector Concentration

top_sector_exposure=final_sectors.iloc[0]['sector_pct']
print(top_sector_exposure)

#METRIC 4 - overlap intensity
a=merged.groupby('stock_name')['Mutual_Fund_Name'].nunique().reset_index().sort_values(by='Mutual_Fund_Name',ascending=False)
overlap_intensity=a.iloc[0]['Mutual_Fund_Name']
print(overlap_intensity)

#PENALTY SCORE ENGINE
# for metric 1 - 
if top_stock_exposure < 5:
    top_stock_penalty = 0

elif top_stock_exposure < 10:
    top_stock_penalty = 5

elif top_stock_exposure < 15:
    top_stock_penalty = 10

else:
    top_stock_penalty = 20

print(top_stock_penalty)

# =====================================
# FACTOR 2 → TOP 5 STOCK CONCENTRATION
# =====================================

if top_5_stock_conc < 25:
    top5_penalty = 0

elif top_5_stock_conc < 40:
    top5_penalty = 5

elif top_5_stock_conc < 60:
    top5_penalty = 10

else:
    top5_penalty = 20


print(top5_penalty)



# =====================================
# FACTOR 3 → TOP SECTOR CONCENTRATION
# =====================================

if top_sector_exposure < 20:
    sector_penalty = 0

elif top_sector_exposure < 35:
    sector_penalty = 5

elif top_sector_exposure < 50:
    sector_penalty = 10

else:
    sector_penalty = 20


print(sector_penalty)



# =====================================
# FACTOR 4 → OVERLAP INTENSITY
# =====================================

if overlap_intensity == 1:
    overlap_penalty = 0

elif overlap_intensity <= 3:
    overlap_penalty = 5

elif overlap_intensity <= 5:
    overlap_penalty = 10

else:
    overlap_penalty = 20


print(overlap_penalty)


#FINAL SCORE

# =====================================
# FINAL PORTFOLIO HEALTH SCORE
# =====================================

final_score = 100 - (
    top_stock_penalty
    + top5_penalty
    + sector_penalty
    + overlap_penalty
)

print(f"Portfolio Health Score = {final_score}/100")


#Summary

summary = pd.DataFrame({
    'Portfolio_Health_Score': [final_score],
    'Top_Stock_Exposure': [top_stock_exposure],
    'Top_5_Stock_Concentration': [top_5_stock_conc],
    'Top_Sector_Exposure': [top_sector_exposure],
    'Overlap_Intensity': [overlap_intensity]
})
print(summary)

#Exporting 

top_exp.to_csv(r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\cleaned\top_stock_exposure.csv",index=False)
final_sectors.to_csv(r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\cleaned\final_sector_exposure.csv",index=False)
summary.to_csv(r"C:\Users\HP\Desktop\Mutual_Fund_XRay_Project\cleaned\portfolio_summary.csv",index=False)


