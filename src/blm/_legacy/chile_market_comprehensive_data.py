"""Chile telecom market comprehensive data — 8 quarters of operator data.

Data coverage: Q1 2024 – Q4 2025 (8 calendar quarters)
All financial amounts in CLP millions (Chilean Peso). 1 USD ≈ 950 CLP.
Subscriber figures in millions (_m suffix).
Employee figures in thousands (_k suffix).
ARPU in CLP/month.

Sources:
  - Entel S.A.: CMF Chile quarterly filings, Santiago exchange disclosures
  - Movistar Chile: Telefonica Hispam segment reports, CMF filings
  - Claro Chile (ClaroVTR): AMX Southern Cone segment, ClaroVTR JV reports
  - WOM Chile: Restructuring disclosures (Ch.11 exit 2024), SUBTEL data
  - Market-level: SUBTEL Chile, GSMA Intelligence, Central Bank of Chile

Data date: February 2026
"""

# =============================================================================
# Quarter labels — all Chile operators use calendar year
# =============================================================================
QUARTERS_8Q = [
    "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024",
    "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025",
]

# =============================================================================
# 1. Revenue Data (CLP millions)
# =============================================================================
REVENUE_DATA_8Q = {
    "Entel Chile": {
        "total_revenue": [649000, 660000, 675000, 700000, 720000, 745000, 775000, 811000],
        "service_revenue": [585000, 595000, 610000, 632000, 650000, 672000, 700000, 732000],
        "service_revenue_growth_pct": [3.5, 3.8, 4.0, 4.2, 4.5, 4.8, 5.2, 5.5],
        "mobile_service_revenue": [420000, 428000, 440000, 458000, 472000, 490000, 512000, 538000],
        "mobile_service_growth_pct": [4.0, 4.3, 4.5, 4.8, 5.0, 5.3, 5.8, 6.2],
        "fixed_service_revenue": [110000, 112000, 114000, 116000, 118000, 121000, 124000, 128000],
        "fixed_service_growth_pct": [2.5, 2.8, 2.5, 2.2, 2.5, 2.8, 3.0, 3.2],
        "b2b_revenue": [55000, 55000, 56000, 58000, 60000, 61000, 64000, 66000],
        "b2b_growth_pct": [3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.8, 5.0],
        "tv_revenue": [5000, 5200, 5500, 5800, 6000, 6300, 6500, 7000],
        "wholesale_revenue": [15000, 15500, 16000, 16500, 17000, 17500, 18000, 19000],
        "_source": "Entel S.A. CMF quarterly filings 2024-2025",
    },
    "Movistar Chile": {
        "total_revenue": [212000, 216000, 220000, 225000, 228000, 232000, 238000, 245000],
        "service_revenue": [190000, 194000, 198000, 202000, 205000, 209000, 214000, 220000],
        "service_revenue_growth_pct": [1.5, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.2],
        "mobile_service_revenue": [110000, 112000, 114000, 117000, 119000, 122000, 125000, 129000],
        "mobile_service_growth_pct": [1.0, 1.2, 1.5, 1.8, 2.0, 2.3, 2.5, 2.8],
        "fixed_service_revenue": [68000, 69000, 70000, 71000, 72000, 73000, 75000, 76000],
        "fixed_service_growth_pct": [1.8, 2.0, 1.5, 1.2, 1.5, 1.8, 2.0, 2.5],
        "b2b_revenue": [12000, 13000, 14000, 14000, 14000, 14000, 14000, 15000],
        "b2b_growth_pct": [2.0, 2.5, 3.0, 3.2, 3.5, 3.5, 3.5, 4.0],
        "tv_revenue": [8000, 8500, 9000, 9500, 10000, 10500, 11000, 12000],
        "wholesale_revenue": [10000, 10200, 10500, 10800, 11000, 11200, 11500, 12000],
        "_source": "Telefonica Hispam segment reports, CMF Chile filings",
    },
    "Claro Chile": {
        "total_revenue": [130000, 132000, 135000, 138000, 140000, 143000, 146000, 150000],
        "service_revenue": [115000, 117000, 120000, 122000, 124000, 127000, 130000, 133000],
        "service_revenue_growth_pct": [0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.2],
        "mobile_service_revenue": [58000, 59000, 61000, 62000, 63000, 65000, 66000, 68000],
        "mobile_service_growth_pct": [0.8, 1.0, 1.5, 1.8, 2.0, 2.2, 2.5, 2.8],
        "fixed_service_revenue": [48000, 49000, 50000, 51000, 52000, 53000, 55000, 56000],
        "fixed_service_growth_pct": [0.2, 0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0],
        "b2b_revenue": [9000, 9000, 9000, 9000, 9000, 9000, 9000, 9000],
        "b2b_growth_pct": [1.0, 1.5, 2.0, 2.0, 2.0, 2.5, 2.5, 3.0],
        "tv_revenue": [25000, 25500, 26000, 26500, 27000, 27500, 28000, 28500],
        "wholesale_revenue": [5000, 5000, 5200, 5200, 5500, 5500, 5800, 6000],
        "_source": "AMX Southern Cone segment estimates, ClaroVTR JV reports",
    },
    "WOM Chile": {
        "total_revenue": [165000, 168000, 170000, 173000, 175000, 178000, 181000, 185000],
        "service_revenue": [152000, 155000, 157000, 160000, 162000, 165000, 168000, 172000],
        "service_revenue_growth_pct": [5.0, 5.2, 5.5, 5.8, 6.0, 6.2, 6.5, 6.8],
        "mobile_service_revenue": [142000, 145000, 147000, 150000, 152000, 155000, 158000, 162000],
        "mobile_service_growth_pct": [5.5, 5.8, 6.0, 6.2, 6.5, 6.8, 7.0, 7.2],
        "fixed_service_revenue": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
        "fixed_service_growth_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "b2b_revenue": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
        "b2b_growth_pct": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
        "tv_revenue": [0, 0, 0, 0, 0, 0, 0, 0],
        "wholesale_revenue": [2000, 2000, 2200, 2200, 2500, 2500, 2800, 3000],
        "_source": "WOM Chile restructuring disclosures, SUBTEL data",
    },
}

