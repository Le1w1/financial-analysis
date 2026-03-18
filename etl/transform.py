import pandas as pd
from sqlalchemy import create_engine
import time

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
    df["volatility_20"] = df["daily_return"].rolling(window=20).std()
    return df


def load_to_sql(df: pd.DataFrame, table_name: str, engine, if_exists: str = "replace") -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists=if_exists,
        index=True,
        index_label="date"
        )
    print(f"Carga exitosa: {table_name}")



if __name__ == "__main__":
    from extract import get_stock_data
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    engine = get_engine()
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

    for i, symbol in enumerate(symbols):
        print(f"Procesando {symbol}...")

        if_exists = "replace" if i == 0 else "append"

        df_raw = get_stock_data(symbol)
        load_to_sql(df_raw, "stock_prices", engine, if_exists)

        df_metrics = calculate_metrics(df_raw.copy())
        load_to_sql(df_metrics, "stock_metrics", engine, if_exists)

        df_raw.to_csv(os.path.join(BASE_DIR, f"data/{symbol}_prices.csv"))
        df_metrics.to_csv(os.path.join(BASE_DIR, f"data/{symbol}_metrics.csv"))

        print(f"{symbol} completado.")
        time.sleep(15)