# to run only VISUALISATION
# comment out everything in main code EXCEPT visualisation, paste this and run it

clean_data_folder = "clean_data"
chips_file_name = f"{clean_data_folder}/chips.csv"
df_chips = load_data_file(chips_file_name, date_cols=['DATE'])
analysis_data_folder = "analysis_data"
analysis_results = {}
analysis_results['SEGMENT_SUMMARY'] = load_data_file(f"{analysis_data_folder}/segment_summary.csv")
analysis_results['BRAND_PRICE_LIST'] = load_data_file(f"{analysis_data_folder}/brand_price_list.csv")
charts_folder = "charts"

# to run ONLY TASK 2
clean_data_folder = "clean_data"
chips_file_name = f"{clean_data_folder}/chips.csv"
df_chips = load_data_file(chips_file_name, date_cols=['DATE'])
charts_folder = "charts"
trial_analysis_charts = f"{charts_folder}/trial_analysis_charts"


# --------------------------------

# FOR STORE TRIAL ANALYSIS

# check for stores which have all the required data (with respect to number of months)
# Keeps only stores with a full period of data.
store_monthly_complete = filter_complete_stores(store_monthly, required_months=12)
from trial_analysis import filter_complete_stores

# paste the below code in trial_analysis.py
def filter_complete_stores(store_monthly, required_months):
    months_per_store = store_monthly.groupby('STORE_NBR')['YEARMONTH'].nunique()
    complete_stores = months_per_store[months_per_store == required_months].index

    before = store_monthly['STORE_NBR'].nunique()
    filtered = store_monthly[store_monthly['STORE_NBR'].isin(complete_stores)]
    print(f"Stores with complete {required_months}-month data: {len(complete_stores)} of {before}")

    return filtered



# if that add labels isn't working, try this one

def add_bar_labels(ax, padding=3):
    for container in ax.containers:
        ax.bar_label(container, padding=padding)