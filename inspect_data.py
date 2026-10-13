import pandas as pd

visits = pd.read_csv(
    "data/visitation.csv",
    keep_default_na=True
)

print("\n--- First 10 records ---")
print(visits.head(10))

print("\n--- Missing values ---")
print(visits.isna().sum())

print("\n--- Duplicate records ---")
print("Exact duplicate rows:", visits.duplicated().sum())

print("\n--- Repeated visit IDs ---")
print(
    visits["visit_id"].value_counts()
    .loc[lambda x: x > 1]
)

print("\n--- Resort names ---")
print(visits["resort"].value_counts(dropna=False))

print("\n--- Invalid dates ---")
parsed_dates = pd.to_datetime(
    visits["visit_date"],
    errors="coerce"
)

print(
    visits.loc[
        parsed_dates.isna(),
        ["visit_id", "visit_date"]
    ]
)