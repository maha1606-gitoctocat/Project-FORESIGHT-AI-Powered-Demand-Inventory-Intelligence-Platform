# FORESIGHT – Retail Inventory Forecasting & Risk Analytics

## Project Overview

FORESIGHT is a retail analytics project designed to forecast product demand and identify inventory risks at the store-SKU level.

The project combines historical sales data, time-series features, machine learning forecasting, inventory risk analysis, and business recommendations.

## Objectives

- Forecast weekly product demand.
- Compare a machine learning forecasting model against a Seasonal Naive baseline.
- Generate an 8-week future demand forecast for 5,000 SKUs.
- Identify potential stockout and overstock risks.
- Estimate inventory value at risk.
- Provide recommended inventory actions for store-SKU combinations.

## Methodology

### 1. Data Preparation

Historical retail sales data was aggregated into weekly SKU-level demand.

The weekly dataset covers:

- Start date: 2022-01-03
- End date: 2026-01-05
- 5,000 SKUs
- 1,033,579 weekly records

### 2. Feature Engineering

The forecasting model uses:

- Lag 1 week
- Lag 4 weeks
- Lag 12 weeks
- Lag 52 weeks
- 4-week rolling mean
- 12-week rolling mean
- Month
- Week of year
- Trend

### 3. Forecasting Model

A Random Forest Regressor was used for demand forecasting.

Model configuration:

- n_estimators = 100
- max_depth = 15
- min_samples_leaf = 5
- random_state = 42

### 4. Model Validation

Rolling-origin backtesting was used to evaluate forecasting performance.

The Random Forest model was compared with a Seasonal Naive baseline.

Results:

- Random Forest WAPE: 29.88%
- Seasonal Naive WAPE: 38.23%
- WAPE improvement: 21.83%

The Random Forest model performed better than the Seasonal Naive baseline on the selected backtesting periods.

### 5. Future Forecast

An 8-week recursive forecast was generated for all 5,000 SKUs.

Forecast period:

- Start: 2026-01-12
- End: 2026-03-02

Total forecast records:

- 40,000

### 6. Inventory Risk Analysis

Forecast demand was combined with store-level inventory information.

The analysis uses:

- Stock on hand
- Reorder point
- Safety stock
- Cost price
- Forecasted 8-week demand

Stock coverage was calculated as:

Current Stock / Forecasted 8-Week Demand

Forecast-driven stockout and overstock risk classifications were then created.

### 7. Business Recommendations

Each store-SKU combination receives an inventory action:

- Reorder Now
- Watch / Replenish Soon
- Clear / Markdown
- Watch / Reduce Orders
- Healthy

### 8. Financial Exposure

The analysis estimates the inventory value associated with potential stockout and overstock exposure.

Final estimated exposure:

- Stockout value at risk: ₹182.42 crore
- Overstock value at risk: ₹124.32 crore
- Total value at stake: ₹306.73 crore

These values represent estimated inventory exposure based on the project's forecast and assumptions. They should not be interpreted as guaranteed financial losses.

## Important Limitation

The inventory dataset does not contain a supplier lead-time field.

Therefore, the stockout classification is a forecast-driven inventory risk classification rather than a true lead-time-based stockout probability.

The overstock thresholds used in the analysis are project-level decision assumptions and should be reviewed against actual business policies before operational use.

## Project Files

| File | Description |
|---|---|
| `FORESIGHT_Inventory_Forecasting.ipynb` | Complete Jupyter Notebook containing the analysis and forecasting workflow |
| `final_inventory_risk_output.csv` | Final store-SKU inventory risk output |
| `forecast_results.csv` | Historical test-set forecast results |
| `rolling_backtest_results.csv` | Rolling-origin model evaluation results |

## Tools & Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Jupyter Notebook
- Matplotlib
- Excel/CSV

## Key Outcome

The project demonstrates an end-to-end retail analytics workflow:

Historical Sales
→ Feature Engineering
→ Demand Forecasting
→ Model Validation
→ Future Forecast
→ Inventory Risk Detection
→ Financial Exposure
→ Recommended Business Action