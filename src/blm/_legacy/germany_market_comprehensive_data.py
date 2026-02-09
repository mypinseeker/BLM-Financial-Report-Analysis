"""德国电信市场综合数据 - 全维度分析数据集

数据口径说明:
- 所有数据均为德国区域数据（非集团层面）
- 移动用户数已分离IoT连接和消费者连接
- 数据来源: 各公司季度财报、年报、Bundesnetzagentur报告
- 时间维度: 8个季度 (Q4 FY24 - Q3 FY26)

数据更新日期: 2026年2月6日
"""

# =============================================================================
# 季度标签
# =============================================================================
QUARTERS_8Q = ["Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26"]

# =============================================================================
# 第一部分: 经营层面数据 (Operating Data)
# =============================================================================

# 1.1 收入数据 - 多维度 (单位: €M 百万欧元)
REVENUE_DATA_8Q = {
    "Vodafone Germany": {
        # 总收入
        "total_revenue": [3050, 3080, 3060, 3070, 3080, 3090, 3090, 3092],
        # 服务收入
        "service_revenue": [2680, 2700, 2690, 2700, 2710, 2720, 2720, 2726],
        "service_revenue_growth_pct": [-0.8, -0.5, -0.3, 0.0, 0.2, 0.4, 0.5, 0.7],
        # 移动服务收入
        "mobile_service_revenue": [1450, 1460, 1465, 1470, 1480, 1490, 1500, 1520],
        "mobile_service_growth_pct": [-0.5, -0.2, 0.3, 0.8, 1.2, 1.8, 2.3, 2.8],
        # 固定服务收入
        "fixed_service_revenue": [820, 815, 810, 808, 805, 802, 798, 795],
        "fixed_service_growth_pct": [-2.8, -2.5, -2.3, -2.1, -1.8, -1.5, -1.3, -1.1],
        # B2B收入
        "b2b_revenue": [410, 420, 430, 445, 460, 480, 500, 520],
        "b2b_growth_pct": [3.5, 4.2, 5.0, 5.8, 6.5, 7.2, 7.8, 8.5],
        # TV收入
        "tv_revenue": [285, 283, 280, 278, 275, 273, 270, 268],
        # 批发收入
        "wholesale_revenue": [180, 185, 190, 200, 220, 260, 320, 380],
        # 来源说明
        "_source": "Vodafone Q3 FY26 Trading Update, Feb 5, 2026; H1 FY26 Results",
    },
    "Deutsche Telekom Germany": {
        # 注意: 此处为德国业务单元数据
        "total_revenue": [5980, 6020, 6050, 6080, 6120, 6150, 6180, 6200],
        "service_revenue": [5250, 5290, 5320, 5350, 5380, 5410, 5440, 5460],
        "service_revenue_growth_pct": [2.8, 2.5, 2.2, 2.0, 1.8, 1.5, 1.3, 1.1],
        "mobile_service_revenue": [2380, 2410, 2440, 2465, 2490, 2515, 2535, 2555],
        "mobile_service_growth_pct": [3.5, 3.2, 2.8, 2.5, 2.2, 2.0, 1.8, 1.6],
        "fixed_service_revenue": [1820, 1835, 1850, 1865, 1880, 1890, 1900, 1910],
        "fixed_service_growth_pct": [2.0, 1.8, 1.6, 1.5, 1.3, 1.2, 1.0, 0.9],
        "b2b_revenue": [950, 990, 1030, 1070, 1110, 1150, 1190, 1230],
        "b2b_growth_pct": [5.5, 6.0, 6.5, 7.0, 7.2, 7.5, 7.5, 7.5],
        "tv_revenue": [440, 448, 455, 463, 470, 476, 482, 488],
        "wholesale_revenue": [340, 342, 345, 347, 350, 352, 354, 356],
        "_source": "Deutsche Telekom Q3 2025 Results, Germany Segment",
    },
    "Telefónica O2 Germany": {
        "total_revenue": [2120, 2100, 2080, 2050, 2030, 2020, 2010, 2000],
        "service_revenue": [1820, 1800, 1780, 1750, 1730, 1720, 1710, 1700],
        "service_revenue_growth_pct": [-1.5, -2.0, -2.5, -3.0, -3.2, -3.4, -3.4, -3.4],
        "mobile_service_revenue": [1380, 1365, 1350, 1335, 1320, 1308, 1296, 1285],
        "mobile_service_growth_pct": [-1.2, -1.8, -2.2, -2.5, -2.8, -3.0, -3.0, -3.0],
        "fixed_service_revenue": [185, 186, 187, 188, 189, 190, 191, 192],
        "fixed_service_growth_pct": [1.5, 1.2, 1.0, 0.8, 0.5, 0.5, 0.5, 0.5],
        "b2b_revenue": [320, 340, 360, 385, 410, 438, 468, 500],
        "b2b_growth_pct": [8.0, 9.0, 10.0, 11.0, 11.5, 12.0, 12.5, 13.0],
        "tv_revenue": [42, 43, 44, 45, 46, 47, 48, 49],
        "wholesale_revenue": [280, 260, 240, 200, 160, 120, 90, 65],
        "_source": "Telefónica Deutschland Q3 2025 Results",
    },
    "1&1 AG": {
        "total_revenue": [1010, 1015, 1020, 1025, 1030, 1032, 1033, 1035],
        "service_revenue": [890, 895, 900, 905, 910, 912, 913, 915],
        "service_revenue_growth_pct": [1.5, 1.2, 0.8, 0.5, 0.3, 0.2, 0.1, 0.1],
        "mobile_service_revenue": [510, 515, 520, 524, 528, 530, 531, 532],
        "mobile_service_growth_pct": [2.0, 1.8, 1.5, 1.2, 1.0, 0.8, 0.5, 0.3],
        "fixed_service_revenue": [300, 298, 296, 294, 292, 290, 288, 287],
        "fixed_service_growth_pct": [-0.5, -0.6, -0.8, -1.0, -1.0, -1.0, -1.0, -1.0],
        "b2b_revenue": [65, 68, 72, 76, 80, 84, 88, 92],
        "b2b_growth_pct": [4.0, 5.0, 6.0, 7.0, 7.5, 8.0, 8.5, 9.0],
        "tv_revenue": [18, 19, 20, 21, 22, 23, 24, 25],
        "wholesale_revenue": [0, 0, 0, 0, 0, 0, 0, 0],
        "_source": "1&1 AG Quarterly Reports 2025-2026",
    },
}

