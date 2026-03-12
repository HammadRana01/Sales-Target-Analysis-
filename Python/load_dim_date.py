import pandas as pd
from sqlalchemy import create_engine, text

# -----------------------------------
# DB connection
# -----------------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:123456789@localhost:5432/Sales_target.db"
)

# -----------------------------------
# Load CSV
# -----------------------------------
df = pd.read_csv(
    r"C:\\Users\\Ayushi\\OneDrive\\Desktop\\Project\\Sales_target Analysis\\Data\\train.csv"
)

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")

# Convert dates
df["Order_Date"] = pd.to_datetime(df["Order_Date"], dayfirst=True)
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], dayfirst=True)

# Combine both dates
all_dates = pd.concat([df["Order_Date"], df["Ship_Date"]]).dropna().unique()

# -----------------------------------
# Insert into dim_date
# -----------------------------------
query = text("""
    INSERT INTO dim_date
    (date_id, full_date, day, month, month_name, quarter, year)
    VALUES
    (:date_id, :full_date, :day, :month, :month_name, :quarter, :year)
    ON CONFLICT (date_id) DO NOTHING
""")

with engine.connect() as conn:
    for d in all_dates:
        conn.execute(
            query,
            {
                "date_id": int(d.strftime("%Y%m%d")),
                "full_date": d.date(),
                "day": d.day,
                "month": d.month,
                "month_name": d.strftime("%B"),
                "quarter": (d.month - 1) // 3 + 1,
                "year": d.year,
            }
        )
    conn.commit()

print("✅ dim_date loaded successfully")
