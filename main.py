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
from trial_analysis import build_store_monthly_summary
from trial_analysis import check_complete_data_in_trial_stores
from trial_analysis import filter_stores_with_required_periods
from trial_analysis import find_control_store
from trial_analysis import plot_trial_vs_control_pretrial
from trial_analysis import compare_trial_vs_control
from trial_analysis import test_significance
from trial_analysis import plot_trial_vs_scaled_control

# # STOP program
# import sys
# sys.exit("Program stopped")

# def SEGMENT (Lifestage x Premium_Customer)

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
print("File/Folder variables...")
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

trial_analysis_charts = f"{charts_folder}/trial_analysis_charts"



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


# print("\n------------------------------------------------------------------------")
# print("Visualisation...")
# print("------------------------------------------------------------------------")
# charts_folder = create_folder(charts_folder)
# visualise_df(df_chips, analysis_results, charts_folder)



print("\n------------------------------------------------------------------------")
print("Task 2: Store Trial Analysis...")
print("------------------------------------------------------------------------")

charts_folder = "charts"
trial_analysis_charts = create_folder(trial_analysis_charts)
trial_stores = [77, 86, 88]
PRE_TRIAL_MONTHS = ['2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01']
TRIAL_MONTHS = ['2019-02', '2019-03', '2019-04']
METRICS = ['TOTAL_SALES', 'N_CUSTOMERS']

print("\n--- Step 1: Build monthly per-store summary ---")
store_monthly = build_store_monthly_summary(df_chips)
store_monthly_complete = filter_stores_with_required_periods(store_monthly, PRE_TRIAL_MONTHS, TRIAL_MONTHS)
check_complete_data_in_trial_stores(store_monthly_complete, trial_stores)

pre_trial = store_monthly_complete[store_monthly_complete['YEARMONTH'].isin(PRE_TRIAL_MONTHS)]
trial_period = store_monthly_complete[store_monthly_complete['YEARMONTH'].isin(TRIAL_MONTHS)]
print(f"Pre-trial: {pre_trial['YEARMONTH'].nunique()} months, {pre_trial.shape[0]} rows")
print(f"Trial period: {trial_period['YEARMONTH'].nunique()} months, {trial_period.shape[0]} rows")

print("\n--- Step 2: Select best control store for each trial store ---")
best_control_77, scores_77 = find_control_store(pre_trial, trial_store=77, exclude_stores=trial_stores)
best_control_86, scores_86 = find_control_store(pre_trial, trial_store=86, exclude_stores=trial_stores)
best_control_88, scores_88 = find_control_store(pre_trial, trial_store=88, exclude_stores=trial_stores)

pairs = [(77, best_control_77), (86, best_control_86), (88, best_control_88)]

print("\n--- Step 3: Visually validate control matches (pre-trial period) ---")
for trial, control in pairs:
    plot_trial_vs_control_pretrial(pre_trial, trial, control, 'TOTAL_SALES', trial_analysis_charts)
    plot_trial_vs_control_pretrial(pre_trial, trial, control, 'N_CUSTOMERS', trial_analysis_charts)

print("\n--- Step 4: Compare trial vs. scaled control (raw % difference) ---")
result_77_sales = compare_trial_vs_control(pre_trial, trial_period, 77, best_control_77, 'TOTAL_SALES')
result_86_sales = compare_trial_vs_control(pre_trial, trial_period, 86, best_control_86, 'TOTAL_SALES')
result_88_sales = compare_trial_vs_control(pre_trial, trial_period, 88, best_control_88, 'TOTAL_SALES')

print("\n--- Step 5: Statistical significance testing (all stores, both metrics) ---")
all_results = {}
for trial, control in pairs:
    for metric in METRICS:
        key = f"{trial}_{metric}"
        print(f"\n{'='*60}\nStore {trial} vs Control {control} — {metric}\n{'='*60}")
        all_results[key] = test_significance(pre_trial, trial_period, trial, control, metric)

print("\n--- Step 6: Visualize trial vs. scaled control (full timeline) ---")
for trial, control in pairs:
    for metric in METRICS:
        key = f"{trial}_{metric}"
        plot_trial_vs_scaled_control(pre_trial, trial_period, trial, control, metric, all_results[key], trial_analysis_charts)

