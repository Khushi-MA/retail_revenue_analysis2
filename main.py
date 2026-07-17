import pandas as pd
from pathlib import Path
import json
import os

from clean import clean_transaction_function
from clean import clean_purchase_behaviour_function
from clean import check_inconsistent_prod_name_number
from clean import extract_chips_data
from clean import merge_df_function
from analyse import analyse_df
from visualise import visualise_df

# import sys
# sys.exit("Program stopped")


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
    
    return folder_name

def create_brand_map():
    with open('brand_map.json', 'r') as f:
        brand_map = json.load(f)
    return brand_map

def load_data_file(file_name, date_cols=None):
    print(f"Extracting data from {file_name}... ")

    # if file is .xlsx
    if file_name.endswith((".xlsx", "xls")):
        df = pd.read_excel(file_name, sheet_name = 0)
        print(f"Extracting data form {file_name} successful")
    
    elif file_name.endswith(".csv"):
        df = pd.read_csv(file_name, parse_dates=date_cols)
        print(f"Extracting data from {file_name} successful")
    
    else:
        print("...WHAT FILE IS THAT???")

    return df

print("\n------------------------------------------------------------------------")
print("File/Folder make...")
print("------------------------------------------------------------------------")
data_folder = "data"
transaction_file_name = f"{data_folder}/QVI_transaction_data.xlsx"
purchase_behaviour_file_name = f"{data_folder}/QVI_purchase_behaviour.csv"

brand_map = create_brand_map()
clean_data_folder = "clean_data"
clean_transaction_file_name = f"{clean_data_folder}/transaction.csv"
clean_purchase_behaviour_file_name = f"{clean_data_folder}/purchase_behaviour.csv"
clean_merge_file_name = f"{clean_data_folder}/merged.csv"
chips_file_name = f"{clean_data_folder}/chips.csv"

analysis_data_folder = "analysis_data"

charts_folder = "charts"

# # to run from after analysis
# clean_data_folder = "clean_data"
# chips_file_name = f"{clean_data_folder}/chips.csv"
# df_chips = load_data_file(chips_file_name, date_cols=['DATE'])
# analysis_data_folder = "analysis_data"
# analysis_results = {}
# analysis_results['SEGMENT_SUMMARY'] = load_data_file(f"{analysis_data_folder}/segment_summary.csv")
# analysis_results['BRAND_PRICE_LIST'] = load_data_file(f"{analysis_data_folder}/brand_price_list.csv")


print("\n------------------------------------------------------------------------")
print("Cleaning...")
print("------------------------------------------------------------------------")
df_transactions = load_data_file(transaction_file_name)
df_purchase_behaviour = load_data_file(purchase_behaviour_file_name)
clean_data_folder = create_folder(clean_data_folder)
df_transactions_cleaned = clean_transaction_function(df_transactions, brand_map, clean_transaction_file_name, qty_outlier_threshold=200)
df_purchase_behaviour_cleaned = clean_purchase_behaviour_function(df_purchase_behaviour, clean_purchase_behaviour_file_name)


print("\n------------------------------------------------------------------------")
print("Merging...")
print("------------------------------------------------------------------------")
df_merged = merge_df_function(df_transactions_cleaned, df_purchase_behaviour, clean_merge_file_name, on="LYLTY_CARD_NBR", how="left")


print("\n------------------------------------------------------------------------")
print("Extract Chips...")
print("------------------------------------------------------------------------")
df_chips = extract_chips_data(df_merged, exclude_products, chips_file_name)


print("\n------------------------------------------------------------------------")
print("Analysis...")
print("------------------------------------------------------------------------")
analysis_data_folder = create_folder(analysis_data_folder)
analysis_results = analyse_df(df_chips, analysis_data_folder)


print("\n------------------------------------------------------------------------")
print("Visualisation...")
print("------------------------------------------------------------------------")
charts_folder = create_folder(charts_folder)
visualise_df(df_chips, analysis_results, charts_folder)

