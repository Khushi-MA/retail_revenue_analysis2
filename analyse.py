def analyse_df(df):
    print("Running analysis...")

    # segment (Lifestage x Premium_Customer)

    # Total sales by segment
    sales_by_segment = (
        df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES']
        .sum()
        .reset_index()
        .sort_values('TOT_SALES', ascending=False)
    )
    print("\n---------------------------------\nTotal sales by segment:")
    print(sales_by_segment)

    # Number of unique customers per segment
    customers_by_segment = (
        df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['LYLTY_CARD_NBR']
        .nunique()
        .reset_index()
        .rename(columns={'LYLTY_CARD_NBR': 'N_CUSTOMERS'})
    )
    print("\n---------------------------------\nNumber of customers by segment:")
    print(customers_by_segment)

    # To get average spend per customer in each segment
    merged = sales_by_segment.merge(customers_by_segment, on=['LIFESTAGE', 'PREMIUM_CUSTOMER'])
    merged['AVG_SALES_PER_CUSTOMER'] = merged['TOT_SALES'] / merged['N_CUSTOMERS']
    merged = merged.sort_values('AVG_SALES_PER_CUSTOMER', ascending=False)
    print("\n---------------------------------\nAverage spend per customer in each segment")
    print(merged)

    # Added column "price per unit" on total sales and product quantity
    df['PRICE_PER_UNIT'] = df['TOT_SALES'] / df['PROD_QTY']

    # avg units per customer
    units_per_customer = (
        df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])
        .agg(
            TOTAL_UNITS=('PROD_QTY', 'sum'),
            N_CUSTOMERS=('LYLTY_CARD_NBR', 'nunique'),
            AVG_PRICE_PER_UNIT=('PRICE_PER_UNIT', 'mean')
        )
        .reset_index()
    )
    units_per_customer['AVG_UNITS_PER_CUSTOMER'] = units_per_customer['TOTAL_UNITS'] / units_per_customer['N_CUSTOMERS']
    units_per_customer = units_per_customer.sort_values('AVG_UNITS_PER_CUSTOMER', ascending=False)
    print("\n---------------------------------\nUnits per customer")
    print(units_per_customer)

    return sales_by_segment, customers_by_segment