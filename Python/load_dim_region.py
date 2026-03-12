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

df = pd.read_csv(r"C:\Users\Ayushi\OneDrive\Desktop\Project\Sales_target Analysis\Data\train.csv")

# EXTRACT UNIQUE REGIONS
regions = df["Region"].dropna().unique()


# LOAD INTO dim_region

with engine.begin() as conn:
    for region in regions:
        conn.execute(
             text("""
                  INSERT INTO dim_region (region_name)
                  values (:region)
                  ON CONFLICT (region_name) DO NOTHING
                """),
                {"region": region}
        )    

print("dim_region loaded successfully.")        