# Gifting Customer Analytics Initiative

**An end-to-end customer analytics project: SQL Server, Python (RFM segmentation) and a two-page Power BI dashboard.**

> **Data disclosure:** this project uses the public **UCI Online Retail II** dataset (a UK online gift-ware retailer, Dec 2009 to Dec 2011). It is **not** real IKEA data. The business scenario is framed as a gifting retailer analytics initiative, and every number below comes from that public dataset.

Author: Neha Bawankar  |

---

## 1. Business Problem

A gifting retailer sells to a mix of individual customers and wholesalers, and most of its revenue arrives in a short seasonal window. The business wants to answer:

1. How much revenue and how many customers do we have, and how do they change over time?
2. Which customers are the most valuable, and which are slipping away?
3. How seasonal is the business, and which countries drive it?
4. Who should we reward, win back, or stop spending on?

## 2. Tools Used

| Tool | Purpose |
|---|---|
| **SQL Server Express** | Database engine for raw and cleaned data |
| **SQL Server Management Studio (SSMS)** | Importing files, writing and running SQL |
| **Jupyter Notebook (Python, pandas, matplotlib)** | RFM calculation, scoring and segmentation |
| **Power BI Desktop** | Interactive two-page dashboard |

## 3. Dataset

- **Source:** UCI Online Retail II (two sheets: 2009-2010 and 2010-2011).
- **Size:** 1,067,371 raw transaction rows, 8 columns (Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country).
- **Period:** 1 Dec 2009 to 9 Dec 2011 (December 2011 is a partial month).

## 4. Project Workflow

```
Raw CSV files (2 sheets)
        |
        v
SQL Server: import, combine, validate, remove duplicates   -->  RetailCleaned
        |
        v
Python (Jupyter): filter, build RFM, score, segment        -->  Transactions with RFM
        |
        v
Power BI: slicers, KPIs, charts, Revenue/Customer toggle   -->  2-page dashboard
```

### Step 1: SQL Server (data preparation)

- Imported both CSV files with the SSMS *Import Flat File* wizard and combined them with `UNION ALL` into one table (1,067,371 rows).
- Converted dates, prices and quantities safely with `TRY_CONVERT` (0 failed conversions).
- Ran data-quality checks:

| Check | Result |
|---|---|
| Rows with missing Customer ID | 243,007 (about 22.8%) |
| Rows with negative quantity (returns / cancellations) | 22,950 |
| Rows with missing description | 4,382 |
| Exact duplicate rows | 34,335 extra rows |

- Removed duplicates with a **window function**:

```sql
WITH Deduped AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY Invoice, StockCode, Description, Quantity,
                            InvoiceDate, Price, Customer_ID, Country
               ORDER BY (SELECT NULL)) AS RowNum
    FROM dbo.RetailCombined)
SELECT * INTO dbo.RetailCleaned FROM Deduped WHERE RowNum = 1;   -- 1,033,036 rows
```

- `SourceSheet` is deliberately left out of the `PARTITION BY`, because the two sheets overlap for the first days of December 2010. Keeping it in would leave about 22,000 duplicate rows.

### Step 2: Python (RFM analysis)

**Filters for customer analysis:** removed rows with no Customer ID, cancellation invoices (starting with `C`), and rows with zero or negative quantity or price.

| Stage | Rows |
|---|---|
| After SQL de-duplication | 1,033,036 |
| After removing missing customers | 797,885 |
| After removing cancellations | 779,495 |
| After removing bad quantity / price | **779,425** |

Result: **5,878 customers**, **36,969 orders**, **£17,374,804 revenue**.

**RFM definitions** (snapshot date 10 Dec 2011):

- **Recency:** days since the customer's last purchase
- **Frequency:** number of distinct invoices
- **Monetary:** total revenue

Each measure was scored 1 to 5 with `pd.qcut` (Frequency is ranked first to handle ties), then customers were assigned to segments with a `segment_customer` function:

| Segment | Rule |
|---|---|
| Champions | R >= 4, F >= 4 and M >= 4 |
| Loyal | R >= 3 and F >= 3 |
| At Risk | R <= 2 and F >= 3 |
| New | R >= 4 and F <= 2 |
| Need Attention | R = 3 and F <= 2 |
| Lost | everything else |

A customer is flagged **churned** (`IsChurned`) when Recency is more than 90 days.

### Step 3: Power BI (dashboard)

