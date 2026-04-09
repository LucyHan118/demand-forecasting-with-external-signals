# Demand Forecasting & Risk-Aware Inventory Optimization
**Author:** Lucy Han

---

## 1. Project Overview
Traditional time-series models often suffer from lag in responding to sudden market changes, as they rely primarily on historical demand. This project explores how incorporating **external signals** (e.g., promotions, disruptions, and events) can improve forecast accuracy and reduce uncertainty.

To evaluate this, I compare:
- A **Baseline Model** using only historical demand features
- A **Full Model** that includes both historical features and external signals

The objective is to quantify how much these additional signals improve predictions and how that translates into more efficient inventory decisions.

---

## 2. Code Structure & Components

The implementation is designed as a modular pipeline, moving from synthetic data generation to actionable inventory insights.

### **I. Data & Modeling Foundation (Sections 1–4)**
* **Section 1: Configuration & Reproducibility:** Establishes the environment using `np.random.seed(42)` to ensure synthetic data and results remain consistent and reproducible.
* **Section 2: Synthetic Data Generation:** Simulates a 25-SKU portfolio over 730 days using a linear additive structure:  
  `$Demand = Baseline + Trend + Seasonality + Signals + Noise$`.  
  This creates a controlled “ground truth,” allowing us to evaluate how well the model recovers underlying demand drivers.
* **Section 3: Feature Engineering:** Generates `lag_1` and `lag_7` to capture temporal momentum, along with 7-day rolling means and standard deviations to provide local statistical context.
* **Section 4: Validation Strategy:** Implements a chronological 80/20 split to simulate forward-looking forecasting, ensuring the model is evaluated on unseen future data and avoiding leakage.

---

### **II. Performance & Error Analytics (Sections 5–8)**
* **Section 5: Model Training & Comparison:** Trains both a **Baseline Model** (historical features only) and a **Full Model** (historical + external signals) to isolate the contribution of environmental variables.
* **Section 6: SKU Comparison Selection:** Identifies “Peaceful” (low signal frequency) and “Active” (high signal frequency) SKUs to evaluate performance across different volatility levels.
* **Section 7: Scenario Simulation Logic:** Builds a “what-if” framework to test the model under different market conditions (e.g., demand multipliers and signal combinations), generating multiple possible demand scenarios.
* **Section 8: Results Demonstration:** Translates model outputs (MAE, RMSE, variance) into business-relevant metrics, including side-by-side safety stock comparisons.

---

## 3. Detailed Numerical Analysis

### **Table 1: Global Model Performance**
```
MODEL PERFORMANCE
-----------------------------------------
Baseline  -> MAE: 6.72, RMSE: 8.81
Full Model-> MAE: 5.68, RMSE: 7.16
MAE Improvement:  15.40%
RMSE Improvement: 18.72%
```

* **Interpretation:**  
The Full Model improves both average error (MAE) and large-error sensitivity (RMSE). The stronger RMSE improvement suggests it handles demand spikes and shocks more effectively.

---

### **Table 2: Variance Reduction**
```
VARIANCE REDUCTION
--------------------------------------------
Baseline Var: 77.60 | Full Model Var: 51.24
Total Noise Reduction: 33.97%
```

* **Interpretation:**  
The model explains about one-third of the variability that would otherwise appear as noise, reducing uncertainty in demand estimates and improving planning reliability.

---

### **Table 3: Feature Impact (Weights)**
```
FEATURE IMPACT (WEIGHTS)
-------------------------------
          feature       coef
5      disruption -20.090371
4       promotion  14.492357
6           event  10.286007
1           lag_7   0.475327
2  rolling_mean_7   0.298572
0           lag_1   0.212158
3   rolling_std_7   0.039911

HIGH-UNCERTAINTY SKUs (TOP ERRORS)
-----------------------------------
sku   error (float64)
7     6.233773
9     6.181504
17    6.048237
18    6.025433
21    6.022568
```

* **Interpretation:**  
External signals (disruptions, promotions, events) have a stronger impact than short-term historical features. The higher weight of `lag_7` relative to `lag_1` also indicates a weekly demand pattern.

---

### **Table 4: Scenario Analysis (Active SKU 3)**
```
SCENARIO ANALYSIS (ACTIVE SKU 3)
---------------------------------------------------
    multiplier  promotion  disruption  avg_demand
0          0.8          0           0   85.366878
1          0.8          1           0   96.960764
2          0.8          0           1   69.294581
3          0.8          1           1   80.888467
4          1.0          0           0  106.708598
5          1.0          1           0  121.200955
6          1.0          0           1   86.618226
7          1.0          1           1  101.110584
8          1.2          0           0  128.050317
9          1.2          1           0  145.441146
10         1.2          0           1  103.941871
11         1.2          1           1  121.332700
```

* **Interpretation:**  
Demand ranges from ~69 to ~145 units depending on conditions. This provides a useful range for planning inventory and capacity under uncertainty.

---

### **Table 5: Safety Stock Comparison**
```
SAFETY STOCK COMPARISON (PEACEFUL VS ACTIVE)
------------------------------------------------
SKU          SKU 2 (Peaceful)  SKU 3 (Active)
Level                                        
90% Service             36.22           35.70
95% Service             46.70           46.01
99% Service             65.94           64.98
```

* **Interpretation:**  
By capturing key sources of variability, the model allows higher-volatility SKUs to be managed with similar safety stock levels as more stable ones.

---

## 4. Visual Evidence & Interpretations

### **4.1 Forecast Accuracy Plots**
![Forecast Accuracy Plots](images/Forecast_Accuracy_Plots.png)

The Full Model tracks demand spikes more closely while remaining stable when demand is smooth.

---

### **4.2 Error Distribution (Histogram)**
![Error Distribution](images/Error_Distribution.png)

Errors are more concentrated around zero, indicating more consistent predictions.

---

### **4.3 Feature Importance (Bar Chart)**
![Feature Importance](images/Feature_Importance.png)

External signals rank above lag-based features, reinforcing their importance.

---

## 5. Key Takeaways
1. External signals explain a meaningful portion of demand variability.
2. Improved forecasts reduce large errors and operational risk.
3. More accurate predictions allow for lower safety stock while maintaining service levels.

---

## 6. Tech Stack
* Python (pandas, numpy)
* scikit-learn (Linear Regression)
* matplotlib, seaborn

---

## 7. How to Run
1. Install dependencies:  
   `pip install pandas numpy scikit-learn matplotlib seaborn`
2. Run:  
   `python demand_forecasting.py`
3. Review outputs in the terminal and generated plots.

---

## 8. Conclusion
Incorporating external signals into demand forecasting improves both accuracy and stability. In this project, the model reduces variance by about 34%, leading to more predictable demand estimates and more efficient inventory decisions. These results suggest that combining historical data with external context is an effective approach for building more responsive supply chain systems.