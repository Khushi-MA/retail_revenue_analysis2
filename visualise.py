import matplotlib
matplotlib.use('Agg')  # non-interactive backend — needed since this runs as a script, not a notebook
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.dates as mdates
import numpy as np


color1 = "teal"
color2 = "coral"
color3 = "maroon"

def color_map_function(n):
    return plt.cm.viridis(np.linspace(0, 1, n))

# def add_bar_labels(ax, fmt="{:.0f}", padding=3):
#     for container in ax.containers:
#         ax.bar_label(container, fmt=fmt, padding=padding)

def add_bar_labels(ax, fmt="{:.0f}", padding=3):
    for container in ax.containers:
        labels = ax.bar_label(container, fmt=fmt, padding=padding)

        for label in labels:
            label.set_bbox({
                "facecolor": "white",
                "alpha": 0.7,
                "edgecolor": "none",
                "pad": 0.5
            })



def sales_by_segment(df, charts_dir):
    df = df.sort_values('TOTAL_SALES', ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['LIFESTAGE'] + ' - ' + df['PREMIUM_CUSTOMER'], df['TOTAL_SALES'], color=color1)
    add_bar_labels(ax, fmt="{:.0f}")
    ax.set_xlabel('Total Sales ($)')
    ax.set_title('Total Sales by Segment')
    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'sales_by_segment.png'), dpi=150)
    plt.close(fig)
    print("Saved: sales_by_segment.png")


def top_brands_sales_vs_count(df, charts_dir):
    top5_sales = df.sort_values('TOTAL_SALES', ascending=False).head(5)
    top5_count = df.sort_values('N_TRANSACTIONS', ascending=False).head(5)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left panel: top 5 by sales
    axes[0].bar(top5_sales['BRAND'], top5_sales['TOTAL_SALES'], color=color1)
    add_bar_labels(axes[0], fmt="{:.0f}")
    axes[0].set_title('Top 5 Brands by Total Sales ($)')
    axes[0].set_ylabel('Total Sales ($)')
    axes[0].tick_params(axis='x', rotation=45)

    # Right panel: top 5 by count
    axes[1].bar(top5_count['BRAND'], top5_count['N_TRANSACTIONS'], color=color2)
    add_bar_labels(axes[1], fmt="{:.0f}")
    axes[1].set_title('Top 5 Brands by Number of Transactions')
    axes[1].set_ylabel('Transaction Count')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'top_brands_sales_vs_count.png'), dpi=150)
    plt.close(fig)
    print("Saved: top_brands_sales_vs_count.png")


def top15_products_sales_vs_units(df, charts_dir):
    product_summary = (
        df.groupby('PROD_NAME')
        .agg(
            TOTAL_SALES=('TOT_SALES', 'sum'), 
            TOTAL_UNITS=('PROD_QTY', 'sum'))
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    top15_sales = product_summary.sort_values('TOTAL_SALES', ascending=False).head(15)
    axes[0].barh(top15_sales['PROD_NAME'], top15_sales['TOTAL_SALES'], color=color1)
    add_bar_labels(axes[0], fmt="{:.0f}")
    axes[0].set_title('Top 15 Products by Total Sales')
    axes[0].invert_yaxis()

    top15_units = product_summary.sort_values('TOTAL_UNITS', ascending=False).head(15)
    axes[1].barh(top15_units['PROD_NAME'], top15_units['TOTAL_UNITS'], color=color2)
    add_bar_labels(axes[1], fmt="{:.0f}")
    axes[1].set_title('Top 15 Products by Units Sold')
    axes[1].invert_yaxis()

    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'top15_products_sales_vs_units.png'), dpi=150)
    plt.close(fig)
    print("Saved: top15_products_sales_vs_units.png")

def avg_spend_per_customer(df, charts_dir):
    df = df.sort_values('AVG_SALES_PER_CUSTOMER', ascending=False)
    segment_labels = df['LIFESTAGE'] + ' - ' + df['PREMIUM_CUSTOMER']

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(segment_labels, df['AVG_SALES_PER_CUSTOMER'], color=color1)
    add_bar_labels(ax, fmt="${:.2f}")
    ax.set_xlabel('Average Spend per Customer ($)')
    ax.set_title('Average Spend per Customer by Segment')
    ax.invert_yaxis()  # highest at top
    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'avg_spend_per_customer.png'), dpi=150)
    plt.close(fig)
    print("Saved: avg_spend_per_customer.png")