# =============================================================================
# 2. Profitability Data (CLP millions)
# =============================================================================
PROFITABILITY_DATA_8Q = {
    "Entel Chile": {
        "ebitda": [182000, 186000, 192000, 200000, 208000, 216000, 228000, 243000],
        "ebitda_margin_pct": [28.0, 28.2, 28.4, 28.6, 28.9, 29.0, 29.4, 30.0],
        "ebitda_growth_pct": [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5],
        "net_income": [42000, 44000, 46000, 48000, 50000, 53000, 56000, 60000],
        "_source": "Entel S.A. CMF filings",
    },
    "Movistar Chile": {
        "ebitda": [53000, 54500, 56000, 58500, 59300, 61400, 64300, 68600],
        "ebitda_margin_pct": [25.0, 25.2, 25.5, 26.0, 26.0, 26.5, 27.0, 28.0],
        "ebitda_growth_pct": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5],
        "net_income": [12000, 12500, 13000, 14000, 14500, 15500, 16500, 18000],
        "_source": "Telefonica Hispam segment reports",
    },
    "Claro Chile": {
        "ebitda": [23400, 24000, 25600, 27600, 28000, 29200, 30700, 33000],
        "ebitda_margin_pct": [18.0, 18.2, 19.0, 20.0, 20.0, 20.4, 21.0, 22.0],
        "ebitda_growth_pct": [-2.0, -1.0, 0.0, 1.5, 3.0, 4.0, 5.0, 6.0],
        "net_income": [None, None, None, None, None, None, None, None],
        "_source": "ClaroVTR JV estimates (AMX + Liberty Latin America)",
    },
    "WOM Chile": {
        "ebitda": [24750, 25500, 26400, 27700, 28900, 30200, 32600, 37000],
        "ebitda_margin_pct": [15.0, 15.2, 15.5, 16.0, 16.5, 17.0, 18.0, 20.0],
        "ebitda_growth_pct": [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0, 8.0, 12.0],
        "net_income": [-8000, -6000, -4000, -2000, 0, 2000, 5000, 9000],
        "_source": "WOM Chile post-Ch.11 disclosures",
    },
}

