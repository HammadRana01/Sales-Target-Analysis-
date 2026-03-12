import pandas as pd 
from sqlalchemy import create_engine, text

# DATABASE CONFIGURATION

DB_USER = "postgres"
DB_PASS = "123456789"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Sales_target.db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# LOAD CSV

df = pd.read_csv(r"C:\\Users\\Ayushi\\OneDrive\\Desktop\\Project\\Sales_target Analysis\\Data\\train.csv")

# EXTRACT UNIQUE CUSTOMERS 
customers = (
    df[["Customer ID", "Customer Name", "Segment"]]
    .dropna()
    .drop_duplicates()
)

# LOAD INTO dim_customer
with engine.begin() as conn:
    for _, row in customers.iterrows():
        conn.execute(
            text("""
                 INSERT INTO dim_customer (customer_id, customer_name, segment)
                 VALUES (:cid, :cname, :segment)
                 ON CONFLICT (customer_id) DO NOTHING 
                """),
                {
                    "cid": row["Customer ID"],
                    "cname": row["Customer Name"],
                    "segment": row["Segment"]
                }
        )

print("dim_customer loaded successfully.")