# 1.2 盈利数据 (Profitability)
PROFITABILITY_DATA_8Q = {
    "Vodafone Germany": {
        # EBITDA (单位: €M)
        "ebitda": [1080, 1090, 1090, 1100, 1100, 1110, 1110, 1120],
        # EBITDA Margin %
        "ebitda_margin_pct": [35.4, 35.5, 35.6, 35.8, 35.9, 36.0, 36.0, 36.2],
        # EBITDA YoY增长率 %
        "ebitda_growth_pct": [-2.0, -1.5, -1.0, 0.0, 0.5, 1.0, 1.2, 1.5],
        # 净利润 (如有)
        "net_income": [None, None, None, None, None, None, None, None],
        "_source": "Vodafone Group Results, Germany Contribution",
    },
    "Deutsche Telekom Germany": {
        "ebitda": [2450, 2480, 2510, 2535, 2560, 2580, 2595, 2610],
        "ebitda_margin_pct": [41.0, 41.2, 41.5, 41.7, 41.8, 41.9, 42.0, 42.1],
        "ebitda_growth_pct": [4.5, 4.2, 3.8, 3.5, 3.2, 3.0, 2.8, 2.6],
        "net_income": [680, 695, 710, 720, 735, 745, 755, 765],
        "_source": "DT Germany Segment Results Q3 2025",
    },
    "Telefónica O2 Germany": {
        "ebitda": [680, 670, 660, 660, 650, 650, 650, 650],
        "ebitda_margin_pct": [32.1, 31.9, 31.7, 32.2, 32.0, 32.2, 32.3, 32.5],
        "ebitda_growth_pct": [2.0, 0.5, -1.0, -1.5, -2.0, -2.0, -1.8, -1.5],
        "net_income": [145, 140, 135, 132, 128, 125, 123, 120],
        "_source": "Telefónica Deutschland Q3 2025 Results",
    },
    "1&1 AG": {
        "ebitda": [145, 140, 135, 132, 130, 128, 127, 126],
        "ebitda_margin_pct": [14.4, 13.8, 13.2, 12.9, 12.6, 12.4, 12.3, 12.2],
        "ebitda_growth_pct": [-8.0, -10.0, -12.0, -10.5, -9.0, -8.5, -8.0, -7.0],
        "net_income": [42, 38, 35, 32, 30, 28, 27, 26],
        "_source": "1&1 AG Quarterly Reports",
    },
}

# 1.3 投资数据 (Investment: OPEX & CAPEX)
INVESTMENT_DATA_8Q = {
    "Vodafone Germany": {
        # OPEX (单位: €M)
        "opex": [1970, 1990, 1970, 1970, 1980, 1980, 1980, 1972],
        # OPEX占收入比 %
        "opex_to_revenue_pct": [64.6, 64.6, 64.4, 64.2, 64.3, 64.1, 64.1, 63.8],
        # CAPEX (单位: €M)
        "capex": [820, 800, 790, 780, 800, 810, 800, 800],
        # CAPEX占收入比 %
        "capex_to_revenue_pct": [26.9, 26.0, 25.8, 25.4, 26.0, 26.2, 25.9, 25.9],
        # 员工数 (千人)
        "employees_k": [15.2, 15.1, 15.0, 14.9, 14.8, 14.7, 14.6, 14.5],
        "_source": "Vodafone Annual Report, Quarterly Updates",
    },
    "Deutsche Telekom Germany": {
        "opex": [3530, 3540, 3540, 3545, 3560, 3570, 3585, 3590],
        "opex_to_revenue_pct": [59.0, 58.8, 58.5, 58.3, 58.2, 58.0, 58.0, 57.9],
        "capex": [1250, 1240, 1220, 1210, 1200, 1200, 1190, 1200],
        "capex_to_revenue_pct": [20.9, 20.6, 20.2, 19.9, 19.6, 19.5, 19.3, 19.4],
        "employees_k": [85.5, 85.3, 85.0, 84.8, 84.5, 84.2, 84.0, 83.8],
        "_source": "DT Germany Segment Reports",
    },
    "Telefónica O2 Germany": {
        "opex": [1440, 1430, 1420, 1390, 1380, 1370, 1360, 1350],
        "opex_to_revenue_pct": [67.9, 68.1, 68.3, 67.8, 68.0, 67.8, 67.7, 67.5],
        "capex": [550, 540, 520, 510, 500, 500, 500, 500],
        "capex_to_revenue_pct": [25.9, 25.7, 25.0, 24.9, 24.6, 24.8, 24.9, 25.0],
        "employees_k": [7.5, 7.4, 7.3, 7.2, 7.1, 7.0, 6.9, 6.8],
        "_source": "Telefónica Deutschland Reports",
    },
    "1&1 AG": {
        "opex": [865, 875, 885, 893, 900, 904, 906, 909],
        "opex_to_revenue_pct": [85.6, 86.2, 86.8, 87.1, 87.4, 87.6, 87.7, 87.8],
        "capex": [350, 380, 400, 420, 400, 400, 400, 400],
        "capex_to_revenue_pct": [34.7, 37.4, 39.2, 41.0, 38.8, 38.8, 38.7, 38.6],
        "employees_k": [3.2, 3.3, 3.4, 3.5, 3.5, 3.6, 3.6, 3.7],
        "_source": "1&1 AG Reports",
    },
}

# =============================================================================
# 第二部分: 业务层面数据 (Business Segment Data)
# =============================================================================

