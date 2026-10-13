
from pathlib import Path
import pandas as pd
import random

# Make the results reproducible each time you run the script
random.seed(42)

# Create the data folder
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Fictional resorts and pass products
resorts = [
    "Copper Mountain",
    "Winter Park",
    "Eldora",
    "Steamboat"
]

pass_types = ["Season Pass", "Midweek Pass", "Day Pass"]

# --------------------------------------------------
# 1. Generate pass sales
# --------------------------------------------------

passes = []

for i in range(1, 101):
    passes.append({
        "pass_id": f"P{i:04d}",
        "sale_date": (
            pd.Timestamp("2025-09-01")
            + pd.Timedelta(days=random.randint(0, 120))
        ).strftime("%Y-%m-%d"),
        "pass_type": random.choice(pass_types),
        "sale_amount": random.choice([299, 499, 799, 999]),
        "sales_channel": random.choice(
            ["Online", "Resort", "Retail Partner"]
        )
    })

passes_df = pd.DataFrame(passes)

# --------------------------------------------------
# 2. Generate visitation records
# --------------------------------------------------

visits = []

for i in range(1, 301):
    visits.append({
        "visit_id": f"V{i:04d}",
        "pass_id": f"P{random.randint(1, 100):04d}",
        "visit_date": (
            pd.Timestamp("2025-12-01")
            + pd.Timedelta(days=random.randint(0, 120))
        ).strftime("%Y-%m-%d"),
        "resort": random.choice(resorts),
        "visits": 1
    })

visits_df = pd.DataFrame(visits)

# --------------------------------------------------
# 3. Generate budget targets
# --------------------------------------------------

budgets = []

for month in range(1, 13):
    for resort in resorts:
        budgets.append({
            "month": f"2025-{month:02d}",
            "resort": resort,
            "budgeted_revenue": random.randint(50000, 150000),
            "budgeted_visits": random.randint(1000, 5000)
        })

budgets_df = pd.DataFrame(budgets)

# --------------------------------------------------
# 4. Introduce intentional data-quality problems
# --------------------------------------------------

# A. Inconsistent resort names
# These all refer to Copper Mountain.
visits_df.loc[0, "resort"] = "copper mountain"
visits_df.loc[1, "resort"] = "Copper Mtn"
visits_df.loc[2, "resort"] = " COPPER MOUNTAIN "

# B. Missing pass IDs
visits_df.loc[3, "pass_id"] = None
visits_df.loc[8, "pass_id"] = None

# C. Invalid dates
# Keep these as strings so they remain visible in the CSV.
visits_df.loc[4, "visit_date"] = "2025-13-45"
visits_df.loc[9, "visit_date"] = "not-a-date"

# D. Duplicate visit records
# Copy entire records, including the original visit IDs.
duplicates = visits_df.iloc[[10, 20, 30]].copy()
visits_df = pd.concat(
    [visits_df, duplicates],
    ignore_index=True
)

# E. An invalid resort name
visits_df.loc[5, "resort"] = "Copper Mountian"

# --------------------------------------------------
# 5. Save the CSV files
# --------------------------------------------------

passes_df.to_csv(DATA_DIR / "passes.csv", index=False)
visits_df.to_csv(DATA_DIR / "visitation.csv", index=False)
budgets_df.to_csv(DATA_DIR / "budget.csv", index=False)

print("Sample CSV files created successfully!")
print(f"Pass sales: {len(passes_df)} records")
print(f"Visitation: {len(visits_df)} records")
print(f"Budgets: {len(budgets_df)} records")
print(f"Files saved to: {DATA_DIR.resolve()}")
