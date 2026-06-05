
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10

# Load data
print("Loading data...")
fb_df = pd.read_csv('01_facebook_ads.csv')
ga_df = pd.read_csv('02_google_ads.csv')
tt_df = pd.read_csv('03_tiktok_ads.csv')

# Normalize column names for unification
fb_df['platform'] = 'Facebook'
fb_df['date'] = pd.to_datetime(fb_df['date'])
fb_df['spend'] = fb_df['spend']

ga_df['platform'] = 'Google Ads'
ga_df['date'] = pd.to_datetime(ga_df['date'])
ga_df['spend'] = ga_df['cost']

tt_df['platform'] = 'TikTok'
tt_df['date'] = pd.to_datetime(tt_df['date'])
tt_df['spend'] = tt_df['cost']

# Create unified dataset with common metrics
unified_data = []

for platform, df in [('Facebook', fb_df), ('Google Ads', ga_df), ('TikTok', tt_df)]:
    temp = df[['date', 'campaign_name', 'impressions', 'clicks', 'spend', 'conversions']].copy()
    temp['platform'] = platform
    unified_data.append(temp)

combined_df = pd.concat(unified_data, ignore_index=True)

# Calculate key metrics
combined_df['ctr'] = (combined_df['clicks'] / combined_df['impressions'] * 100).round(2)
combined_df['cpc'] = (combined_df['spend'] / combined_df['clicks']).round(2)
combined_df['cpa'] = (combined_df['spend'] / combined_df['conversions']).round(2)
combined_df['roas'] = (combined_df['conversions'] / combined_df['spend']).round(2)

print("\n=== UNIFIED DASHBOARD DATA ===")
print(f"Date Range: {combined_df['date'].min()} to {combined_df['date'].max()}")
print(f"Total Spend: ${combined_df['spend'].sum():,.2f}")
print(f"Total Conversions: {combined_df['conversions'].sum():,.0f}")
print(f"Overall CTR: {(combined_df['clicks'].sum() / combined_df['impressions'].sum() * 100):.2f}%")
fig = plt.figure(figsize=(18, 12))
fig.suptitle('Multi-Channel Marketing Analytics Dashboard', fontsize=18, fontweight='bold', y=0.995)

ax1 = plt.subplot(3, 3, 1)
spend_by_platform = combined_df.groupby('platform')['spend'].sum().sort_values(ascending=False)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
spend_by_platform.plot(kind='bar', ax=ax1, color=colors)
ax1.set_title('Total Spend by Platform', fontweight='bold', fontsize=11)
ax1.set_ylabel('Spend ($)')
ax1.set_xlabel('')
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(spend_by_platform.values):
    ax1.text(i, v + max(spend_by_platform) * 0.02, f'${v:,.0f}', ha='center', fontweight='bold')

ax2 = plt.subplot(3, 3, 2)
conv_by_platform = combined_df.groupby('platform')['conversions'].sum().sort_values(ascending=False)
conv_by_platform.plot(kind='bar', ax=ax2, color=colors)
ax2.set_title('Total Conversions by Platform', fontweight='bold', fontsize=11)
ax2.set_ylabel('Conversions')
ax2.set_xlabel('')
ax2.tick_params(axis='x', rotation=45)
for i, v in enumerate(conv_by_platform.values):
    ax2.text(i, v + max(conv_by_platform) * 0.02, f'{v:,.0f}', ha='center', fontweight='bold')

ax3 = plt.subplot(3, 3, 3)
imp_by_platform = combined_df.groupby('platform')['impressions'].sum().sort_values(ascending=False)
imp_by_platform.plot(kind='bar', ax=ax3, color=colors)
ax3.set_title('Total Impressions by Platform', fontweight='bold', fontsize=11)
ax3.set_ylabel('Impressions')
ax3.set_xlabel('')
ax3.tick_params(axis='x', rotation=45)
for i, v in enumerate(imp_by_platform.values):
    ax3.text(i, v + max(imp_by_platform) * 0.02, f'{v/1e6:.1f}M', ha='center', fontweight='bold')

ax4 = plt.subplot(3, 3, 4)
cpa_data = combined_df.groupby('platform').apply(lambda x: (x['spend'].sum() / x['conversions'].sum())).sort_values(ascending=True)
cpa_data.plot(kind='barh', ax=ax4, color=colors)
ax4.set_title('Cost Per Acquisition (CPA) by Platform', fontweight='bold', fontsize=11)
ax4.set_xlabel('CPA ($)')
for i, v in enumerate(cpa_data.values):
    ax4.text(v + max(cpa_data) * 0.02, i, f'${v:.2f}', va='center', fontweight='bold')

