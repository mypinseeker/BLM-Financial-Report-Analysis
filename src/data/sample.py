"""Generate sample BLM financial data for testing and demonstration."""

import numpy as np
import pandas as pd


BLM_PROGRAMS = [
    "Wildlife Management",
    "Range Management",
    "Forestry",
    "Oil & Gas Management",
    "Mining Law Administration",
    "Recreation Management",
    "Cadastral Survey",
    "Fire Management",
    "Wild Horse & Burro",
    "Land & Realty Management",
    "Cultural Resources",
    "Soil/Water/Air Management",
    "Hazardous Materials",
    "Energy & Minerals",
    "National Conservation Lands",
]

BLM_STATES = [
    "Alaska", "Arizona", "California", "Colorado", "Idaho",
    "Montana", "Nevada", "New Mexico", "Oregon", "Utah", "Wyoming",
]


def generate_sample_data(
    n_records: int = 200,
    start_year: int = 2019,
    end_year: int = 2025,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate realistic sample BLM financial data.

    Args:
        n_records: Number of records to generate.
        start_year: Start year for date range.
        end_year: End year for date range.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with sample financial data.
    """
    rng = np.random.default_rng(seed)

    categories = rng.choice(BLM_PROGRAMS, n_records)
    states = rng.choice(BLM_STATES, n_records)

    # Generate fiscal years
    fiscal_years = rng.integers(start_year, end_year + 1, n_records)

    # Generate dates within fiscal years
    dates = []
    for fy in fiscal_years:
        month = rng.integers(1, 13)
        day = rng.integers(1, 29)  # safe for all months
        dates.append(f"{fy}-{month:02d}-{day:02d}")

    # Generate budget amounts (base amounts vary by program)
    base_budgets = {prog: rng.uniform(500_000, 50_000_000) for prog in BLM_PROGRAMS}
    budgets = np.array([base_budgets[cat] * rng.uniform(0.8, 1.2) for cat in categories])

    # Actual spending: usually close to budget, sometimes significantly over/under
    variance_factors = rng.normal(1.0, 0.15, n_records)
    # Add some outliers
    outlier_mask = rng.random(n_records) < 0.05
    variance_factors[outlier_mask] = rng.uniform(1.5, 2.5, outlier_mask.sum())
    actuals = budgets * variance_factors

    # Revenue (for some programs)
    revenue_programs = {"Oil & Gas Management", "Mining Law Administration", "Land & Realty Management"}
    revenues = np.where(
        np.isin(categories, list(revenue_programs)),
        rng.uniform(100_000, 30_000_000, n_records),
        0,
    )

    df = pd.DataFrame({
        "date": dates,
        "fiscal_year": fiscal_years,
        "state": states,
        "category": categories,
        "program": categories,
        "budget": np.round(budgets, 2),
        "actual": np.round(actuals, 2),
        "amount": np.round(actuals, 2),
        "revenue": np.round(revenues, 2),
        "description": [
            f"FY{fy} {cat} - {state}"
            for fy, cat, state in zip(fiscal_years, categories, states)
        ],
    })

    return df.sort_values("date").reset_index(drop=True)
