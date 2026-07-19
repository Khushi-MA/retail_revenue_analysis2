# Chip Category Analysis — Initial Findings

---

# Executive Summary

This report analyses chip transactions from July 2018 to June 2019 alongside customer loyalty data to identify purchasing patterns and key customer segments.

While Retirees and Singles/Couples generate the highest total sales, this is largely due to their larger customer base. On a per-customer basis, Older and Young Families are the most valuable segments, driven by higher purchase frequency rather than differences in price, pack size, or brand preference.

Sales show a clear seasonal pattern, peaking in December and declining sharply in February. These findings suggest focusing marketing efforts on increasing purchase frequency among Family segments and planning inventory around seasonal demand.

---

# 1. Data Preparation

## Transaction Data

* Converted Excel serial dates to standard date format.
* Removed two anomalous transactions with quantities of 200 units.
* Standardised product names and extracted pack weight into a separate column.
* Created a standardised brand mapping to correct naming inconsistencies.
* Verified a one-to-one relationship between product numbers and product names.
* Removed one duplicate transaction.
* Excluded non-chip products (e.g., dips, salsas, crackers, papadums) after manual review.

## Customer Data

* No missing values or duplicate loyalty records were identified.
* Confirmed all transaction loyalty cards matched customer records.
* Merged customer and transaction data and filtered to chip products only.

---

# 2. Analysis Approach

Customers were segmented using the combination of:

* **Lifestage (7 categories)**
* **Premium Tier (Budget, Mainstream, Premium)**

This produced 21 customer segments.

Metrics analysed included:

* Total sales
* Customer count
* Units purchased
* Average spend per customer
* Average units per customer
* Average price per unit
* Average pack weight
* Brand share
* Pack size mix (Small, Standard, Large)

Brand-level sales, unit, and transaction metrics were also calculated.

---

# 3. Key Findings

## 3.1 Family segments deliver the highest customer value

Although Retirees and Singles/Couples contribute the most total sales, they also represent the largest share of customers.

| Lifestage              | Share of Customers |
| ---------------------- | ------------------ |
| Retirees               | 20.4%              |
| Older Singles/Couples  | 20.2%              |
| Young Singles/Couples  | 19.7%              |
| Older Families         | 13.5%              |
| Young Families         | 12.7%              |
| Midage Singles/Couples | 10.0%              |
| New Families           | 3.5%               |

When measured by average spend per customer, Older and Young Families consistently outperform other segments across all premium tiers.

---

## 3.2 Higher value comes from buying more often

Family segments spend more because they purchase chips more frequently.

Key drivers such as price, pack size, and brand preference show little variation across segments:

* Average price per unit remains consistent (~$3.70–$4.00).
* Standard packs (150–200g) dominate across all segments.
* Kettle, Smiths, Doritos, and Pringles are the leading brands in nearly every segment.

As a result, purchase frequency—not product choice—is the primary driver of higher customer value.

---

## 3.3 Strong seasonal demand pattern

| Month    | Sales ($) |
| -------- | --------: |
| Jul 2018 |   151,293 |
| Aug 2018 |   144,036 |
| Sep 2018 |   146,970 |
| Oct 2018 |   150,118 |
| Nov 2018 |   146,360 |
| Dec 2018 |   153,800 |
| Jan 2019 |   148,621 |
| Feb 2019 |   137,520 |
| Mar 2019 |   152,560 |
| Apr 2019 |   146,134 |
| May 2019 |   143,080 |
| Jun 2019 |   147,048 |

* December recorded the highest sales, likely driven by holiday demand.
* February experienced the largest decline.
* Sales recovered strongly in March.
* The trend was consistent across customer segments, indicating category-wide seasonality.

*Note: Findings are based on a single 12-month period and should be validated against additional years where available.*

---

# 4. Recommendations

### 1. Focus on Family Segments

Target Older and Young Families with loyalty programs, multi-buy offers, and frequency-based promotions to encourage repeat purchases.

### 2. Align Inventory with Seasonal Demand

Increase stock levels before the November–December peak and consider promotions in February to offset weaker demand.

### 3. Time Campaigns Around Seasonality

Since segment preferences are similar, product launches and marketing campaigns should be scheduled around peak demand periods rather than specific customer segments.

### 4. Maintain Current Pack Size Mix

Demand for Standard packs remains dominant across all segments, suggesting no major pack-size adjustments are required.

---

# 5. Limitations

* Analysis covers only one year of data.
* Some product exclusions required manual classification due to the absence of a chip/non-chip flag.
* Two unusually large transactions were removed as likely anomalies.

---

# Supporting Visualisations

* Sales by segment
* Average spend per customer by segment
* Pack size mix by segment
* Brand sales and transaction share
* Top products by sales and units sold
* Monthly sales trend
* Customer distribution by lifestage
* Customer distribution by premium tier
* Top customers by total sales
