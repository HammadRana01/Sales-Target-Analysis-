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

# TAKE UNIQUE CATEGORY + SUB-CATEGORY
categories = df[["Category", "Sub-Category"]].drop_duplicates()

# INSERT INTO dim_category
with engine.begin() as conn:
    for _, row in categories.iterrows():
        conn.execute(
            text("""
                 INSERT INTO dim_category (category, sub_category)
                 VALUES (:cat, :subcat)
                 ON CONFLICT (category, sub_category) DO NOTHING
             """),
            {
             "cat": row["Category"],
             "subcat": row["Sub-Category"]
            }
        )

print("dim_category loaded.")