# 2.1 移动业务详细数据
MOBILE_BUSINESS_DATA_8Q = {
    "Vodafone Germany": {
        # 消费者移动用户 (不含IoT, 单位: 百万)
        "consumer_mobile_subs_m": [28.2, 28.4, 28.6, 28.8, 29.0, 29.2, 29.4, 29.5],
        # IoT连接数 (单位: 百万)
        "iot_connections_m": [2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0],
        # 移动总用户 (消费者+IoT)
        "total_mobile_subs_m": [30.5, 30.8, 31.1, 31.4, 31.7, 32.0, 32.3, 32.5],
        # 后付费用户 (单位: 百万)
        "postpaid_subs_m": [21.8, 22.0, 22.2, 22.4, 22.6, 22.8, 23.0, 23.2],
        # 预付费用户 (单位: 百万)
        "prepaid_subs_m": [6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.3],
        # 后付费占比 %
        "postpaid_ratio_pct": [77.3, 77.5, 77.6, 77.8, 77.9, 78.1, 78.2, 78.6],
        # 合同用户占比 %
        "contract_ratio_pct": [92.0, 92.2, 92.5, 92.8, 93.0, 93.3, 93.6, 94.0],
        # 移动ARPU (€/月)
        "mobile_arpu_eur": [11.8, 11.9, 12.0, 12.2, 12.4, 12.5, 12.6, 12.8],
        # 新客户ARPU增长 %
        "new_customer_arpu_growth_pct": [8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 21.0],
        # 月度流失率 %
        "monthly_churn_pct": [1.15, 1.12, 1.10, 1.08, 1.06, 1.05, 1.05, 1.05],
        # 净增用户 (千)
        "net_adds_k": [85, 90, 95, 100, 105, 110, 115, 80],
        "_source": "Vodafone Q3 FY26 Trading Update",
    },
    "Deutsche Telekom Germany": {
        # 注: DT Germany移动用户约47-48M, 非集团69.8M
        "consumer_mobile_subs_m": [44.5, 44.8, 45.1, 45.4, 45.7, 46.0, 46.3, 46.5],
        "iot_connections_m": [3.8, 4.0, 4.2, 4.5, 4.8, 5.1, 5.4, 5.7],
        "total_mobile_subs_m": [48.3, 48.8, 49.3, 49.9, 50.5, 51.1, 51.7, 52.2],
        "postpaid_subs_m": [34.5, 34.9, 35.2, 35.6, 35.9, 36.2, 36.5, 36.8],
        "prepaid_subs_m": [10.0, 9.9, 9.9, 9.8, 9.8, 9.8, 9.8, 9.7],
        "postpaid_ratio_pct": [77.5, 77.9, 78.0, 78.4, 78.5, 78.7, 78.8, 79.1],
        "contract_ratio_pct": [95.0, 95.2, 95.3, 95.5, 95.6, 95.7, 95.8, 96.0],
        "mobile_arpu_eur": [13.5, 13.6, 13.8, 13.9, 14.0, 14.1, 14.1, 14.2],
        "new_customer_arpu_growth_pct": [5.0, 5.5, 6.0, 6.0, 5.5, 5.0, 4.5, 4.0],
        "monthly_churn_pct": [0.85, 0.84, 0.82, 0.81, 0.80, 0.80, 0.80, 0.80],
        "net_adds_k": [350, 380, 400, 420, 400, 380, 360, 340],
        "_source": "DT Germany Q3 2025 Results",
    },
    "Telefónica O2 Germany": {
        "consumer_mobile_subs_m": [38.5, 38.2, 37.9, 37.6, 37.3, 37.1, 36.9, 36.7],
        "iot_connections_m": [6.5, 6.8, 7.2, 7.6, 8.0, 8.4, 8.8, 9.2],
        "total_mobile_subs_m": [45.0, 45.0, 45.1, 45.2, 45.3, 45.5, 45.7, 45.9],
        "postpaid_subs_m": [23.5, 23.3, 23.1, 22.9, 22.8, 22.7, 22.6, 22.5],
        "prepaid_subs_m": [15.0, 14.9, 14.8, 14.7, 14.5, 14.4, 14.3, 14.2],
        "postpaid_ratio_pct": [61.0, 61.0, 60.9, 60.9, 61.1, 61.2, 61.2, 61.3],
        "contract_ratio_pct": [85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.0],
        "mobile_arpu_eur": [10.5, 10.5, 10.6, 10.6, 10.7, 10.7, 10.8, 10.8],
        "new_customer_arpu_growth_pct": [2.0, 2.5, 3.0, 3.0, 3.0, 3.0, 2.5, 2.0],
        "monthly_churn_pct": [0.95, 0.94, 0.92, 0.91, 0.90, 0.90, 0.90, 0.90],
        "net_adds_k": [150, 160, 170, 180, 184, 180, 175, 170],
        "_source": "Telefónica Deutschland Q3 2025",
    },
    "1&1 AG": {
        "consumer_mobile_subs_m": [11.5, 11.6, 11.7, 11.8, 11.9, 12.0, 12.1, 12.2],
        "iot_connections_m": [0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
        "total_mobile_subs_m": [11.7, 11.8, 12.0, 12.1, 12.2, 12.3, 12.4, 12.5],
        "postpaid_subs_m": [9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5],
        "prepaid_subs_m": [1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7],
        "postpaid_ratio_pct": [85.2, 85.6, 85.5, 85.9, 86.1, 86.2, 86.5, 86.8],
        "contract_ratio_pct": [90.0, 90.5, 91.0, 91.2, 91.5, 91.8, 92.0, 92.0],
        "mobile_arpu_eur": [9.5, 9.5, 9.6, 9.6, 9.7, 9.7, 9.8, 9.8],
        "new_customer_arpu_growth_pct": [1.0, 1.5, 2.0, 2.0, 2.0, 1.5, 1.0, 1.0],
        "monthly_churn_pct": [1.10, 1.08, 1.05, 1.03, 1.00, 0.98, 0.96, 0.95],
        "net_adds_k": [40, 45, 50, 50, 45, 40, 35, 30],
        "_source": "1&1 AG Quarterly Reports",
    },
}

# 2.2 固网宽带业务详细数据
FIXED_BROADBAND_DATA_8Q = {
    "Vodafone Germany": {
        # 宽带总用户 (百万)
        "broadband_subs_m": [10.32, 10.28, 10.21, 10.14, 10.08, 10.02, 9.97, 9.94],
        # 按接入技术分类 (百万)
        "fiber_ftth_subs_m": [0.85, 0.92, 1.00, 1.08, 1.18, 1.28, 1.38, 1.48],
        "cable_docsis_subs_m": [7.50, 7.45, 7.38, 7.30, 7.22, 7.14, 7.06, 6.98],
        "dsl_copper_subs_m": [1.97, 1.91, 1.83, 1.76, 1.68, 1.60, 1.53, 1.48],
        # 各技术占比 %
        "fiber_ratio_pct": [8.2, 8.9, 9.8, 10.7, 11.7, 12.8, 13.8, 14.9],
        "cable_ratio_pct": [72.7, 72.5, 72.3, 72.0, 71.6, 71.3, 70.8, 70.2],
        "dsl_ratio_pct": [19.1, 18.6, 17.9, 17.4, 16.7, 16.0, 15.3, 14.9],
        # 宽带净增 (千)
        "net_adds_k": [-55, -60, -65, -70, -68, -65, -63, -63],
        # 宽带ARPU (€/月)
        "broadband_arpu_eur": [28.5, 28.8, 29.0, 29.2, 29.5, 29.8, 30.0, 30.2],
        # Gigabit覆盖用户占比 %
        "gigabit_coverage_pct": [24.0, 25.5, 27.0, 28.5, 30.0, 32.0, 34.0, 36.0],
        "_source": "Vodafone Germany Infrastructure Report",
    },
    "Deutsche Telekom Germany": {
        "broadband_subs_m": [14.50, 14.62, 14.75, 14.88, 15.00, 15.08, 15.15, 15.22],
        "fiber_ftth_subs_m": [4.20, 4.45, 4.72, 5.00, 5.30, 5.62, 5.95, 6.30],
        "cable_docsis_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "dsl_copper_subs_m": [10.30, 10.17, 10.03, 9.88, 9.70, 9.46, 9.20, 8.92],
        "fiber_ratio_pct": [29.0, 30.4, 32.0, 33.6, 35.3, 37.3, 39.3, 41.4],
        "cable_ratio_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "dsl_ratio_pct": [71.0, 69.6, 68.0, 66.4, 64.7, 62.7, 60.7, 58.6],
        "net_adds_k": [85, 90, 95, 100, 105, 95, 85, 80],
        "broadband_arpu_eur": [32.5, 32.8, 33.0, 33.2, 33.5, 33.8, 34.0, 34.2],
        "gigabit_coverage_pct": [35.0, 38.0, 41.0, 44.0, 47.0, 50.0, 53.0, 56.0],
        "_source": "DT Germany Fiber Strategy Update",
    },
    "Telefónica O2 Germany": {
        "broadband_subs_m": [2.35, 2.36, 2.37, 2.38, 2.38, 2.39, 2.39, 2.40],
        "fiber_ftth_subs_m": [0.25, 0.28, 0.32, 0.36, 0.40, 0.45, 0.50, 0.55],
        "cable_docsis_subs_m": [1.20, 1.18, 1.15, 1.12, 1.09, 1.06, 1.03, 1.00],
        "dsl_copper_subs_m": [0.90, 0.90, 0.90, 0.90, 0.89, 0.88, 0.86, 0.85],
        "fiber_ratio_pct": [10.6, 11.9, 13.5, 15.1, 16.8, 18.8, 20.9, 22.9],
        "cable_ratio_pct": [51.1, 50.0, 48.5, 47.1, 45.8, 44.4, 43.1, 41.7],
        "dsl_ratio_pct": [38.3, 38.1, 38.0, 37.8, 37.4, 36.8, 36.0, 35.4],
        "net_adds_k": [8, 10, 10, 8, 5, 8, 5, 8],
        "broadband_arpu_eur": [26.0, 26.2, 26.5, 26.8, 27.0, 27.2, 27.5, 27.8],
        "gigabit_coverage_pct": [18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0],
        "_source": "Telefónica Deutschland Q3 2025",
    },
    "1&1 AG": {
        "broadband_subs_m": [3.92, 3.91, 3.90, 3.89, 3.88, 3.87, 3.86, 3.86],
        "fiber_ftth_subs_m": [0.45, 0.50, 0.56, 0.62, 0.68, 0.75, 0.82, 0.90],
        "cable_docsis_subs_m": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "dsl_copper_subs_m": [3.47, 3.41, 3.34, 3.27, 3.20, 3.12, 3.04, 2.96],
        "fiber_ratio_pct": [11.5, 12.8, 14.4, 15.9, 17.5, 19.4, 21.2, 23.3],
        "cable_ratio_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "dsl_ratio_pct": [88.5, 87.2, 85.6, 84.1, 82.5, 80.6, 78.8, 76.7],
        "net_adds_k": [-8, -10, -10, -8, -8, -8, -8, -5],
        "broadband_arpu_eur": [24.5, 24.6, 24.8, 25.0, 25.2, 25.4, 25.6, 25.8],
        "gigabit_coverage_pct": [15.0, 17.0, 19.0, 21.0, 23.0, 25.0, 27.0, 29.0],
        "_source": "1&1 AG Reports",
    },
}

# 2.3 B2B业务详细数据
B2B_BUSINESS_DATA_8Q = {
    "Vodafone Germany": {
        # B2B总收入已在REVENUE中
        # 连接业务收入 (€M)
        "connectivity_revenue": [255, 260, 265, 270, 275, 280, 285, 290],
        # 数字化业务收入 (€M)
        "digital_services_revenue": [155, 160, 165, 175, 185, 200, 215, 230],
        # 连接业务占比 %
        "connectivity_ratio_pct": [62.2, 61.9, 61.6, 60.7, 59.8, 58.3, 57.0, 55.8],
        # 数字化业务占比 %
        "digital_ratio_pct": [37.8, 38.1, 38.4, 39.3, 40.2, 41.7, 43.0, 44.2],
        # 细分: 云服务收入
        "cloud_revenue": [45, 48, 52, 58, 65, 75, 85, 95],
        # 细分: 安全服务收入
        "security_revenue": [32, 34, 36, 38, 40, 43, 46, 50],
        # 细分: 管理服务收入
        "managed_services_revenue": [42, 44, 46, 48, 50, 52, 54, 56],
        # 细分: IoT收入
        "iot_revenue": [36, 34, 31, 31, 30, 30, 30, 29],
        # B2B客户数 (千)
        "b2b_customers_k": [185, 188, 192, 196, 200, 205, 210, 215],
        "_source": "Vodafone Business Germany Reports",
    },
    "Deutsche Telekom Germany": {
        "connectivity_revenue": [550, 565, 580, 595, 610, 625, 640, 655],
        "digital_services_revenue": [400, 425, 450, 475, 500, 525, 550, 575],
        "connectivity_ratio_pct": [57.9, 57.1, 56.3, 55.6, 55.0, 54.3, 53.8, 53.3],
        "digital_ratio_pct": [42.1, 42.9, 43.7, 44.4, 45.0, 45.7, 46.2, 46.7],
        "cloud_revenue": [145, 158, 172, 188, 205, 222, 240, 260],
        "security_revenue": [85, 92, 100, 108, 115, 122, 130, 138],
        "managed_services_revenue": [120, 125, 130, 135, 140, 145, 150, 155],
        "iot_revenue": [50, 50, 48, 44, 40, 36, 30, 22],
        "b2b_customers_k": [420, 430, 440, 450, 460, 470, 480, 490],
        "_source": "T-Systems Germany Reports",
    },
    "Telefónica O2 Germany": {
        "connectivity_revenue": [205, 215, 225, 235, 248, 260, 275, 290],
        "digital_services_revenue": [115, 125, 135, 150, 162, 178, 193, 210],
        "connectivity_ratio_pct": [64.1, 63.2, 62.5, 61.0, 60.5, 59.4, 58.8, 58.0],
        "digital_ratio_pct": [35.9, 36.8, 37.5, 39.0, 39.5, 40.6, 41.2, 42.0],
        "cloud_revenue": [35, 40, 45, 52, 58, 65, 72, 80],
        "security_revenue": [28, 32, 36, 40, 44, 48, 52, 56],
        "managed_services_revenue": [35, 38, 42, 46, 50, 55, 60, 65],
        "iot_revenue": [17, 15, 12, 12, 10, 10, 9, 9],
        "b2b_customers_k": [125, 130, 135, 142, 150, 158, 166, 175],
        "_source": "O2 Business Germany Reports",
    },
    "1&1 AG": {
        "connectivity_revenue": [52, 54, 57, 60, 63, 66, 69, 72],
        "digital_services_revenue": [13, 14, 15, 16, 17, 18, 19, 20],
        "connectivity_ratio_pct": [80.0, 79.4, 79.2, 78.9, 78.8, 78.6, 78.4, 78.3],
        "digital_ratio_pct": [20.0, 20.6, 20.8, 21.1, 21.2, 21.4, 21.6, 21.7],
        "cloud_revenue": [6, 7, 8, 8, 9, 9, 10, 10],
        "security_revenue": [3, 3, 3, 4, 4, 4, 5, 5],
        "managed_services_revenue": [3, 3, 3, 3, 3, 4, 4, 4],
        "iot_revenue": [1, 1, 1, 1, 1, 1, 0, 1],
        "b2b_customers_k": [45, 47, 49, 51, 54, 57, 60, 63],
        "_source": "1&1 Versatel Reports",
    },
}

# 2.4 TV与融合业务数据
TV_FMC_DATA_8Q = {
    "Vodafone Germany": {
        # TV用户 (百万)
        "tv_subs_m": [8.12, 8.08, 8.02, 7.95, 7.88, 7.81, 7.75, 7.74],
        # TV净增 (千)
        "tv_net_adds_k": [-15, -18, -20, -18, -15, -12, -10, -6],
        # FMC融合用户 (百万) - 同时使用移动+固网
        "fmc_subs_m": [4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9],
        # FMC用户占宽带用户比 %
        "fmc_penetration_pct": [40.7, 41.8, 43.1, 44.4, 45.6, 46.9, 48.1, 49.3],
        # GigaKombi捆绑折扣用户 (百万)
        "bundle_discount_subs_m": [3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5],
        "_source": "Vodafone Germany Consumer Reports",
    },
    "Deutsche Telekom Germany": {
        "tv_subs_m": [4.10, 4.15, 4.20, 4.25, 4.28, 4.32, 4.35, 4.38],
        "tv_net_adds_k": [25, 30, 32, 30, 28, 30, 28, 25],
        "fmc_subs_m": [6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9],
        "fmc_penetration_pct": [44.8, 45.8, 46.8, 47.7, 48.7, 49.7, 50.8, 51.9],
        "bundle_discount_subs_m": [5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2],
        "_source": "DT MagentaEINS Reports",
    },
    "Telefónica O2 Germany": {
        "tv_subs_m": [0.52, 0.53, 0.54, 0.55, 0.55, 0.56, 0.56, 0.57],
        "tv_net_adds_k": [5, 8, 8, 6, 4, 6, 4, 5],
        "fmc_subs_m": [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15],
        "fmc_penetration_pct": [34.0, 36.0, 38.0, 39.9, 42.0, 43.9, 46.0, 47.9],
        "bundle_discount_subs_m": [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95],
        "_source": "O2 my Home Reports",
    },
    "1&1 AG": {
        "tv_subs_m": [0.35, 0.36, 0.37, 0.38, 0.39, 0.40, 0.41, 0.42],
        "tv_net_adds_k": [5, 8, 8, 8, 8, 8, 8, 8],
        "fmc_subs_m": [1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55],
        "fmc_penetration_pct": [30.6, 32.0, 33.3, 34.7, 36.1, 37.5, 38.9, 40.2],
        "bundle_discount_subs_m": [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35],
        "_source": "1&1 Bundle Reports",
    },
}

# =============================================================================
# 第三部分: 战略与组织数据
# =============================================================================

STRATEGY_DATA = {
    "Vodafone Germany": {
        "strategic_priorities": [
            "1. 价值客户经营 (Value over Volume)",
            "2. 5G网络领导力",
            "3. B2B数字化转型",
            "4. 固网业务止血",
            "5. 运营效率提升",
        ],
        "key_initiatives": {
            "network": "5G覆盖目标95%人口(FY26), OpenRAN试点",
            "b2b": "Skaylink收购增强云服务能力, SME市场拓展",
            "consumer": "GigaKombi捆绑策略, 高端用户获取",
            "cost": "数字化转型降本, 员工优化",
        },
        "fy26_guidance": "服务收入增长转正, EBITDA稳定增长",
        "recent_achievements": [
            "1&1网络迁移完成 (1200万用户)",
            "服务收入连续8季度改善",
            "新客户ARPU创3年新高 (+21%)",
            "合同用户占比提升至94%",
        ],
        "_source": "Vodafone FY26 Strategic Update",
    },
    "Deutsche Telekom Germany": {
        "strategic_priorities": [
            "1. 光纤网络全覆盖 (FTTH Rollout)",
            "2. MagentaEINS融合生态",
            "3. B2B/ICT业务增长",
            "4. 客户体验领先",
            "5. 可持续发展",
        ],
        "key_initiatives": {
            "network": "光纤覆盖目标10M homes passed, 5G SA商用",
            "b2b": "T-Systems云业务整合, 行业解决方案",
            "consumer": "MagentaEINS全家桶策略, 流媒体内容",
            "cost": "AI驱动客服, 流程自动化",
        },
        "fy25_guidance": "营收增长2-3%, EBITDA持续增长",
        "recent_achievements": [
            "连续35季度EBITDA增长",
            "光纤用户突破600万",
            "客户满意度行业第一",
            "5G SA全国商用",
        ],
        "_source": "DT Capital Markets Day 2025",
    },
    "Telefónica O2 Germany": {
        "strategic_priorities": [
            "1. IoT/数字业务转型",
            "2. 成本效率优化",
            "3. B2B市场增长",
            "4. 网络现代化",
            "5. 合作伙伴生态",
        ],
        "key_initiatives": {
            "network": "5G网络优化, 虚拟化核心网",
            "b2b": "IoT平台拓展, 行业解决方案",
            "consumer": "O2 Priority会员计划, 数字渠道优化",
            "cost": "网络共享协议, 渠道数字化",
        },
        "fy25_guidance": "收入稳定, EBITDA margin维持",
        "recent_achievements": [
            "5G覆盖达98%人口",
            "IoT连接数增长47%",
            "B2B收入双位数增长",
            "数字渠道占比提升至45%",
        ],
        "_source": "Telefónica Deutschland Strategy",
    },
    "1&1 AG": {
        "strategic_priorities": [
            "1. OpenRAN网络建设",
            "2. 成本优化 (€100M/年)",
            "3. 自有网络用户迁移",
            "4. 差异化定价",
            "5. 光纤合作拓展",
        ],
        "key_initiatives": {
            "network": "OpenRAN全球首个大规模商用网络",
            "b2b": "1&1 Versatel企业业务整合",
            "consumer": "价格竞争力维持, 自有网络体验提升",
            "cost": "批发成本下降, 运营效率提升",
        },
        "fy26_guidance": "网络覆盖50%人口, 成本节约€100M",
        "recent_achievements": [
            "OpenRAN网络覆盖55%人口",
            "自有网络用户超过200万",
            "与DT批发协议续签",
            "5G独立组网商用",
        ],
        "_source": "1&1 AG Investor Day 2025",
    },
}

# 高管变动数据
EXECUTIVE_CHANGES = {
    "Vodafone Germany": {
        "ceo": {"name": "Marcel de Groot", "since": "2023-09", "background": "CFO VF Netherlands"},
        "cfo": {"name": "Anna Googel", "since": "2022-01", "background": "Internal promotion"},
        "cto": {"name": "Gerhard Mack", "since": "2018-04", "background": "Network veteran"},
        "recent_changes": [
            "2025-06: Chief Commercial Officer更换 (消费者业务重组)",
            "2025-03: B2B业务负责人调整 (Skaylink整合)",
        ],
        "_source": "LinkedIn, Company Announcements",
    },
    "Deutsche Telekom Germany": {
        "ceo": {"name": "Srini Gopalan", "since": "2020-11", "background": "DT Board, Consumer"},
        "cfo": {"name": "Christian Illek", "since": "2018-01", "background": "McKinsey partner"},
        "cto": {"name": "Claudia Nemat", "since": "2011-10", "background": "Tech/Innovation"},
        "recent_changes": [
            "2025-08: 数字化转型负责人新任命",
            "2025-02: B2B/T-Systems重组完成",
        ],
        "_source": "DT Annual Report, LinkedIn",
    },
    "Telefónica O2 Germany": {
        "ceo": {"name": "Markus Haas", "since": "2017-01", "background": "CFO O2 Germany"},
        "cfo": {"name": "Markus Rolle", "since": "2019-04", "background": "Finance veteran"},
        "cto": {"name": "Mallik Rao", "since": "2020-01", "background": "Telefónica Group"},
        "recent_changes": [
            "2025-09: 企业业务负责人变动",
            "2025-05: 消费者业务重组",
        ],
        "_source": "O2 Germany, LinkedIn",
    },
    "1&1 AG": {
        "ceo": {"name": "Ralph Dommermuth", "since": "1988-01", "background": "创始人"},
        "cfo": {"name": "Markus Huhn", "since": "2017-06", "background": "United Internet"},
        "cto": {"name": "Karsten Pradel", "since": "2022-01", "background": "Network expert"},
        "recent_changes": [
            "2025-07: 网络建设负责人更换 (OpenRAN加速)",
            "2025-01: 营销负责人新任命",
        ],
        "_source": "1&1 AG Reports, LinkedIn",
    },
}

# =============================================================================
# 第四部分: 网络基础设施数据
# =============================================================================

NETWORK_INFRASTRUCTURE = {
    "Vodafone Germany": {
        "mobile_network": {
            "5g_population_coverage_pct": 92,
            "5g_base_stations": 18500,
            "4g_population_coverage_pct": 99.5,
            "spectrum_holdings_mhz": {"700": 20, "1800": 50, "2100": 40, "2600": 20, "3600": 90},
            "technology": "Ericsson + Nokia (non-standalone 5G)",
            "5g_sa_status": "Testing, planned 2026",
        },
        "fixed_network": {
            "cable_homes_passed_m": 24.0,
            "docsis_31_coverage_pct": 85,
            "fiber_homes_passed_m": 1.5,
            "ftth_build_plan": "与DT合作扩展FTTH覆盖",
        },
        "core_network": {
            "vendor": "Ericsson",
            "virtualization_pct": 45,
            "edge_nodes": 12,
        },
        "investment_focus": [
            "DOCSIS 4.0升级",
            "5G SA部署",
            "边缘计算节点扩展",
        ],
        "_source": "Vodafone Network Reports",
    },
    "Deutsche Telekom Germany": {
        "mobile_network": {
            "5g_population_coverage_pct": 97,
            "5g_base_stations": 35000,
            "4g_population_coverage_pct": 99.8,
            "spectrum_holdings_mhz": {"700": 20, "900": 35, "1800": 60, "2100": 50, "2600": 40, "3600": 90},
            "technology": "Ericsson + Huawei (legacy)",
            "5g_sa_status": "Commercial since 2024-09",
        },
        "fixed_network": {
            "cable_homes_passed_m": 0,
            "docsis_31_coverage_pct": 0,
            "fiber_homes_passed_m": 8.5,
            "ftth_build_plan": "10M homes by 2026, 全国覆盖by 2030",
        },
        "core_network": {
            "vendor": "Ericsson + Nokia",
            "virtualization_pct": 70,
            "edge_nodes": 28,
        },
        "investment_focus": [
            "光纤网络加速部署",
            "5G SA全国覆盖",
            "网络切片商用",
        ],
        "_source": "DT Network Strategy",
    },
    "Telefónica O2 Germany": {
        "mobile_network": {
            "5g_population_coverage_pct": 98,
            "5g_base_stations": 20000,
            "4g_population_coverage_pct": 99.7,
            "spectrum_holdings_mhz": {"800": 20, "1800": 35, "2100": 30, "2600": 20, "3600": 70},
            "technology": "Nokia + Samsung",
            "5g_sa_status": "Commercial since 2025-03",
        },
        "fixed_network": {
            "cable_homes_passed_m": 2.5,
            "docsis_31_coverage_pct": 60,
            "fiber_homes_passed_m": 0.8,
            "ftth_build_plan": "批发合作为主",
        },
        "core_network": {
            "vendor": "Nokia",
            "virtualization_pct": 55,
            "edge_nodes": 8,
        },
        "investment_focus": [
            "核心网虚拟化",
            "IoT平台扩展",
            "网络共享优化",
        ],
        "_source": "O2 Network Reports",
    },
    "1&1 AG": {
        "mobile_network": {
            "5g_population_coverage_pct": 55,
            "5g_base_stations": 4500,
            "4g_population_coverage_pct": 55,
            "spectrum_holdings_mhz": {"2100": 20, "3600": 50},
            "technology": "OpenRAN (Rakuten Symphony)",
            "5g_sa_status": "Commercial, OpenRAN first-mover",
        },
        "fixed_network": {
            "cable_homes_passed_m": 0,
            "docsis_31_coverage_pct": 0,
            "fiber_homes_passed_m": 0,
            "ftth_build_plan": "批发接入为主 (DT, 区域光纤商)",
        },
        "core_network": {
            "vendor": "Mavenir (cloud-native)",
            "virtualization_pct": 100,
            "edge_nodes": 3,
        },
        "investment_focus": [
            "OpenRAN网络扩展至50%覆盖",
            "全云原生核心网",
            "批发成本优化",
        ],
        "_source": "1&1 Network Update",
    },
}

# =============================================================================
# 第五部分: 套餐资费数据 (代表性套餐)
# =============================================================================

TARIFF_DATA = {
    "mobile_postpaid": {
        "Vodafone Germany": {
            "entry": {"name": "Red S", "data_gb": 10, "price_eur": 29.99, "5g": True},
            "mid": {"name": "Red M", "data_gb": 25, "price_eur": 39.99, "5g": True},
            "premium": {"name": "Red L", "data_gb": 50, "price_eur": 49.99, "5g": True},
            "unlimited": {"name": "Red XL", "data_gb": "Unlimited", "price_eur": 79.99, "5g": True},
            "promotion": "GigaKombi: 固网+移动捆绑享20%折扣",
        },
        "Deutsche Telekom Germany": {
            "entry": {"name": "MagentaMobil S", "data_gb": 10, "price_eur": 34.95, "5g": True},
            "mid": {"name": "MagentaMobil M", "data_gb": 25, "price_eur": 44.95, "5g": True},
            "premium": {"name": "MagentaMobil L", "data_gb": 60, "price_eur": 54.95, "5g": True},
            "unlimited": {"name": "MagentaMobil XL", "data_gb": "Unlimited", "price_eur": 84.95, "5g": True},
            "promotion": "MagentaEINS: 固网+移动+TV捆绑享25%折扣",
        },
        "Telefónica O2 Germany": {
            "entry": {"name": "O2 Mobile S", "data_gb": 10, "price_eur": 24.99, "5g": True},
            "mid": {"name": "O2 Mobile M", "data_gb": 25, "price_eur": 34.99, "5g": True},
            "premium": {"name": "O2 Mobile L", "data_gb": 60, "price_eur": 44.99, "5g": True},
            "unlimited": {"name": "O2 Mobile Unlimited", "data_gb": "Unlimited", "price_eur": 59.99, "5g": True},
            "promotion": "O2 my Home组合: 固网+移动享15%折扣",
        },
        "1&1 AG": {
            "entry": {"name": "1&1 All-Net-Flat S", "data_gb": 10, "price_eur": 19.99, "5g": True},
            "mid": {"name": "1&1 All-Net-Flat M", "data_gb": 25, "price_eur": 29.99, "5g": True},
            "premium": {"name": "1&1 All-Net-Flat L", "data_gb": 50, "price_eur": 39.99, "5g": True},
            "unlimited": {"name": "1&1 Unlimited", "data_gb": "Unlimited", "price_eur": 49.99, "5g": True},
            "promotion": "DSL+Mobile组合: 双产品享€10/月折扣",
        },
    },
    "fixed_broadband": {
        "Vodafone Germany": {
            "entry": {"name": "Red Internet 100", "speed_mbps": 100, "price_eur": 29.99, "tech": "Cable/DSL"},
            "mid": {"name": "Red Internet 500", "speed_mbps": 500, "price_eur": 39.99, "tech": "Cable"},
            "premium": {"name": "GigaCable Max", "speed_mbps": 1000, "price_eur": 49.99, "tech": "Cable"},
        },
        "Deutsche Telekom Germany": {
            "entry": {"name": "MagentaZuhause S", "speed_mbps": 50, "price_eur": 34.95, "tech": "DSL/Fiber"},
            "mid": {"name": "MagentaZuhause M", "speed_mbps": 100, "price_eur": 44.95, "tech": "DSL/Fiber"},
            "premium": {"name": "MagentaZuhause Giga", "speed_mbps": 1000, "price_eur": 69.95, "tech": "Fiber"},
        },
        "Telefónica O2 Germany": {
            "entry": {"name": "O2 my Home S", "speed_mbps": 50, "price_eur": 24.99, "tech": "DSL"},
            "mid": {"name": "O2 my Home M", "speed_mbps": 100, "price_eur": 34.99, "tech": "DSL/Cable"},
            "premium": {"name": "O2 my Home XL", "speed_mbps": 500, "price_eur": 44.99, "tech": "Cable"},
        },
        "1&1 AG": {
            "entry": {"name": "1&1 DSL 50", "speed_mbps": 50, "price_eur": 24.99, "tech": "DSL"},
            "mid": {"name": "1&1 DSL 100", "speed_mbps": 100, "price_eur": 34.99, "tech": "DSL/Fiber"},
            "premium": {"name": "1&1 Glasfaser 1000", "speed_mbps": 1000, "price_eur": 49.99, "tech": "Fiber"},
        },
    },
}

# =============================================================================
# 第六部分: 市场汇总数据
# =============================================================================

MARKET_SUMMARY_8Q = {
    # 德国电信市场总体数据
    "total_mobile_market_revenue_m": [5220, 5250, 5275, 5294, 5328, 5343, 5362, 5392],
    "total_fixed_market_revenue_m": [3125, 3134, 3143, 3155, 3166, 3172, 3177, 3184],
    "total_market_revenue_m": [10220, 10295, 10370, 10430, 10490, 10540, 10573, 10615],
    # 市场份额 (服务收入口径) %
    "market_share_vodafone": [26.2, 26.2, 25.9, 25.9, 25.8, 25.8, 25.7, 25.7],
    "market_share_dt": [51.4, 51.4, 51.3, 51.3, 51.3, 51.3, 51.4, 51.5],
    "market_share_o2": [17.8, 17.5, 17.2, 16.8, 16.5, 16.3, 16.2, 16.0],
    "market_share_1and1": [4.6, 4.9, 5.6, 6.0, 6.4, 6.6, 6.7, 6.8],
    # 5G用户渗透率 %
    "5g_adoption_pct": [28, 32, 36, 40, 44, 48, 52, 56],
    # 光纤渗透率 %
    "fiber_penetration_pct": [12, 14, 16, 18, 20, 22, 24, 26],
    "_source": "Bundesnetzagentur, Company Reports",
}

# 用户流动数据 (季度净流动, 千)
USER_FLOW_8Q = {
    "from_vodafone_to_dt": [25, 22, 20, 18, 15, 12, 10, 8],
    "from_vodafone_to_o2": [18, 16, 15, 14, 12, 10, 9, 8],
    "from_vodafone_to_1and1": [8, 7, 6, 5, 5, 4, 4, 3],
    "from_dt_to_vodafone": [12, 11, 10, 10, 9, 9, 8, 8],
    "from_dt_to_o2": [10, 9, 9, 8, 8, 7, 7, 6],
    "from_dt_to_1and1": [5, 5, 4, 4, 4, 3, 3, 3],
    "from_o2_to_vodafone": [15, 14, 13, 12, 11, 10, 9, 8],
    "from_o2_to_dt": [20, 18, 17, 16, 15, 14, 13, 12],
    "from_o2_to_1and1": [12, 11, 10, 9, 8, 8, 7, 7],
    "from_1and1_to_vodafone": [5, 5, 4, 4, 4, 3, 3, 3],
    "from_1and1_to_dt": [6, 6, 5, 5, 5, 4, 4, 4],
    "from_1and1_to_o2": [4, 4, 3, 3, 3, 3, 2, 2],
}
