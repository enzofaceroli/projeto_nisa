import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
def fetch_dataframe(query: str, params=None) -> pd.DataFrame:
    conn = get_connection()
    
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    
    finally:
        conn.close()
