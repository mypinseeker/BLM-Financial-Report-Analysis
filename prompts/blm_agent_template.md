# BLM (Business Leadership Model) Financial Report Analysis Template

## Overview

The **Business Leadership Model (BLM)** is a strategic management framework that bridges the gap between strategy formulation and execution. Originally developed by IBM and widely adopted by leading enterprises (e.g., Huawei), the BLM framework ensures that strategic intent translates into tangible business results.

This template guides the automated analysis of publicly listed companies' annual financial reports through the BLM lens.

---

## BLM Framework Structure

### Part 1: Strategy (战略)

| Dimension | Description | Key Data Points |
|-----------|-------------|-----------------|
| **Market Insight (市场洞察)** | Understanding of market trends, customer needs, competitor landscape | Revenue trends, market share, segment analysis, geographic breakdown |
| **Strategic Intent (战略意图)** | Company's vision, mission, and strategic goals | Stated strategic priorities, long-term targets, guidance |
| **Innovation Focus (创新焦点)** | R&D investment, new products, digital transformation | R&D expenditure, capex, patent activity, new product launches |
| **Business Design (业务设计)** | Business model, value proposition, revenue model | Revenue mix, margin structure, customer segments, partnerships |

### Part 2: Execution (执行)

| Dimension | Description | Key Data Points |
|-----------|-------------|-----------------|
| **Critical Tasks (关键任务)** | Key operational priorities and milestones | Major projects, M&A activity, restructuring, regulatory compliance |
| **Formal Organization (正式组织)** | Organizational structure and governance | Corporate structure, reporting segments, governance changes |
| **Talent (人才)** | Workforce strategy, headcount, talent development | Employee count, compensation, training investment, leadership changes |
| **Culture & Climate (氛围与文化)** | Corporate culture, ESG, stakeholder engagement | ESG scores, sustainability reports, employee engagement, DEI initiatives |

### Gap Analysis (差距分析)

- **Performance Gap (业绩差距)**: Gap between current results and strategic targets
- **Opportunity Gap (机会差距)**: Unrealized market opportunities identified through analysis

---

## Agent Instructions

### Step 1: Data Collection
1. Read the input parameters file to obtain: target URLs, country, fiscal year
2. For each company URL:
   - Fetch the investor relations / annual report page
   - Extract key financial metrics (Revenue, EBITDA, Net Income, Free Cash Flow)
   - Extract strategic commentary and outlook statements
   - Note any PDF links for annual reports

### Step 2: Data Cleaning & Organization
1. Normalize all financial figures to the same currency (EUR for European companies)
2. Organize data by BLM dimensions
3. Flag any missing or inconsistent data points

### Step 3: BLM Matrix Analysis
1. For each company, populate all 8 BLM dimensions with evidence from the financial reports
2. Rate each dimension: Strong (3), Moderate (2), Weak (1)
3. Identify Performance Gaps and Opportunity Gaps
4. Generate cross-company comparison where applicable

### Step 4: Report Generation
1. Output format: Markdown (.md)
2. Save to: `outputs/` directory
3. Filename convention: `BLM_Report_{Country}_{Year}_{YYYYMMDD}.md`
4. Include:
   - Executive Summary
   - Company-by-company BLM analysis
   - Comparative BLM matrix
   - Gap analysis
   - Strategic recommendations
   - Data sources and methodology notes

---

## Output Report Structure

```
# BLM Financial Analysis Report: {Country} {Year}

## Executive Summary
## Company Analysis
### Company 1
#### Strategy Dimensions
#### Execution Dimensions
#### Gap Analysis
### Company 2
...
## Comparative BLM Matrix
## Strategic Insights & Recommendations
## Methodology & Data Sources
```

---

## Quality Standards
- All financial figures must cite their source
- Analysis must be evidence-based, not speculative
- Each BLM dimension must have at least 2 supporting data points
- Report should be actionable for strategic decision-makers
