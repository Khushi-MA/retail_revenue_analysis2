# Pre-trial period: July 2018 – January 2019 (7 months) — used to select control stores
# Trial period: February–April 2019 (3 months) — used to measure impact
# Post-trial: May–June 2019 — not used in this analysis
import matplotlib.pyplot as plt
import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# ============================================================
# SECTION 1: Build & filter store-level monthly data
# ============================================================

def build_store_monthly_summary(df):
    """Builds monthly per-store metrics table."""
    df = df.copy()
    df['YEARMONTH'] = df['DATE'].dt.to_period('M').astype(str)
    store_monthly = (
        df.groupby(['STORE_NBR', 'YEARMONTH'])
        .agg(
            TOTAL_SALES=('TOT_SALES', 'sum'),
            N_CUSTOMERS=('LYLTY_CARD_NBR', 'nunique'),
            N_TRANSACTIONS=('TXN_ID', 'nunique'),
            N_UNITS=('PROD_QTY', 'sum'),
        )
        .reset_index()
    )
    store_monthly['AVG_TXN_PER_CUSTOMER'] = store_monthly['N_TRANSACTIONS'] / store_monthly['N_CUSTOMERS']
    store_monthly['AVG_SALES_PER_CUSTOMER'] = store_monthly['TOTAL_SALES'] / store_monthly['N_CUSTOMERS']
    print(f"Store-monthly summary built: {store_monthly.shape[0]} rows, {store_monthly['STORE_NBR'].nunique()} stores")
    return store_monthly


def filter_stores_with_required_periods(store_monthly, pre_trial_months, trial_months):
    """Keeps only stores with complete data across the pre-trial AND trial months (ignores months outside these windows)."""
    months_present = store_monthly.groupby('STORE_NBR')['YEARMONTH'].apply(set)
    has_full_pretrial = months_present.apply(lambda m: set(pre_trial_months).issubset(m))
    has_full_trial = months_present.apply(lambda m: set(trial_months).issubset(m))
    valid_stores = months_present[has_full_pretrial & has_full_trial].index
    before = store_monthly['STORE_NBR'].nunique()
    filtered = store_monthly[store_monthly['STORE_NBR'].isin(valid_stores)]
    print(f"Stores with complete pre-trial + trial period data: {len(valid_stores)} of {before}")
    return filtered


def check_complete_data_in_trial_stores(store_monthly_complete, trial_stores):
    """Confirms the specified trial stores survived the completeness filter."""
    found_stores = set(store_monthly_complete[store_monthly_complete['STORE_NBR'].isin(trial_stores)]['STORE_NBR'].unique())
    if found_stores == set(trial_stores):
        print(f"All the required trial stores {trial_stores} have complete data")
    else:
        print(f"Missing trial stores: {set(trial_stores) - found_stores}")


# ============================================================
# SECTION 2: Control store selection (correlation + magnitude distance)
# ============================================================

def calculate_correlation(pre_trial, metric_col, trial_store):
    """Pearson correlation of each candidate store's monthly pattern vs. the trial store's, over the pre-trial period."""
    pivot = pre_trial.pivot(index='YEARMONTH', columns='STORE_NBR', values=metric_col)
    trial_series = pivot[trial_store]
    corr = pivot.corrwith(trial_series)
    return corr.rename('corr_score')


def calculate_magnitude_distance(pre_trial, metric_col, trial_store):
    """Scaled closeness (0-1) of each candidate store's raw values vs. the trial store's, averaged over the pre-trial period."""
    pivot = pre_trial.pivot(index='YEARMONTH', columns='STORE_NBR', values=metric_col)
    trial_series = pivot[trial_store]
    distance = pivot.subtract(trial_series, axis=0).abs()
    min_dist = distance.min(axis=1)
    max_dist = distance.max(axis=1)
    scaled = distance.subtract(min_dist, axis=0).div(max_dist - min_dist, axis=0)
    score = 1 - scaled
    return score.mean(axis=0).rename('magnitude_score')


