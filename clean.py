import pandas as pd
from pathlib import Path
import re
import json

def check_inconsistent_prod_name_number(df):
    # Check if any PROD_NBR has more than one PROD_NAME
    prod_nbr_to_names = df.groupby("PROD_NBR")["PROD_NAME"].nunique()
    multi_name_prods = prod_nbr_to_names[prod_nbr_to_names > 1]

    print("PROD_NBR with more than one PROD_NAME:")
    print(multi_name_prods)

    # Check if any PROD_NAME has more than one PROD_NBR
    prod_name_to_numbers = df.groupby("PROD_NAME")["PROD_NBR"].nunique()
    multi_number_prods = prod_name_to_numbers[prod_name_to_numbers > 1]

    print("\nPROD_NAME with more than one PROD_NBR:")
    print(multi_number_prods)

    # For any PROD_NBR with multiple names, show exactly what those names are
    if len(multi_name_prods) > 0:
        problem_nbrs = multi_name_prods.index
        print(df[df['PROD_NBR'].isin(problem_nbrs)][['PROD_NBR', 'PROD_NAME']].drop_duplicates().sort_values('PROD_NBR'))

    # Same for the reverse case
    if len(multi_number_prods) > 0:
        problem_names = multi_number_prods.index
        print(df[df['PROD_NAME'].isin(problem_names)][['PROD_NBR', 'PROD_NAME']].drop_duplicates().sort_values('PROD_NAME'))


def clean_transaction_function(df, brand_map, clean_transaction_file_name, qty_outlier_threshold):
    print("Cleaning transaction data...")
    print("Shape before cleaning: ", df.shape, "\n")

    print("Date:")
    # date changed to datetime type
    df['DATE'] = pd.to_datetime(
        df['DATE'],
        unit='D',
        origin='1899-12-30'
    )
    print("Date changed from int to datetime datatype\n")

    print("Product Quantity:")
    before = len(df)
    df = df[df["PROD_QTY"] < qty_outlier_threshold].reset_index(drop=True)
    print(f"Removed {before - len(df)} rows, outliers wrt PROD_QTY, product quantity < 200\n")

    print("Product Name:")
    # edit that one name that has weight in between the brand and product name
    df.loc[df["PROD_NAME"].str.lower() == "kettle 135g swt pot sea salt", "PROD_NAME"] = "KETTLE SWT POT SEA SALT 135G"
    print("Kettle name replacement complete\n")

    # make all uppercase remove trailing spaces convert to string
    df["PROD_NAME"] = df["PROD_NAME"].astype(str).str.strip().str.upper()
    # remove double spaces in product names
    df["PROD_NAME"] = (df["PROD_NAME"].str.split().str.join(" "))
    print("Product name uppercased, stripped, removed double spaces\n")

    print("Packet Weight:")
    df["PACKET_WEIGHT"] = (df["PROD_NAME"]
                            .str.extract(r'(\d+)\s*G\s*$', expand=False)
                            .astype("Int64"))
    df["PROD_NAME"] = (df["PROD_NAME"]
                            .str.replace(r'(\d+)\s*G\s*$', "", regex=True)
                            .str.strip())
    print("extracted packet weight form PROD_NAME into PACKET_WEIGHT and removed form PROD_NAME")

    print("Products whose weight extraction failed (null packet weights):")
    print(df[df['PACKET_WEIGHT'].isna()]['PROD_NAME'].unique())

    df["BRAND"] = df["PROD_NAME"].str.split().str[0]
    print("Created BRAND column in df from first word of the products")
    df["BRAND"] = df["BRAND"].replace(brand_map)
    print("Due to inconsistency, replaced the brand name with the mapped value in brand_map")

    for raw, standardized in sorted(brand_map.items(), key=lambda x: -len(x[0].split())):
        if raw == standardized:
            continue  # nothing to fix
        pattern = r'^' + re.escape(raw) + r'\b'
        already_correct = df["PROD_NAME"].str.startswith(standardized)
        needs_fix = df["PROD_NAME"].str.match(pattern) & ~already_correct
        df.loc[needs_fix, "PROD_NAME"] = df.loc[needs_fix, "PROD_NAME"].str.replace(pattern, standardized, regex=True)

    print("Checking inconsistent product names and numbers...")
    check_inconsistent_prod_name_number(df)
    print("Checked\n")

    before = len(df)
    print("Number of duplicate transaction records: ", df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Duplicate {before - len(df)} rows removed\n")

    print("Total duplicate txn_id... same transaction with multiple products: ", df["TXN_ID"].duplicated().sum(), "\n")
    print("Shape after cleaning: ", df.shape)
    
    print("Cleaning completed, returned df")
    df.to_csv(clean_transaction_file_name, index=False)
    return df

def clean_purchase_behaviour_function(df, clean_purchase_behaviour_file_name):
    print("Cleaning purchases data...")
    print("Shape before cleaning: ", df.shape)

    df = df.drop_duplicates().reset_index(drop=True)

    print("Shape after cleaning: ", df.shape)
    print("Cleaning completed, returned df")
    df.to_csv(clean_purchase_behaviour_file_name, index=False)
    return df

def extract_chips_data(df, exclude_products, chips_file_name):
    print("Filtering chips data...")

    before = len(df)
    print("\nOther non-Chip products that will be git rid of:")
    print(df.loc[df["PROD_NAME"].isin(exclude_products),["PROD_NAME", "BRAND"]]
                    .drop_duplicates().sort_values("PROD_NAME"))
    
    df = df[~df['PROD_NAME'].isin(exclude_products)].reset_index(drop=True)

    print(f"\nDropped {before - len(df)} non-chip rows")
    print("Returned chip data")

    df.to_csv(chips_file_name, index=False)
    return df

def merge_df_function(df_transactions_cleaned, df_purchase_behaviour, clean_merge_file_name, on="LYLTY_CARD_NBR", how="left"):
    df = df_transactions_cleaned.merge(df_purchase_behaviour, on=on, how=how)
    print("Both the data merged into one with common LYLTY_CARD_NBR column\nNew data shape: ", df.shape)
    
    df.to_csv(clean_merge_file_name, index=False)
    return df