ax5 = plt.subplot(3, 3, 5)
ctr_data = (combined_df.groupby('platform')['clicks'].sum() / combined_df.groupby('platform')['impressions'].sum() * 100).sort_values(ascending=False)
ctr_data.plot(kind='bar', ax=ax5, color=colors)
ax5.set_title('Click-Through Rate (CTR) by Platform', fontweight='bold', fontsize=11)
ax5.set_ylabel('CTR (%)')
ax5.set_xlabel('')
ax5.tick_params(axis='x', rotation=45)
for i, v in enumerate(ctr_data.values):
    ax5.text(i, v + max(ctr_data) * 0.02, f'{v:.2f}%', ha='center', fontweight='bold')

ax6 = plt.subplot(3, 3, 6)
roas_data = (combined_df.groupby('platform')['conversions'].sum() / combined_df.groupby('platform')['spend'].sum()).sort_values(ascending=False)
roas_data.plot(kind='bar', ax=ax6, color=colors)
ax6.set_title('Return on Ad Spend (ROAS) by Platform', fontweight='bold', fontsize=11)
ax6.set_ylabel('ROAS (Conversions/$)')
ax6.set_xlabel('')
ax6.tick_params(axis='x', rotation=45)
for i, v in enumerate(roas_data.values):
    ax6.text(i, v + max(roas_data) * 0.02, f'{v:.3f}', ha='center', fontweight='bold')

ax7 = plt.subplot(3, 3, 7)
daily_spend = combined_df.groupby(['date', 'platform'])['spend'].sum().unstack()
daily_spend.plot(ax=ax7, marker='o', linewidth=2)
ax7.set_title('Daily Spend Trend by Platform', fontweight='bold', fontsize=11)
ax7.set_ylabel('Spend ($)')
ax7.set_xlabel('Date')
ax7.legend(title='Platform', loc='best')
ax7.grid(True, alpha=0.3)

ax8 = plt.subplot(3, 3, 8)
daily_conv = combined_df.groupby(['date', 'platform'])['conversions'].sum().unstack()
daily_conv.plot(ax=ax8, marker='o', linewidth=2)
ax8.set_title('Daily Conversions Trend by Platform', fontweight='bold', fontsize=11)
ax8.set_ylabel('Conversions')
ax8.set_xlabel('Date')
ax8.legend(title='Platform', loc='best')
ax8.grid(True, alpha=0.3)

ax9 = plt.subplot(3, 3, 9)
campaign_perf = combined_df.groupby('campaign_name').agg({
    'spend': 'sum',
    'conversions': 'sum'
}).reset_index()
campaign_perf['cpa'] = campaign_perf['spend'] / campaign_perf['conversions']
top_campaigns = campaign_perf.nlargest(5, 'conversions')

x_pos = np.arange(len(top_campaigns))
ax9.bar(x_pos, top_campaigns['conversions'].values, color='steelblue', label='Conversions', alpha=0.7)
ax9_twin = ax9.twinx()
ax9_twin.plot(x_pos, top_campaigns['cpa'].values, color='red', marker='o', linewidth=2, label='CPA', markersize=8)

ax9.set_title('Top 5 Campaigns: Conversions vs CPA', fontweight='bold', fontsize=11)
ax9.set_ylabel('Conversions', color='steelblue')
ax9_twin.set_ylabel('CPA ($)', color='red')
ax9.set_xticks(x_pos)
ax9.set_xticklabels([name[:15] for name in top_campaigns['campaign_name'].values], rotation=45, ha='right', fontsize=8)
ax9.tick_params(axis='y', labelcolor='steelblue')
ax9_twin.tick_params(axis='y', labelcolor='red')

plt.tight_layout()
plt.savefig('marketing_dashboard.png', dpi=300, bbox_inches='tight')
print("\n✓ Dashboard saved as 'marketing_dashboard.png'")

print("\n=== PLATFORM BREAKDOWN ===")
for platform in combined_df['platform'].unique():
    platform_data = combined_df[combined_df['platform'] == platform]
    total_spend = platform_data['spend'].sum()
    total_conv = platform_data['conversions'].sum()
    total_clicks = platform_data['clicks'].sum()
    total_imp = platform_data['impressions'].sum()
    
    print(f"\n{platform}:")
    print(f"  Spend: ${total_spend:,.2f}")
    print(f"  Conversions: {total_conv:,.0f}")
    print(f"  CPA: ${total_spend/total_conv:.2f}")
    print(f"  CTR: {(total_clicks/total_imp*100):.2f}%")
    print(f"  ROAS: {(total_conv/total_spend):.3f}")

plt.show()
