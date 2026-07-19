# Store Trial Evaluation — Initial Findings

# Executive Summary

A new store layout was trialled in three stores (77, 86, and 88) between February and April 2019, with the goal of determining whether it should be rolled out chain-wide. To isolate the layout's true effect from normal month-to-month variation and seasonality, each trial store was matched against a statistically similar control store — one that was not exposed to the new layout, but tracked the trial store closely in the seven months beforehand. All three trial stores showed a statistically significant sales increase in at least two of the three trial months, driven primarily by more customers shopping rather than existing customers spending more per visit. However, the pattern differed by store: Store 77's uplift built steadily over the trial; Store 86 peaked sharply in a single month; and Store 88's uplift faded by the final month, with its result carrying more uncertainty due to a weaker control-store match. Overall, the trial provides reasonably strong evidence to support a wider rollout, with a recommendation to investigate Store 88's fading effect and Store 86's single-month pattern before committing fully.

# 1. Methodology

## 1.1 Why a Control Store Comparison Is Necessary

Simply comparing a trial store's sales before and after the layout change would not isolate the layout's effect — seasonal trends, national promotions, or other unrelated factors occurring during the same period could easily be mistaken for the layout's impact. A control store — one that was not exposed to the new layout but otherwise behaves similarly to the trial store — provides a baseline for what would likely have happened without the change, allowing the layout's actual effect to be isolated.

## 1.2 Control Store Selection

Using seven months of pre-trial data (July 2018 – January 2019), each trial store was compared against every other eligible store using two combined measures:

- Pearson correlation — whether a candidate store's monthly pattern rose and fell in step with the trial store, regardless of scale.
- Magnitude distance — whether a candidate store's raw sales and customer counts were close in size to the trial store, using a standardised distance score (1 minus normalised distance from the trial store, averaged across all pre-trial months).

These two measures were combined, and averaged across both Total Sales and Number of Customers, to produce a single similarity score per candidate store. The highest-scoring store was selected as the control for each trial store. Stores with incomplete data across the required pre-trial or trial months were excluded from consideration.

## 1.3 Selected Control Stores

| Trial Store | Control Store | Similarity Score | Visual Pre-Trial Match |
|------------|--------------|-----------------|------------------------|
| 77 | 233 | 0.938 | Good — lines track closely, some divergence |
| 86 | 155 | 0.924 | Strong — near-identical pre-trial pattern |
| 88 | 238 | 0.727 | Weaker — noticeably less parallel pre-trial pattern |

Each control store's raw values were scaled to match the trial store's average pre-trial level before comparison, ensuring differences reflect actual behavioural change rather than a pre-existing size gap between the two stores.

## 1.4 Significance Testing

For each trial month, the trial store's actual value was compared against its scaled control using a percentage difference. The typical (pre-trial) month-to-month variation between each trial store and its control was used to calculate a t-value for each trial-period difference, tested against a 95% confidence threshold. This determines whether an observed difference is large enough to represent a genuine effect, rather than normal noise.

# 2. Findings by Store

## 2.1 Store 77 (Control: 233)

| Month | Sales % Diff | Sales Significant? | Customers % Diff | Customers Significant? |
|---------|------------|------------------|----------------|----------------------|
| Feb 2019 | -11.2% | No | -4.6% | No |
| Mar 2019 | +33.9% | Yes | +26.2% | Yes |
| Apr 2019 | +72.8% | Yes | +65.1% | Yes |

Store 77 shows no significant effect in the first trial month, followed by a strong and accelerating uplift in March and April. Since customer count and sales move together across the same months, the uplift is being driven by more customers shopping at the store, not by existing customers spending more per visit. This pattern is consistent with a layout change that takes a short period to influence customer behaviour before producing a strong, sustained effect.

## 2.2 Store 86 (Control: 155)

| Month | Sales % Diff | Sales Significant? | Customers % Diff | Customers Significant? |
|---------|------------|------------------|----------------|----------------------|
| Feb 2019 | +5.4% | No | +12.2% | Yes |
| Mar 2019 | +32.2% | Yes | +23.4% | Yes |
| Apr 2019 | +4.8% | No | +7.0% | Yes |

Store 86 shows a different pattern: customer numbers were significantly higher in all three trial months, but this only translated into a significant sales increase in March. This suggests the new layout consistently drew more customers into the store throughout the trial, but only converted into a clear sales lift in one specific month — worth investigating further, as it may point to a promotional event, stocking difference, or other factor specific to March.

## 2.3 Store 88 (Control: 238)

| Month | Sales % Diff | Sales Significant? | Customers % Diff | Customers Significant? |
|---------|------------|------------------|----------------|----------------------|
| Feb 2019 | +24.8% | Yes | +14.9% | Yes |
| Mar 2019 | +39.7% | Yes | +37.0% | Yes |
| Apr 2019 | +8.4% | No | +7.9% | No |

Store 88 shows the opposite trajectory to Store 77: a strong, significant uplift in the first two trial months that fades by April, ending statistically indistinguishable from its control. Store 88's control match was also the weakest of the three (similarity score 0.727, versus 0.92+ for the other two), so this result should be treated with more caution — some of the apparent effect, and its fading pattern, may reflect a less reliable baseline rather than a true decline in the layout's impact.

# 3. Overall Assessment

All three trial stores recorded a statistically significant sales increase in at least two of the three trial months, and in every case where sales rose significantly, customer counts rose significantly too — indicating the layout's effect operates by attracting more shopping customers, not by increasing spend per existing customer. This is a consistent, credible signal across independently-matched stores and control pairs.

That said, the three stores tell three different stories about how the effect develops over time — building (77), peaking mid-trial (86), and fading (88) — and Store 88's result rests on a weaker control match. This variation is worth understanding before committing to a full rollout, rather than treating the trial as a single uniform result.

# 4. Recommendations

**1. Proceed with a broader rollout, on the strength of consistent, significant sales gains across all three trial stores.** The evidence supports the new layout having a genuine positive effect on customer counts and sales, not merely reflecting normal variation.

**2. Investigate Store 88 further before treating its result as equivalent to 77 and 86.** Given its weaker control match and the fading effect by April, consider re-running the comparison with an alternative control store, or gathering additional months of post-trial data, to confirm whether the effect genuinely diminished or whether this reflects noise in a less reliable baseline.

**3. Look into what happened specifically in March at Store 86.** Since customer counts were elevated in all three months but sales only rose significantly in March, understanding this store's March-specific circumstances (e.g. a local promotion, stock availability) could reveal an additional lever to combine with the layout change during a wider rollout.

**4. Track customer counts, not just sales, when monitoring a wider rollout.** Since the layout's effect operates through attracting more customers rather than increasing spend per visit, customer footfall is the more sensitive early indicator of whether the layout is working in a newly-rolled-out store.

# 5. Limitations

- Only one control store was matched per trial store; a more robust approach could consider blending multiple close-matching control stores to reduce reliance on any single comparison.
- The significance test assumes pre-trial variability is a fair representation of "normal" month-to-month noise; with only seven pre-trial months, this estimate is based on a small sample.
- Store 88's control match (similarity score 0.727) was visibly less parallel than the other two pairs in the pre-trial period, reducing confidence in its trial-period comparison specifically.
- This analysis covers a single three-month trial window; a longer trial or post-rollout monitoring period would give a clearer picture of whether effects are sustained.