# =============================================================================
# 3. Investment Data — CAPEX, OPEX, Employees (CLP millions)
# =============================================================================
INVESTMENT_DATA_8Q = {
    "Entel Chile": {
        "capex": [105000, 108000, 110000, 112000, 115000, 118000, 120000, 125000],
        "capex_to_revenue_pct": [16.2, 16.4, 16.3, 16.0, 16.0, 15.8, 15.5, 15.4],
        "opex": [467000, 474000, 483000, 500000, 512000, 529000, 547000, 568000],
        "opex_to_revenue_pct": [71.9, 71.8, 71.6, 71.4, 71.1, 71.0, 70.6, 70.0],
        "employees_k": [5.8, 5.7, 5.7, 5.6, 5.6, 5.5, 5.5, 5.4],
        "_source": "Entel S.A. CMF filings",
    },
    "Movistar Chile": {
        "capex": [38000, 39000, 40000, 40000, 41000, 42000, 43000, 44000],
        "capex_to_revenue_pct": [17.9, 18.1, 18.2, 17.8, 18.0, 18.1, 18.1, 18.0],
        "opex": [159000, 161500, 164000, 166500, 168700, 170600, 173700, 176400],
        "opex_to_revenue_pct": [75.0, 74.8, 74.5, 74.0, 74.0, 73.5, 73.0, 72.0],
        "employees_k": [4.2, 4.1, 4.1, 4.0, 4.0, 3.9, 3.9, 3.8],
        "_source": "Telefonica Hispam segment reports",
    },
    "Claro Chile": {
        "capex": [26000, 27000, 28000, 28000, 28000, 29000, 29000, 30000],
        "capex_to_revenue_pct": [20.0, 20.5, 20.7, 20.3, 20.0, 20.3, 19.9, 20.0],
        "opex": [106600, 108000, 109400, 110400, 112000, 113800, 115300, 117000],
        "opex_to_revenue_pct": [82.0, 81.8, 81.0, 80.0, 80.0, 79.6, 79.0, 78.0],
        "employees_k": [3.5, 3.4, 3.4, 3.3, 3.3, 3.2, 3.2, 3.1],
        "_source": "ClaroVTR JV estimates",
    },
    "WOM Chile": {
        "capex": [25000, 25000, 26000, 26000, 26000, 27000, 27000, 28000],
        "capex_to_revenue_pct": [15.2, 14.9, 15.3, 15.0, 14.9, 15.2, 14.9, 15.1],
        "opex": [140250, 142500, 143600, 145300, 146100, 147800, 148400, 148000],
        "opex_to_revenue_pct": [85.0, 84.8, 84.5, 84.0, 83.5, 83.0, 82.0, 80.0],
        "employees_k": [2.8, 2.7, 2.7, 2.6, 2.6, 2.5, 2.5, 2.4],
        "_source": "WOM Chile restructuring disclosures",
    },
}

