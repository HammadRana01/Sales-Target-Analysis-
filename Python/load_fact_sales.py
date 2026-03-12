import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------------------------------
# 1️⃣ Database connection
# -------------------------------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:123456789@localhost:5432/Sales_target.db"
)

# -------------------------------------------------
# 2️⃣ Load CSV
# -------------------------------------------------
df = pd.read_csv(
    r"C:\Users\Ayushi\OneDrive\Desktop\Project\Sales_target Analysis\Data\train.csv"
)

# Normalize column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# -------------------------------------------------
# 3️⃣ Date handling
# -------------------------------------------------
df["Order_Date"] = pd.to_datetime(df["Order_Date"], dayfirst=True)
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], dayfirst=True)

df["order_date_id"] = df["Order_Date"].dt.strftime("%Y%m%d").astype(int)
df["ship_date_id"] = df["Ship_Date"].dt.strftime("%Y%m%d").astype(int)

# -------------------------------------------------
# 4️⃣ Region mapping
# -------------------------------------------------
region_map = {
    "East": 1,
    "West": 2,
    "Central": 3,
    "South": 4
}
df["region_id"] = df["Region"].map(region_map)

# -------------------------------------------------
# 5️⃣ Load dimension key mappings
# -------------------------------------------------
with engine.connect() as conn:
    customer_map = {
        row["customer_id"]: row["customer_key"]
        for row in conn.execute(
            text("SELECT customer_id, customer_key FROM dim_customer")
        ).mappings()
    }

    product_map = {
        row["product_id"]: row["product_key"]
        for row in conn.execute(
            text("SELECT product_id, product_key FROM dim_product")
        ).mappings()
    }

# -------------------------------------------------
# 6️⃣ Insert into fact_sales
# -------------------------------------------------
insert_stmt = text("""
    INSERT INTO fact_sales (
        order_id,
        row_id,
        order_date_id,
        ship_date_id,
        customer_key,
        product_key,
        region_id,
        sales_amount
    )
    VALUES (
        :order_id,
        :row_id,
        :order_date_id,
        :ship_date_id,
        :customer_key,
        :product_key,
        :region_id,
        :sales_amount
    )
""")

rows_inserted = 0

with engine.begin() as conn:  # auto-commit + rollback safety
    for _, r in df.iterrows():

        # Safety checks (NO silent corruption)
        if r["Customer_ID"] not in customer_map:
            continue
        if r["Product_ID"] not in product_map:
            continue
        if pd.isna(r["region_id"]):
            continue

        conn.execute(
            insert_stmt,
            {
                "order_id": r["Order_ID"],
                "row_id": int(r["Row_ID"]),
                "order_date_id": int(r["order_date_id"]),
                "ship_date_id": int(r["ship_date_id"]),
                "customer_key": customer_map[r["Customer_ID"]],
                "product_key": product_map[r["Product_ID"]],
                "region_id": int(r["region_id"]),
                "sales_amount": float(r["Sales"]),
            }
        )
        rows_inserted += 1

print(f"✅ fact_sales loaded successfully → {rows_inserted} rows inserted")
