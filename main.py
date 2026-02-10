from db.connection import fetch_dataframe
from db.queries import *
import pandas as pd

def main():
    df = peso_medio_por_coleta()
    
    print(df)
    
if __name__ == '__main__':
    main()