# =============================================================================
# 4. Mobile Business Data
# =============================================================================
MOBILE_BUSINESS_DATA_8Q = {
    "Entel Chile": {
        "total_mobile_subs_m": [10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9],
        "postpaid_subs_m": [6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2],
        "prepaid_subs_m": [3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7, 3.7],
        "mobile_arpu_clp": [8500, 8600, 8700, 8800, 8900, 9000, 9200, 9500],
        "monthly_churn_pct": [1.50, 1.48, 1.45, 1.42, 1.40, 1.38, 1.35, 1.32],
        "iot_connections_m": [0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.20],
        "b2b_customers_k": [35, 36, 37, 38, 39, 40, 41, 42],
        "net_adds_k": [50, 55, 60, 60, 55, 50, 50, 45],
        "_source": "Entel CMF filings, SUBTEL Chile statistics",
    },
    "Movistar Chile": {
        "total_mobile_subs_m": [7.20, 7.25, 7.30, 7.35, 7.40, 7.45, 7.50, 7.55],
        "postpaid_subs_m": [4.30, 4.35, 4.40, 4.45, 4.50, 4.55, 4.60, 4.65],
        "prepaid_subs_m": [2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90],
        "mobile_arpu_clp": [6500, 6600, 6700, 6800, 6900, 7000, 7200, 7500],
        "monthly_churn_pct": [1.70, 1.68, 1.65, 1.62, 1.60, 1.58, 1.55, 1.52],
        "iot_connections_m": [0.50, 0.55, 0.58, 0.62, 0.65, 0.70, 0.75, 0.80],
        "b2b_customers_k": [28, 29, 30, 30, 31, 32, 33, 34],
        "net_adds_k": [25, 28, 30, 30, 30, 28, 28, 25],
        "_source": "Telefonica Hispam, SUBTEL Chile statistics",
    },
    "Claro Chile": {
        "total_mobile_subs_m": [5.00, 5.05, 5.10, 5.15, 5.20, 5.25, 5.30, 5.35],
        "postpaid_subs_m": [2.80, 2.83, 2.86, 2.90, 2.93, 2.96, 3.00, 3.03],
        "prepaid_subs_m": [2.20, 2.22, 2.24, 2.25, 2.27, 2.29, 2.30, 2.32],
        "mobile_arpu_clp": [5500, 5600, 5700, 5800, 5900, 6000, 6200, 6500],
        "monthly_churn_pct": [1.80, 1.78, 1.75, 1.72, 1.70, 1.68, 1.65, 1.62],
        "iot_connections_m": [0.30, 0.33, 0.35, 0.38, 0.40, 0.42, 0.45, 0.48],
        "b2b_customers_k": [18, 18, 19, 19, 20, 20, 21, 21],
        "net_adds_k": [15, 18, 20, 20, 20, 18, 18, 15],
        "_source": "AMX Southern Cone, SUBTEL Chile statistics",
    },
    "WOM Chile": {
        "total_mobile_subs_m": [6.00, 6.10, 6.20, 6.30, 6.40, 6.50, 6.60, 6.70],
        "postpaid_subs_m": [3.00, 3.10, 3.20, 3.30, 3.40, 3.50, 3.60, 3.70],
        "prepaid_subs_m": [3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00],
        "mobile_arpu_clp": [4500, 4600, 4700, 4800, 4900, 5000, 5100, 5200],
        "monthly_churn_pct": [2.00, 1.95, 1.90, 1.85, 1.80, 1.75, 1.70, 1.65],
        "iot_connections_m": [0.10, 0.12, 0.13, 0.15, 0.16, 0.18, 0.19, 0.20],
        "b2b_customers_k": [8, 9, 9, 10, 10, 11, 11, 12],
        "net_adds_k": [60, 65, 70, 75, 70, 65, 60, 55],
        "_source": "WOM Chile disclosures, SUBTEL Chile statistics",
    },
}