def find_control_store(pre_trial, trial_store, exclude_stores):
    """Combines correlation + magnitude distance across TOTAL_SALES and N_CUSTOMERS to pick the best-matching control store."""
    metrics = ['TOTAL_SALES', 'N_CUSTOMERS']
    combined_scores = []
    for metric in metrics:
        corr = calculate_correlation(pre_trial, metric, trial_store)
        mag = calculate_magnitude_distance(pre_trial, metric, trial_store)
        metric_score = (corr + mag) / 2
        combined_scores.append(metric_score)
    overall_score = sum(combined_scores) / len(combined_scores)
    overall_score = overall_score.drop(index=exclude_stores, errors='ignore')
    best_control = overall_score.idxmax()
    print(f"Trial store {trial_store} -> best control store: {best_control} (score: {overall_score.max():.4f})")
    return best_control, overall_score.sort_values(ascending=False)


# ============================================================
# SECTION 3: Trial vs. control comparison
# ============================================================

def scale_control_store(pre_trial, trial_period, trial_store, control_store, metric_col):
    """Scales the control store's trial-period values using the pre-trial ratio, so it represents the trial store's 'no-change' baseline."""
    trial_pretrial_avg = pre_trial.loc[pre_trial['STORE_NBR'] == trial_store, metric_col].mean()
    control_pretrial_avg = pre_trial.loc[pre_trial['STORE_NBR'] == control_store, metric_col].mean()
    scaling_factor = trial_pretrial_avg / control_pretrial_avg
    control_trial = trial_period[trial_period['STORE_NBR'] == control_store].copy()
    control_trial[f'SCALED_{metric_col}'] = control_trial[metric_col] * scaling_factor
    print(f"Scaling factor for {metric_col} ({trial_store} vs {control_store}): {scaling_factor:.4f}")
    return control_trial


def compare_trial_vs_control(pre_trial, trial_period, trial_store, control_store, metric_col):
    """Computes the % difference between the trial store's actual values and its scaled control, per trial month."""
    scaled_control = scale_control_store(pre_trial, trial_period, trial_store, control_store, metric_col)
    trial_data = trial_period[trial_period['STORE_NBR'] == trial_store]
    comparison = trial_data[['YEARMONTH', metric_col]].merge(
        scaled_control[['YEARMONTH', f'SCALED_{metric_col}']],
        on='YEARMONTH'
    )
    comparison['PCT_DIFF'] = (
        (comparison[metric_col] - comparison[f'SCALED_{metric_col}']) / comparison[f'SCALED_{metric_col}']
    ) * 100
    print(f"\n{metric_col} — Store {trial_store} vs scaled control {control_store}:")
    print(comparison)
    return comparison


# ============================================================
# SECTION 4: Statistical significance testing
# ============================================================

def test_significance(pre_trial, trial_period, trial_store, control_store, metric_col):
    """Tests whether each trial-month % difference exceeds normal pre-trial noise, using a one-tailed t-test."""
    trial_pretrial_avg = pre_trial.loc[pre_trial['STORE_NBR'] == trial_store, metric_col].mean()
    control_pretrial_avg = pre_trial.loc[pre_trial['STORE_NBR'] == control_store, metric_col].mean()
    scaling_factor = trial_pretrial_avg / control_pretrial_avg

    pretrial_control = pre_trial[pre_trial['STORE_NBR'] == control_store].copy()
    pretrial_control[f'SCALED_{metric_col}'] = pretrial_control[metric_col] * scaling_factor

    pretrial_trial = pre_trial[pre_trial['STORE_NBR'] == trial_store]
    pretrial_compare = pretrial_trial[['YEARMONTH', metric_col]].merge(
        pretrial_control[['YEARMONTH', f'SCALED_{metric_col}']], on='YEARMONTH'
    )
    pretrial_compare['PCT_DIFF'] = (
        (pretrial_compare[metric_col] - pretrial_compare[f'SCALED_{metric_col}']) / pretrial_compare[f'SCALED_{metric_col}']
    ) * 100

    std_dev = pretrial_compare['PCT_DIFF'].std()
    degrees_freedom = len(pretrial_compare) - 1

    trial_comparison = compare_trial_vs_control(pre_trial, trial_period, trial_store, control_store, metric_col)
    trial_comparison['T_VALUE'] = trial_comparison['PCT_DIFF'] / std_dev

    critical_t = stats.t.ppf(0.95, degrees_freedom)
    trial_comparison['SIGNIFICANT'] = trial_comparison['T_VALUE'].abs() > critical_t

    print(f"\nPre-trial noise level (std dev of % diff): {std_dev:.2f}%")
    print(f"Critical t-value (95% confidence, df={degrees_freedom}): {critical_t:.3f}")
    print(trial_comparison[['YEARMONTH', 'PCT_DIFF', 'T_VALUE', 'SIGNIFICANT']])

    return trial_comparison


