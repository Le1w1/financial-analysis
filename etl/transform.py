import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "mssql+pyodbc://localhost\\SQLEXPRESS/financial_analysis"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
        )
# Si algún día se cambia el servidor, se modifica desde aca.

def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame: 
    df["MA20"] = df["close"].rolling(window=20).mean()
    df["MA50"] = df["close"].rolling(window=50).mean()
    df["daily_return"] = df["close"].pct_change()
    return df

def load_to_sql(df : pd.DataFrame, table_name: str, engine)-> None:
    df.to_sql(
        name= table_name,
        con= engine,
        if_exists="replace",
        index= True,
        index_label="date"
    )
    print(f"Carga exitosa: {table_name}")

if __name__ == "__main__":
    from extract import get_stock_data

    engine = get_engine()
    df_raw = get_stock_data("AAPL")
    load_to_sql(df_raw, "stock_prices",engine)

    df_metrics = calculate_metrics(df_raw.copy())
    load_to_sql(df_metrics,"stock_metrics",engine)