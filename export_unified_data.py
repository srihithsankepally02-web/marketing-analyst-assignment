"""
Export Unified Data for Google Sheets
Creates a single unified table ready to upload to Google Sheets
"""

import pandas as pd

# Load data
print("Loading data...")
fb_df = pd.read_csv('01_facebook_ads.csv')
ga_df = pd.read_csv('02_google_ads.csv')
tt_df = pd.read_csv('03_tiktok_ads.csv')

# Normalize for unification
fb_df['platform'] = 'Facebook'
fb_df['date'] = pd.to_datetime(fb_df['date'])
fb_df['cost'] = fb_df['spend']

ga_df['platform'] = 'Google Ads'
ga_df['date'] = pd.to_datetime(ga_df['date'])

tt_df['platform'] = 'TikTok'
tt_df['date'] = pd.to_datetime(tt_df['date'])

# Extract common columns and create unified table
columns_to_keep = ['date', 'campaign_id', 'campaign_name', 'impressions', 'clicks', 'cost', 'conversions', 'platform']

fb_unified = fb_df[columns_to_keep].copy()
ga_unified = ga_df[columns_to_keep].copy()
tt_unified = tt_df[columns_to_keep].copy()

# Combine all data
unified_df = pd.concat([fb_unified, ga_unified, tt_unified], ignore_index=True)

# Add calculated metrics
unified_df['ctr'] = (unified_df['clicks'] / unified_df['impressions'] * 100).round(2)
unified_df['cpc'] = (unified_df['cost'] / unified_df['clicks']).round(2)
unified_df['cpa'] = (unified_df['cost'] / unified_df['conversions']).round(2)
unified_df['roas'] = (unified_df['conversions'] / unified_df['cost']).round(3)

# Sort by date
unified_df = unified_df.sort_values('date').reset_index(drop=True)

# Export to CSV for Google Sheets
output_file = 'unified_marketing_data.csv'
unified_df.to_csv(output_file, index=False)
print(f"✓ Unified data exported to '{output_file}'")

# Display summary
print("\n=== UNIFIED DATA SUMMARY ===")
print(f"Total Records: {len(unified_df)}")
print(f"Date Range: {unified_df['date'].min().date()} to {unified_df['date'].max().date()}")
print(f"Platforms: {', '.join(unified_df['platform'].unique())}")
print(f"\nColumns in unified table:")
for col in unified_df.columns:
    print(f"  - {col}")

print(f"\n=== QUICK STATS ===")
print(f"Total Spend: ${unified_df['cost'].sum():,.2f}")
print(f"Total Conversions: {unified_df['conversions'].sum():,.0f}")
print(f"Total Impressions: {unified_df['impressions'].sum():,.0f}")
print(f"Average CPA: ${unified_df['cpa'].mean():.2f}")

# Show first few rows
print("\n=== FIRST 5 ROWS ===")
print(unified_df.head())

# Export to Excel as well for easier Google Sheets import
unified_df.to_excel('unified_marketing_data.xlsx', index=False, sheet_name='Marketing Data')
print("\n✓ Also exported to 'unified_marketing_data.xlsx' for easier import")