# ============================================================
# SECTION 5: Visualizations
# ============================================================

def plot_trial_vs_control_pretrial(pre_trial, trial_store, control_store, metric_col, output_dir):
    """Plots trial vs. control's raw (unscaled) values over the pre-trial period, to visually validate the match."""
    subset = pre_trial[pre_trial['STORE_NBR'].isin([trial_store, control_store])]
    fig, ax = plt.subplots(figsize=(10, 5))
    for store, label, color in [(trial_store, 'Trial', 'crimson'), (control_store, 'Control', 'steelblue')]:
        store_data = subset[subset['STORE_NBR'] == store].sort_values('YEARMONTH')
        ax.plot(store_data['YEARMONTH'], store_data[metric_col], marker='o', label=f'{label} (Store {store})', color=color)
    ax.set_title(f'Pre-Trial {metric_col}: Store {trial_store} vs Control {control_store}')
    ax.set_xlabel('Month')
    ax.set_ylabel(metric_col)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(f"{output_dir}/pretrial_check_{trial_store}_vs_{control_store}_{metric_col}.png", dpi=150)
    plt.close(fig)
    print(f"Saved: pretrial_check_{trial_store}_vs_{control_store}_{metric_col}.png")


def plot_trial_vs_scaled_control(pre_trial, trial_period, trial_store, control_store, metric_col, significance_df, output_dir):
    """Plots trial vs. scaled control across the full timeline (pre-trial + trial), with the trial period shaded and significant months starred."""
    all_months = pd.concat([pre_trial, trial_period])
    trial_data = all_months[all_months['STORE_NBR'] == trial_store].sort_values('YEARMONTH')
    control_data = all_months[all_months['STORE_NBR'] == control_store].sort_values('YEARMONTH')

    trial_pretrial_avg = pre_trial.loc[pre_trial['STORE_NBR'] == trial_store, metric_col].mean()
    control_pretrial_avg = pre_trial.loc[pre_trial['STORE_NBR'] == control_store, metric_col].mean()
    scaling_factor = trial_pretrial_avg / control_pretrial_avg
    control_data = control_data.copy()
    control_data[f'SCALED_{metric_col}'] = control_data[metric_col] * scaling_factor

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(trial_data['YEARMONTH'], trial_data[metric_col], marker='o', label=f'Trial (Store {trial_store})', color='crimson', linewidth=2)
    ax.plot(control_data['YEARMONTH'], control_data[f'SCALED_{metric_col}'], marker='o', label=f'Scaled Control (Store {control_store})', color='steelblue', linewidth=2)

    trial_months = trial_period['YEARMONTH'].unique()
    ax.axvspan(trial_months[0], trial_months[-1], color='yellow', alpha=0.15, label='Trial Period')

    sig_months = significance_df.loc[significance_df['SIGNIFICANT'], 'YEARMONTH']
    for month in sig_months:
        y_val = trial_data.loc[trial_data['YEARMONTH'] == month, metric_col].values[0]
        ax.annotate('*', (month, y_val), textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=20, color='darkgreen', fontweight='bold')

    ax.set_title(f'Store {trial_store} vs Scaled Control {control_store} — {metric_col}\n(* = statistically significant month)')
    ax.set_xlabel('Month')
    ax.set_ylabel(metric_col)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(f"{output_dir}/trial_vs_control_{trial_store}_{metric_col}.png", dpi=150)
    plt.close(fig)
    print(f"Saved: trial_vs_control_{trial_store}_{metric_col}.png")