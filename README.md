# Demand Forecasting & Risk-Aware Inventory Optimization

This project implements a multi-step forecasting framework to quantify the impact of exogenous signals on demand variability. By comparing an autoregressive baseline with a feature-enriched "Full Model," the analysis demonstrates how reducing forecast variance directly informs safety stock positioning and risk mitigation in supply chain operations.

---

## 1. Project Overview
Traditional time-series models often lag during sudden market shifts. This repository explores the integration of **synthetic external signals** (promotions, supply disruptions, and specific events) into a linear regression framework to improve responsiveness to non-linear shocks.

---

## 2. Code Structure & Components

The implementation is designed as a modular pipeline, transitioning from raw data simulation to actionable inventory insights.

### **I. Data & Modeling Foundation (Sections 1–4)**
* **Section 1: Data Generation:** Simulates a 25-SKU portfolio over 730 days using deterministic elements (trend + seasonality) and stochastic noise.
* **Section 2: Feature Engineering:** Generates `lag_1` and `lag_7` to capture momentum, alongside 7-day rolling means/STDs for local context.
* **Section 3 & 4: Model Training:** Implements a chronological split (80/20) to train a **Baseline Model** (historical data only) and a **Full Model** (historical + external signals).

### **II. Performance & Error Analytics (Sections 5–8)**
* **Section 5: Performance Metrics:** Calculates **MAE** and **RMSE** to quantify the magnitude of error.
* **Section 6: Variance Reduction:** Compares the variance ($\sigma^2$) of residuals to measure the "stability" gain of the Full Model.
* **Section 7: Feature Impact:** Extracts regression coefficients to rank the influence of promotions, disruptions, and events on demand volume.
* **Section 8: High-Uncertainty SKUs:** Aggregates errors at the SKU level to identify high-risk products requiring manual intervention or higher buffers.

### **III. Scenario Simulation & Inventory Logic (Sections 9–11)**
* **Section 9: Scenario Engine:** Stress-tests the supply chain by permuting multipliers and external flags to see "What-If" outcomes.
* **Section 10: Safety Stock Calculation:** Translates forecast uncertainty into physical units using the formula: $Safety Stock = Z \times \sigma_d \times \sqrt{L}$.
* **Section 11: Visualization:** Generates the diagnostic plots used for the technical analysis below.

---

## 3. Technical Analysis of Results

### Plot 1: SKU 0 Forecast vs. Actual (Full Model)
![SKU 0 Forecast vs Actual](Forcast_vs_actual.png)
* **Observation:** The predicted series (Orange) achieves high phase-alignment with actual demand (Blue), specifically tracking 7-day seasonality and the magnitude of non-periodic spikes.
* **Implications:**
    * **Signal Capture:** The model successfully deconvolves "signal" from "noise," prioritizing structured variance over stochastic residuals.
    * **Responsiveness:** Alignment at peaks suggests coefficients for exogenous features are well-calibrated, allowing the model to "anticipate" shifts.
    * **Inventory Impact:** High tracking accuracy reduces the requirement for "speculative" inventory.

### Plot 2: SKU 0 Baseline vs. Full Model Comparison
![SKU 0 Baseline vs Full Model](Baseline_vs_full_model.png)
* **Observation:** The Baseline (Orange) follows the mean trend but underestimates volatility. The Full Model (Green) exhibits significantly higher sensitivity to extreme values.
* **Implications:**
    * **Information Gain:** Visual evidence that Baseline models suffer from "regression to the mean," while the Full Model captures the true amplitude of demand.
    * **Bias Mitigation:** The Baseline exhibits a downward bias during promotions; the Full Model corrects this, preventing stockouts during high-revenue periods.

### Plot 3: Error Distribution Comparison
![Error Distribution Comparison](Error_distribution.png)
* **Observation:** The Full Model (Orange) shows a higher density at the 0–5 error bin and a "thinner tail" compared to the Baseline (Blue).
* **Implications:**
    * **Heteroscedasticity Reduction:** Incorporating signals reduces residual variance. The Baseline’s "fat tail" (errors >30) represents high-risk failure points.
    * **Reliability:** A zero-centered error distribution makes the Full Model a more reliable point estimate for automated ordering.

### Plot 4: Scenario Impact: Demand vs. Promotion & Multiplier
![Scenario Impact](Scnario_impact.png)
* **Observation:** Structured sensitivity analysis shows linear growth across multipliers with a consistent additive "lift" from promotions.
* **Implications:**
    * **Decision Support:** Allows stakeholders to quantify expected load (e.g., "What is the load if we have 20% growth AND a promotion?").
    * **Linearity Validation:** Confirms the model has learned a stable, generalizable effect for marketing activities.

### Plot 5: Safety Stock Distribution Across SKUs
![Safety Stock Distribution Across SKUs](Safty_stock.png)
* **Observation:** A histogram of safety stocks (52 to 60 units), showing a multi-modal distribution of risk.
* **Implications:**
    * **Risk Quantization:** Translates uncertainty ($\sigma$) into capital ($units$).
    * **Operational Optimization:** Improving the forecast shifts this distribution left, **freeing up working capital** without increasing stockout risk.

---

## 4. Key Takeaways
1.  **Exogenous signals are primary variance reducers:** Lags capture the "rhythm," but signals capture the "shocks."
2.  **Uncertainty is a Cost:** Every unit of forecast error variance contributes to a higher Safety Stock requirement.
3.  **Model Robustness:** Scenario simulation transforms static predictions into proactive risk management tools.

## 5. Tech Stack
* **Python:** Pandas, NumPy, Scikit-learn, Matplotlib

## 6. How to Run
```bash
pip install -r requirements.txt
# Run the analysis script or open the notebook
python notebooks/demand_forecasting_analysis.py

Author Lucy Han