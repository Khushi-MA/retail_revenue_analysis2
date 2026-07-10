import pandas as pd
from pathlib import Path
import re
import json
import os

from clean import clean_transaction_function
from clean import clean_purchase_behaviour_function
from clean import check_inconsistent_prod_name_number
from clean import extract_chips_data
from analyse import analyse_df

exclude_products = [
    'INFUZIONS BBQ RIB PRAWN CRACKERS',
    'INFUZIONS MANGO CHUTNY PAPADUMS',
    'INFUZIONS SOURCREAM&HERBS VEG STRWS',
    'OLD EL PASO SALSA DIP TOMATO MILD',
    'OLD EL PASO SALSA DIP CHNKY TOM HT',
    'OLD EL PASO SALSA DIP TOMATO MED',
    'WOOLWORTHS MILD SALSA',
    'WOOLWORTHS MEDIUM SALSA',
    'DORITOS SALSA MEDIUM',
    'DORITOS SALSA MILD',
]

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f"Folder {folder_name} created")

def create_brand_map():
    with open('brand_map.json', 'r') as f:
        brand_map = json.load(f)
    return brand_map

def load_file(file_name):
    print("extracting data from file...")
    # if file is .xlsx
    if file_name.endswith((".xlsx", "xls")):
        df = pd.read_excel(file_name, sheet_name = 0)
        print(f"Extracting data form {file_name} successful")
    
    elif file_name.endswith(".csv"):
        df = pd.read_csv(file_name)
        print(f"Extracting data from {file_name} successful")
    
    else:
        print("WHAT FILE IS THAT???")

    return df


# print("\n------------------------------------------------------------------------")
# print("Cleaning...")
# print("------------------------------------------------------------------------")
# df_purchase_behaviour = load_file("data/QVI_purchase_behaviour.csv")
# df_transactions = load_file("data/QVI_transaction_data.xlsx")
# print("------------------------------------------------------------------------")
# brand_map = create_brand_map()
# create_folder("clean_data")
# df_transactions_cleaned = clean_transaction_function(df_transactions, brand_map, qty_outlier_threshold=200)
# df_transactions_cleaned.to_csv("clean_data/transaction.csv", index=False)
# print("------------------------------------------------------------------------")
# df_purchase_behaviour_cleaned = clean_purchase_behaviour_function(df_purchase_behaviour)
# df_purchase_behaviour_cleaned.to_csv("clean_data/purchase_behaviour.csv", index=False)

# print("\n------------------------------------------------------------------------")
# print("Merging...")
# print("------------------------------------------------------------------------")
# df_transactions_cleaned = load_file("clean_data/transaction.csv")
# df_purchase_behaviour = load_file("clean_data/purchase_behaviour.csv")
# print("------------------------------------------------------------------------")
# df_merged = df_transactions_cleaned.merge(df_purchase_behaviour, on='LYLTY_CARD_NBR', how='left')
# print("Both the data merged into one with common LYLTY_CARD_NBR column")
# print("New data shape: ", df_merged.shape)
# df_merged.to_csv('clean_data/merged.csv', index=False)

# print("\n------------------------------------------------------------------------")
# print("Extract Chips...")
# print("------------------------------------------------------------------------")
# df_merged = load_file("clean_data/merged.csv")
# df_chips = extract_chips_data(df_merged, exclude_products)
# df_chips.to_csv('clean_data/chips.csv', index=False)

print("\n------------------------------------------------------------------------")
print("Analysis...")
print("------------------------------------------------------------------------")
df = load_file("clean_data/chips.csv")
create_folder("graphs")
analyse_df(df)