def pack_size_mix(df, charts_dir):
    segment_labels = df['LIFESTAGE'] + ' - ' + df['PREMIUM_CUSTOMER']

    fig, ax = plt.subplots(figsize=(10, 8))
    bars1 = ax.barh(segment_labels, df['PACK_SIZE1'], color=color2, label='Small (<150g)')
    bars2 = ax.barh(segment_labels, df['PACK_SIZE2'], left=df['PACK_SIZE1'], color=color1, label='Medium (150-200g)')
    bars3 = ax.barh(segment_labels, df['PACK_SIZE3'], left=df['PACK_SIZE1'] + df['PACK_SIZE2'], color=color3, label='Large (>200g)')
    ax.bar_label(bars1, fmt="%.1f%%", label_type="center")
    ax.bar_label(bars2, fmt="%.1f%%", label_type="center")
    ax.bar_label(bars3, fmt="%.1f%%", label_type="center")

    ax.set_xlabel('% of Purchases')
    ax.set_title('Pack Size Mix by Segment')
    ax.legend(loc='lower right')
    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'pack_size_mix.png'), dpi=150)
    plt.close(fig)
    print("Saved: pack_size_mix.png")

def monthly_sales_trend(df, charts_dir):
    df = df.copy()
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['MONTH'] = df['DATE'].dt.to_period('M').dt.to_timestamp()

    monthly_sales = df.groupby('MONTH')['TOT_SALES'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_sales['MONTH'], monthly_sales['TOT_SALES'], marker='o', color=color1, linewidth=2)
    for x, y in zip(monthly_sales['MONTH'], monthly_sales['TOT_SALES']):
        ax.annotate(
            f"{y:,.0f}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center"
        )
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales ($)')
    ax.set_title('Monthly Chip Sales Trend (Jul 2018 - Jun 2019)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'monthly_sales_trend.png'), dpi=150)
    plt.close(fig)
    print("Saved: monthly_sales_trend.png")


def top_customers_by_sales(df, output_dir, top_n=15):
    customer_sales = (
        df.groupby('LYLTY_CARD_NBR')['TOT_SALES']
        .sum()
        .reset_index()
        .sort_values('TOT_SALES', ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(customer_sales['LYLTY_CARD_NBR'].astype(str), customer_sales['TOT_SALES'], color=color1)
    add_bar_labels(ax, fmt="${:.2f}")
    ax.set_xlabel('Total Sales ($)')
    ax.set_ylabel('Loyalty Card Number')
    ax.set_title(f'Top {top_n} Customers by Total Sales')
    ax.invert_yaxis()  # highest at top
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'top_customers_by_sales.png'), dpi=150)
    plt.close(fig)
    print("Saved: top_customers_by_sales.png")


def headcount_lifestage(segment_df, charts_dir):
    # Collapse to single-variable headcounts by summing across the other dimension
    lifestage_counts = segment_df.groupby('LIFESTAGE')['N_CUSTOMERS'].sum().sort_values(ascending=False)

    # --- Figure 1: LIFESTAGE ---
    fig1, axes1 = plt.subplots(1, 2, figsize=(14, 6))

    axes1[0].bar(lifestage_counts.index, lifestage_counts.values, color=color1)
    add_bar_labels(axes1[0], fmt="{:.0f}")
    axes1[0].set_title('Customer Count by Lifestage')
    axes1[0].set_ylabel('Number of Customers')
    axes1[0].tick_params(axis='x', rotation=45)

    axes1[1].pie(lifestage_counts.values, labels=lifestage_counts.index, colors=color_map_function(len(lifestage_counts)), autopct='%1.1f%%', startangle=90)
    axes1[1].set_title('Customer Share by Lifestage')

    plt.tight_layout()
    fig1.savefig(os.path.join(charts_dir, 'headcount_lifestage.png'), dpi=150)
    plt.close(fig1)
    print("Saved: headcount_lifestage.png")


def headcount_premium(segment_df, charts_dir):
    # Collapse to single-variable headcounts by summing across the other dimension
    premium_counts = segment_df.groupby('PREMIUM_CUSTOMER')['N_CUSTOMERS'].sum().sort_values(ascending=False)

    # --- Figure 2: PREMIUM_CUSTOMER ---
    fig2, axes2 = plt.subplots(1, 2, figsize=(12, 6))

    axes2[0].bar(premium_counts.index, premium_counts.values, color=color1)
    add_bar_labels(axes2[0], fmt="{:.0f}")
    axes2[0].set_title('Customer Count by Premium Tier')
    axes2[0].set_ylabel('Number of Customers')

    axes2[1].pie(premium_counts.values, labels=premium_counts.index, colors=color_map_function(len(premium_counts)), autopct='%1.1f%%', startangle=90)
    axes2[1].set_title('Customer Share by Premium Tier')

    plt.tight_layout()
    fig2.savefig(os.path.join(charts_dir, 'headcount_premium_customer.png'), dpi=150)
    plt.close(fig2)
    print("Saved: headcount_premium_customer.png")


def avg_price_per_unit_by_premium_customer(df, charts_dir):
    premium_cust_summary = (
        df.groupby('PREMIUM_CUSTOMER')
        .agg(
            TOTAL_SALES=('TOT_SALES', 'sum'), 
            TOTAL_UNITS=('PROD_QTY', 'sum'))
        .reset_index()
    )

    premium_cust_summary['AVG_PRICE_PER_UNIT'] = (premium_cust_summary['TOTAL_SALES'] / premium_cust_summary['TOTAL_UNITS'])
    premium_cust_summary = premium_cust_summary.sort_values('AVG_PRICE_PER_UNIT', ascending=False)

    fig, axes = plt.subplots(figsize=(14, 6))
    axes.bar(premium_cust_summary['PREMIUM_CUSTOMER'], premium_cust_summary['AVG_PRICE_PER_UNIT'], color=color1)
    add_bar_labels(axes, fmt="{:.2f}")
    axes.set_title('avg_price_per_unit_by_premium_customer')
    axes.set_xlabel('Premium customer type')
    axes.set_ylabel('avg_price_per_unit ($)')
    axes.tick_params(axis='x', rotation=45)

    fig.savefig(os.path.join(charts_dir, 'avg_price_per_unit_by_premium_customer.png'), dpi=150)
    plt.close(fig)
    print("Saved: avg_price_per_unit_by_premium_customer.png")


def affluence_effect_summary(df, charts_dir):
    premium_summary = (
        df.groupby('PREMIUM_CUSTOMER')
        .agg(
            TOTAL_SALES=('TOT_SALES', 'sum'),
            TOTAL_UNITS=('PROD_QTY', 'sum'),
            AVG_PACKET_WEIGHT=('PACKET_WEIGHT', 'mean'),
        )
        .reset_index()
    )
    premium_summary['AVG_PRICE_PER_UNIT'] = premium_summary['TOTAL_SALES'] / premium_summary['TOTAL_UNITS']
    premium_summary = premium_summary.sort_values('AVG_PRICE_PER_UNIT', ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].bar(premium_summary['PREMIUM_CUSTOMER'], premium_summary['AVG_PRICE_PER_UNIT'], color=color1)
    add_bar_labels(axes[0], fmt="{:.2f}")
    axes[0].set_title('Average Price per Unit')
    axes[0].set_ylabel('$ per unit')
    axes[0].tick_params(axis='x', rotation=45)

    axes[1].bar(premium_summary['PREMIUM_CUSTOMER'], premium_summary['AVG_PACKET_WEIGHT'], color=color2)
    add_bar_labels(axes[1], fmt="{:.0f}")
    axes[1].set_title('Average Pack Size')
    axes[1].set_ylabel('grams')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig.savefig(f"{charts_dir}/affluence_effect_summary.png", dpi=150)
    plt.close(fig)
    print("Saved: affluence_effect_summary.png")


def visualise_df(df, analysis_results, charts_dir):
    SEGMENT_SUMMARY = analysis_results['SEGMENT_SUMMARY']
    BRAND_PRICE_LIST = analysis_results['BRAND_PRICE_LIST']

    sales_by_segment(SEGMENT_SUMMARY, charts_dir)
    top_brands_sales_vs_count(BRAND_PRICE_LIST, charts_dir)
    top15_products_sales_vs_units(df, charts_dir)
    avg_spend_per_customer(SEGMENT_SUMMARY, charts_dir)
    pack_size_mix(SEGMENT_SUMMARY, charts_dir)
    monthly_sales_trend(df, charts_dir)
# Chip sales peak in December-January and should inform inventory planning and promotional timing — stock levels and shelf space should be increased ahead of the holiday season, with the sharp February drop-off suggesting promotions/discounting could help sustain volume through the post-holiday slump rather than accepting the seasonal decline passively."
    headcount_lifestage(SEGMENT_SUMMARY, charts_dir)
    headcount_premium(SEGMENT_SUMMARY, charts_dir)
    top_customers_by_sales(df, charts_dir)
    avg_price_per_unit_by_premium_customer(df, charts_dir)
    affluence_effect_summary(df, charts_dir)



    # Top brands by segment multibar



