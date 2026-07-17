import pandas as pd

def analyse_df(df, analysis_data_folder):
    results = {}
    print("Running analysis...")

    # def SEGMENT (Lifestage x Premium_Customer)

    # Total sales by segment
    segment_summary = (
        df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])
        .agg(
            TOTAL_SALES = ('TOT_SALES', 'sum'),
            N_CUSTOMERS = ('LYLTY_CARD_NBR', 'nunique'),
            TOTAL_UNITS = ('PROD_QTY', 'sum'),
            AVG_PACKET_WEIGHT = ('PACKET_WEIGHT', 'mean')
        ).reset_index()
    )

    segment_summary['AVG_SALES_PER_CUSTOMER'] = segment_summary['TOTAL_SALES'] / segment_summary['N_CUSTOMERS']
    segment_summary['AVG_PRICE_PER_UNIT'] = segment_summary['TOTAL_SALES'] / segment_summary['TOTAL_UNITS']
    segment_summary['AVG_UNITS_PER_CUSTOMER'] = segment_summary['TOTAL_UNITS'] / segment_summary['N_CUSTOMERS']
    # print("Segment summary\n", segment_summary)

# ----------------------------------------------------------------

    df['PACK_SIZE_CATEGORY'] = pd.cut(
        df['PACKET_WEIGHT'],
        bins=[0, 150, 200, 1000],
        labels=['PACK_SIZE1', 'PACK_SIZE2', 'PACK_SIZE3']
    )

    pack_category_by_segment = (
        (
                pd.crosstab(
                [df['LIFESTAGE'], df['PREMIUM_CUSTOMER']],
                df['PACK_SIZE_CATEGORY'],
                normalize='index'  # gives % within each segment, not raw counts
            ) * 100
        ).round(1).reset_index()
    )

    segment_summary = segment_summary.merge(
        pack_category_by_segment,
        on=['LIFESTAGE', 'PREMIUM_CUSTOMER'])
    # print("Pack size in buckets by segment", pack_category_by_segment)

# ------------------------------------------------------------------------------------

    # brand percentages
    # Brand share (%) within each segment
    brand_share_by_segment = (
            pd.crosstab(
                [df['LIFESTAGE'], df['PREMIUM_CUSTOMER']],
                df['BRAND'],
                normalize='index'
            ) * 100
        )

    def top3_plus_other_labeled(row):
        sorted_row = row.sort_values(ascending=False)
        top3 = sorted_row.head(3)
        others = sorted_row.iloc[3:].sum()
        return pd.Series({
            'BRAND_1': top3.index[0], 'BRAND_1_PCT': round(top3.iloc[0], 1),
            'BRAND_2': top3.index[1], 'BRAND_2_PCT': round(top3.iloc[1], 1),
            'BRAND_3': top3.index[2], 'BRAND_3_PCT': round(top3.iloc[2], 1),
            'BRAND_OTHERS_PCT': round(others, 1)
        })
    
    brand_share_by_segment = brand_share_by_segment.apply(top3_plus_other_labeled, axis=1)
    brand_share_by_segment = brand_share_by_segment.reset_index()

    segment_summary = segment_summary.merge(
        brand_share_by_segment,
        on=['LIFESTAGE', 'PREMIUM_CUSTOMER']
    )

    # print("brand share in segments", brand_share_by_segment)

# ------------------------------------------------------------------------------------

    brand_price_list = (
        df.groupby('BRAND')
        .agg(
            TOTAL_SALES=('TOT_SALES', 'sum'),
            TOTAL_UNITS=('PROD_QTY', 'sum'),
            N_TRANSACTIONS=('TXN_ID', 'count')
        )
        .reset_index()
    )
    brand_price_list['AVG_PRICE_PER_UNIT'] = brand_price_list['TOTAL_SALES'] / brand_price_list['TOTAL_UNITS']
    brand_price_list = brand_price_list.sort_values('TOTAL_UNITS', ascending=False)
    # print("Brand price list", brand_price_list)

# ------------------------------------------------------------------------------------

    segment_summary.to_csv(f"{analysis_data_folder}/segment_summary.csv", index=False)
    brand_price_list.to_csv(f"{analysis_data_folder}/brand_price_list.csv", index=False)

# create dictionary of results
    results['SEGMENT_SUMMARY'] = segment_summary
    results['BRAND_PRICE_LIST'] = brand_price_list

    print("Analysis completed, returned results.")
    return results







    # AFTER UNITS PER CUSTOMER AND PRICE PER UNIT
# So the answer to "why do families spend more per customer" is now clear: 
# it's volume, not price. Families buy roughly double the number of chip packets per person compared to Young Singles/Couples, at essentially the same price per packet. 
# This matches basic intuition — families are buying chips for multiple household members, so of course they need more units — 
# Putting all three metrics together — the full story
# Total sales - Singles/Couples and Retirees "win," because they have huge customer counts
# Avg sales per customer - Families actually spend more per person
# Avg price per unit vs avg units per customer - why — Families buy more units, not pricier units

# Why this matters for your recommendation
# This is actually useful precisely because it rules something out. Combined with your earlier findings, the full chain of reasoning now looks like:
# Total sales alone was misleading — driven by segment headcount, not customer value (Table 1)
# Families are the highest-value customers per head (Table 2)
# That's driven by buying more units, not pricier units (price/unit is flat, ~$3.7-4.0 everywhere) (Table 3)
# It's also not driven by buying bigger packs — pack size mix is flat across every segment (Table 4, this one)
# So the conclusion tightens: families buy chips more frequently / in more separate transactions, at the same price point and same pack size as everyone else — this is a frequency/volume story, not a product-mix story. That's actually a cleaner, more useful insight for Julia than if pack size had varied — it tells her the lever to pull is availability, shelf space, and multi-buy promotions (encouraging more frequent or bulk purchase occasions) rather than needing to stock different pack sizes for different customer types.

# Look at the concentration numbers: top-3 brands combined only ever add up to ~38–45% of purchases in any segment (100% − Others%). That means the majority of chip purchases, in every single segment, are spread across many smaller brands rather than concentrated in a few favorites. And critically — the identity of the top 3 (Kettle, Smiths, Doritos/Pringles) barely changes across all 21 segments.
