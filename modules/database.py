import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URL

# ==============================
# CREATE DATABASE ENGINE
# ==============================

engine = create_engine(DATABASE_URL)

# ==============================
# SAVE DATA TO POSTGRESQL
# ==============================

def save_to_database(df):

    try:

        df.to_sql(
    "news_sentiment",
    engine,
    schema="public",
    if_exists="append",
    index=False
)
        

        print("✅ Data saved to PostgreSQL successfully!")

    except Exception as e:

        print("❌ Database Error:")
        print(e)

# ==============================
# FETCH DATA FROM POSTGRESQL
# ==============================

def fetch_data():

    try:

        query = """
        SELECT *
        FROM public.news_sentiment
        ORDER BY created_at DESC
        """

        df = pd.read_sql(query, engine)

        return df

    except Exception as e:

        print("❌ Fetch Error:")
        print(e)

        return pd.DataFrame()