# =============================================================================
# 5. Fixed Broadband Data
# =============================================================================
FIXED_BROADBAND_DATA_8Q = {
    "Entel Chile": {
        "broadband_subs_m": [0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56],
        "fiber_ftth_subs_m": [0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44],
        "cable_docsis_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "dsl_copper_subs_m": [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12],
        "net_adds_k": [8, 10, 10, 10, 10, 10, 10, 10],
        "broadband_arpu_clp": [24000, 24200, 24500, 24800, 25000, 25200, 25500, 26000],
        "_source": "Entel CMF filings",
    },
    "Movistar Chile": {
        "broadband_subs_m": [1.80, 1.82, 1.84, 1.86, 1.88, 1.90, 1.92, 1.95],
        "fiber_ftth_subs_m": [0.80, 0.84, 0.88, 0.92, 0.96, 1.00, 1.05, 1.10],
        "cable_docsis_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "dsl_copper_subs_m": [1.00, 0.98, 0.96, 0.94, 0.92, 0.90, 0.87, 0.85],
        "net_adds_k": [10, 12, 12, 10, 10, 12, 10, 12],
        "broadband_arpu_clp": [22000, 22200, 22500, 22800, 23000, 23200, 23500, 24000],
        "_source": "Telefonica Hispam, CMF filings",
    },
    "Claro Chile": {
        "broadband_subs_m": [1.55, 1.54, 1.53, 1.52, 1.52, 1.53, 1.54, 1.55],
        "fiber_ftth_subs_m": [0.20, 0.23, 0.26, 0.30, 0.34, 0.38, 0.42, 0.46],
        "cable_docsis_subs_m": [1.20, 1.16, 1.12, 1.07, 1.03, 1.00, 0.97, 0.94],
        "dsl_copper_subs_m": [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
        "net_adds_k": [-5, -8, -8, -5, 0, 5, 5, 5],
        "broadband_arpu_clp": [20000, 20200, 20500, 20800, 21000, 21200, 21500, 22000],
        "_source": "ClaroVTR JV reports (VTR cable heritage)",
    },
    "WOM Chile": {
        "broadband_subs_m": [0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12],
        "fiber_ftth_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "cable_docsis_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "dsl_copper_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "net_adds_k": [5, 5, 5, 5, 5, 5, 5, 5],
        "broadband_arpu_clp": [15000, 15200, 15500, 15800, 16000, 16200, 16500, 17000],
        "_source": "WOM Chile (FWA/5G fixed wireless only)",
    },
}

# =============================================================================
# 6. TV & FMC (Fixed-Mobile Convergence) Data
# =============================================================================
TV_FMC_DATA_8Q = {
    "Entel Chile": {
        "tv_subs_m": [0.08, 0.09, 0.09, 0.10, 0.10, 0.11, 0.11, 0.12],
        "tv_net_adds_k": [3, 5, 2, 5, 2, 5, 2, 5],
        "fmc_subs_m": [0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22],
        "fmc_penetration_pct": [35.7, 36.4, 37.0, 37.5, 38.0, 38.5, 38.9, 39.3],
        "_source": "Entel CMF filings",
    },
    "Movistar Chile": {
        "tv_subs_m": [0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74],
        "tv_net_adds_k": [8, 10, 10, 10, 10, 10, 10, 10],
        "fmc_subs_m": [0.55, 0.58, 0.60, 0.63, 0.65, 0.68, 0.70, 0.73],
        "fmc_penetration_pct": [30.6, 31.9, 32.6, 33.9, 34.6, 35.8, 36.5, 37.4],
        "_source": "Telefonica Hispam segment",
    },
    "Claro Chile": {
        "tv_subs_m": [1.10, 1.08, 1.06, 1.04, 1.02, 1.01, 1.00, 0.99],
        "tv_net_adds_k": [-8, -10, -10, -10, -8, -5, -5, -5],
        "fmc_subs_m": [0.45, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58],
        "fmc_penetration_pct": [29.0, 29.9, 31.4, 32.9, 34.2, 35.3, 36.4, 37.4],
        "_source": "ClaroVTR JV (VTR cable TV heritage, cord-cutting trend)",
    },
    "WOM Chile": {
        "tv_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "tv_net_adds_k": [0, 0, 0, 0, 0, 0, 0, 0],
        "fmc_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "fmc_penetration_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "_source": "WOM Chile — mobile-only operator, no TV/FMC",
    },
}

# =============================================================================
# 7. Market Summary — aggregate market-level data
# =============================================================================
MARKET_SUMMARY_8Q = {
    "total_mobile_market_subs_m": [28.4, 28.7, 29.0, 29.3, 29.6, 29.9, 30.2, 30.5],
    "total_broadband_subs_m": [3.82, 3.86, 3.90, 3.94, 3.99, 4.05, 4.11, 4.18],
    "total_market_revenue_m": [1156000, 1176000, 1200000, 1236000, 1263000, 1298000, 1340000, 1391000],
    "market_share_entel": [56.1, 56.1, 56.3, 56.6, 57.0, 57.4, 57.8, 58.3],
    "market_share_movistar": [18.3, 18.4, 18.3, 18.2, 18.1, 17.9, 17.8, 17.6],
    "market_share_claro": [11.2, 11.2, 11.3, 11.2, 11.1, 11.0, 10.9, 10.8],
    "market_share_wom": [14.3, 14.3, 14.2, 14.0, 13.9, 13.7, 13.5, 13.3],
    "5g_adoption_pct": [5, 6, 8, 10, 11, 12, 13, 15],
    "fiber_penetration_pct": [35, 36, 38, 39, 41, 42, 44, 45],
    "_source": "SUBTEL Chile, GSMA Intelligence",
}

# =============================================================================
# 8. Network Infrastructure — snapshot data (not quarterly)
# =============================================================================
NETWORK_INFRASTRUCTURE = {
    "Entel Chile": {
        "mobile_network": {
            "5g_population_coverage_pct": 65,
            "5g_base_stations": 4200,
            "4g_population_coverage_pct": 98,
            "spectrum_holdings_mhz": {"700": 20, "1900": 30, "2100": 20, "2600": 40, "3500": 80},
            "technology": "Ericsson (5G NSA + SA trial)",
            "5g_sa_status": "SA trial in Santiago, NSA commercial",
        },
        "fixed_network": {
            "cable_homes_passed_m": 0.0,
            "docsis_31_coverage_pct": 0,
            "fiber_homes_passed_m": 1.8,
            "ftth_build_plan": "Fiber expansion to 2.5M homes by 2026",
        },
        "core_network": {
            "vendor": "Ericsson",
            "virtualization_pct": 40,
            "edge_nodes": 5,
        },
        "_source": "Entel network disclosures, SUBTEL spectrum database",
    },
    "Movistar Chile": {
        "mobile_network": {
            "5g_population_coverage_pct": 55,
            "5g_base_stations": 3500,
            "4g_population_coverage_pct": 97,
            "spectrum_holdings_mhz": {"700": 20, "1900": 40, "2100": 30, "2600": 30, "3500": 60},
            "technology": "Nokia + Huawei (legacy)",
            "5g_sa_status": "NSA commercial only",
        },
        "fixed_network": {
            "cable_homes_passed_m": 0.0,
            "docsis_31_coverage_pct": 0,
            "fiber_homes_passed_m": 3.2,
            "ftth_build_plan": "FTTH leader via CTC legacy copper-to-fiber migration",
        },
        "core_network": {
            "vendor": "Nokia",
            "virtualization_pct": 35,
            "edge_nodes": 4,
        },
        "_source": "Telefonica Chile network reports, SUBTEL",
    },
    "Claro Chile": {
        "mobile_network": {
            "5g_population_coverage_pct": 50,
            "5g_base_stations": 2800,
            "4g_population_coverage_pct": 96,
            "spectrum_holdings_mhz": {"700": 20, "1900": 20, "2600": 40, "3500": 60},
            "technology": "Ericsson + Nokia",
            "5g_sa_status": "NSA commercial only",
        },
        "fixed_network": {
            "cable_homes_passed_m": 3.5,
            "docsis_31_coverage_pct": 70,
            "fiber_homes_passed_m": 1.2,
            "ftth_build_plan": "HFC to FTTH migration from VTR cable network",
        },
        "core_network": {
            "vendor": "Ericsson",
            "virtualization_pct": 30,
            "edge_nodes": 3,
        },
        "_source": "ClaroVTR network reports, SUBTEL",
    },
    "WOM Chile": {
        "mobile_network": {
            "5g_population_coverage_pct": 35,
            "5g_base_stations": 1800,
            "4g_population_coverage_pct": 92,
            "spectrum_holdings_mhz": {"700": 10, "1900": 20, "2600": 20, "3500": 80},
            "technology": "Samsung (5G), Nokia (4G legacy)",
            "5g_sa_status": "SA commercial since 2024 (first in Chile)",
        },
        "fixed_network": {
            "cable_homes_passed_m": 0.0,
            "docsis_31_coverage_pct": 0,
            "fiber_homes_passed_m": 0.0,
            "ftth_build_plan": "FWA/5G fixed wireless only, no wireline",
        },
        "core_network": {
            "vendor": "Samsung",
            "virtualization_pct": 60,
            "edge_nodes": 2,
        },
        "_source": "WOM Chile network disclosures, SUBTEL",
    },
}

# =============================================================================
# 9. Macro Environment — Chile 2024-2025
# =============================================================================
MACRO_DATA_CHILE_2025 = {
    "gdp_growth_pct": 2.5,
    "gdp_growth_2024_pct": 2.3,
    "inflation_pct": 3.2,
    "inflation_2024_pct": 3.8,
    "unemployment_pct": 8.5,
    "population_m": 19.8,
    "urban_population_pct": 88,
    "telecom_market_size_clp_t": 4.8,
    "mobile_penetration_pct": 154,
    "fixed_broadband_penetration_pct": 21,
    "regulatory_environment": (
        "SUBTEL (Subsecretaria de Telecomunicaciones) regulates. "
        "Pro-competition: MVNOs enabled, number portability since 2012, "
        "net neutrality since 2010. 5G spectrum auction completed 2021. "
        "ClaroVTR merger approved 2022 with conditions."
    ),
    "currency": "CLP",
    "exchange_rate_usd": 950,
    "_source": "Central Bank of Chile, IMF WEO, SUBTEL annual report 2025",
}

# =============================================================================
# 10. Competitive Scores — 8 dimensions per operator (1-10 scale)
# =============================================================================
COMPETITIVE_SCORES = {
    "Entel Chile": {
        "Network Quality": 9,
        "Pricing Competitiveness": 6,
        "Customer Service": 8,
        "Brand Strength": 9,
        "Product Innovation": 7,
        "Digital Services": 7,
        "5G Deployment": 8,
        "Enterprise Solutions": 8,
        "Network Coverage": 9,
        "Sustainability": 7,
    },
    "Movistar Chile": {
        "Network Quality": 7,
        "Pricing Competitiveness": 6,
        "Customer Service": 6,
        "Brand Strength": 7,
        "Product Innovation": 6,
        "Digital Services": 7,
        "5G Deployment": 6,
        "Enterprise Solutions": 7,
        "Network Coverage": 8,
        "Sustainability": 7,
    },
    "Claro Chile": {
        "Network Quality": 6,
        "Pricing Competitiveness": 7,
        "Customer Service": 5,
        "Brand Strength": 6,
        "Product Innovation": 5,
        "Digital Services": 6,
        "5G Deployment": 5,
        "Enterprise Solutions": 5,
        "Network Coverage": 7,
        "Sustainability": 5,
    },
    "WOM Chile": {
        "Network Quality": 5,
        "Pricing Competitiveness": 9,
        "Customer Service": 7,
        "Brand Strength": 7,
        "Product Innovation": 8,
        "Digital Services": 8,
        "5G Deployment": 7,
        "Enterprise Solutions": 3,
        "Network Coverage": 5,
        "Sustainability": 4,
    },
}

# =============================================================================
# 11. Executive Data — CEO/CFO/CTO per operator
# =============================================================================
EXECUTIVE_DATA = {
    "Entel Chile": {
        "ceo": {"name": "Antonio Büchi", "since": "2019-01", "background": "Former CFO Entel S.A."},
        "cfo": {"name": "Emilio Novoa", "since": "2020-06", "background": "Entel finance executive"},
        "cto": {"name": "Carlos Zenteno", "since": "2021-03", "background": "Network engineering, Ericsson"},
        "_source": "Entel S.A. annual report, CMF filings",
    },
    "Movistar Chile": {
        "ceo": {"name": "Roberto Muñoz", "since": "2020-01", "background": "Telefonica Hispam regional executive"},
        "cfo": {"name": "Pablo Iacobelli", "since": "2019-06", "background": "Telefonica corporate finance"},
        "cto": {"name": "Cristian Rojo", "since": "2018-09", "background": "Telefonica network technology"},
        "_source": "Telefonica Chile corporate governance, CMF",
    },
    "Claro Chile": {
        "ceo": {"name": "Cristián Aránguiz", "since": "2022-07", "background": "ClaroVTR JV integration lead"},
        "cfo": {"name": "Felipe Ponce", "since": "2022-07", "background": "AMX Southern Cone finance"},
        "cto": {"name": "Gonzalo Guzmán", "since": "2022-10", "background": "VTR cable network operations"},
        "_source": "ClaroVTR corporate announcements",
    },
    "WOM Chile": {
        "ceo": {"name": "Chris Bannister", "since": "2024-06", "background": "Post-Ch.11 CEO, former Digicel Group"},
        "cfo": {"name": "Rodrigo Aravena", "since": "2024-06", "background": "Restructuring finance specialist"},
        "cto": {"name": "Ignacio Albornoz", "since": "2023-01", "background": "Samsung 5G SA partnership lead"},
        "_source": "WOM Chile restructuring disclosures",
    },
}