A dark-themed, two-page interactive dashboard with six slicers (Month, Quarter, Year, Country, Segment, Is Churned). Every card and chart responds to every slicer.

**Page 1: Business Overview**
- KPI cards: Total Customers, Total Revenue, Churned %, Avg Customer Value
- **Revenue / Customer toggle** (a Field Parameter) that switches the whole page between revenue and customer numbers
- Total Revenue / Customers by Segment (donut), Retention by Segment, and trends by Month, Quarter and Year

**Page 2: RFM Analysis**
- Segment Performance Summary table (customers, revenue, average R, F and M scores)
- **Segment / Country toggle**
- Segment by Avg Customer Value, and Churned % by Month, Quarter and Year

`<add screenshots here: /images/page1_revenue.png, page1_customer.png, page2_segment.png, page2_country.png>`

## 5. Key Findings

| Finding | Number |
|---|---|
| Total revenue / customers / orders | $17.37M / 5,878 / 36,969 |
| Average revenue per customer / per order | $2,956 / $470 |
| **Champions** | 1,291 customers (22%) generate **68.1%** of revenue |
| Champions' average customer value | $9,169, about 5x the next segment |
| **Churn rate** (no purchase in 90+ days) | **50.85%** (2,989 customers) |
| **Lost** customers | 1,522 customers (26%) but only **3.8%** of revenue |
| **At Risk** customers | 821 customers holding **$1.59M** (9.1% of revenue): the best win-back target |
| **Seasonality** | Revenue peaks in Oct and Nov of both years (Nov 2010: £1.17M, Nov 2011: £1.16M); Q4 is about 36% of all revenue |
| **Geography** | United Kingdom brings in about 83% of revenue (£14.39M); next are EIRE, Netherlands and Germany |
| Churn by year | 40.2% (2009), 56.3% (2010), 31.5% (2011) |

## 6. Business Recommendations

1. **Protect Champions:** early access, loyalty rewards and personal outreach before the Oct to Nov gifting peak.
2. **Win back At Risk customers:** a targeted campaign in September, ahead of the peak season, since this group still holds £1.59M in revenue.
3. **Cap spending on Lost customers:** they are 26% of customers but under 4% of revenue.
4. **Convert New customers:** a second-purchase offer within 30 days to move them toward Loyal.
5. **Plan inventory and staffing for Q4**, which carries about a third of annual revenue.

## 7. Limitations (please read)

- The 90-day churn rule is a business assumption. This is a gifting business, so many customers buy only around holidays, which pushes the churn rate up.
- Segments are built from the same period they are analysed in, so retention by segment is partly circular (At Risk and Lost customers are inactive by definition).
- **243,007 rows (22.8%) have no Customer ID** (mostly guest checkouts). They are included in sales totals but excluded from customer analysis.
- December 2011 is a partial month (data ends 9 Dec 2011).
- Some very large buyers are probably wholesalers, which skews averages. EIRE, for example, has only 5 customers.
- The dataset is one retailer's public data, so results are not IKEA results.

## 8. Repository Structure

```
Gifting-Customer-Analytics/
|-- data/
|   |-- online_retail_II_page_1_2.csv
|   |-- online_retail_II_page_2_2.csv
|-- sql/
|   |-- 01_Database_Setup_and_Cleaning.sql
|-- notebooks/
|   |-- 02_RFM_Segmentation.ipynb
|-- powerbi/
|   |-- Gifting_Customer_Analytics.pbix
|   |-- Dark_Theme.json
|-- images/
|   |-- dashboard screenshots
|-- README.md
```

## 9. How to Reproduce

1. Install SQL Server Express and SSMS. Create the database and import both CSV files (*Tasks > Import Flat File*).
2. Run `sql/01_Database_Setup_and_Cleaning.sql` to build `RetailCleaned`. Export it as CSV.
3. Open `notebooks/02_RFM_Segmentation.ipynb` in Jupyter and run all cells. It writes the transactions-with-RFM file.
4. Open the `.pbix` in Power BI Desktop, point the data source to the exported CSV, and import `Dark_Theme.json` (*View > Themes > Browse for themes*).

## 10. Skills Demonstrated

SQL (CTEs, window functions, `TRY_CONVERT`, data validation) | Python (pandas, `qcut`, custom functions, matplotlib) | RFM segmentation | DAX (measures, calculated columns, Field Parameters) | Dashboard design and storytelling | Business recommendations

## 11. Data Source

Chen, D. (2012). *Online Retail II* dataset, UCI Machine Learning Repository.
