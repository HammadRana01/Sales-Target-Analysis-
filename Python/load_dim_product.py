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



# UNIQUE PRODUCTS
products = (
    df[["Product ID", "Product Name", "Category", "Sub-Category"]]
    .drop_duplicates()
)

with engine.begin() as conn:
    
    #Load category lookup into memory
    category_map = conn.execute(
        text("SELECT category_id, category, sub_category FROM dim_category")
    ).fetchall()

    #convert to dictionary 
    category_dict = {
        (row.category, row.sub_category): row.category_id
        for row in category_map
    }

    for _, row in products.iterrows():
        key = (row["Category"], row["Sub-Category"])
        category_id = category_dict.get(key)
        if category_id is None:
            continue #skip unmapped category

        conn.execute(
            text("""
                 INSERT INTO dim_product (product_id, product_name, category_id)
                 VALUES (:pid, :pname, :cid)
                 ON CONFLICT (product_id) DO NOTHING
                """),
            {
                "pid": row["Product ID"],
                "pname": row["Product Name"],
                "cid": category_id
            }
        )

print("dim_product loaded successfully.")        