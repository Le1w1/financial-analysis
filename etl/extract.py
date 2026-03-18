import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_data(symbol: str, outputsize: str = "compact") -> pd.DataFrame:
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL,params=params)
    data = response.json()

    time_series = data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.columns = ["open","high","low","close","volume"]
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df = df.sort_index()
    df["symbol"] = symbol

    return df

#En lugar de tener el código suelto celda por celda como en el notebook, ahora está encapsulado en una función get_stock_data() que recibe un símbolo como parámetro y devuelve un DataFrame limpio.

if __name__ == "__main__":
    df = get_stock_data("AAPL")
    print(df.shape)
    print(df.head())

#El bloque if __name__ == "__main__" permite ejecutar el archivo directamente para probarlo, pero no interfiere cuando lo importás desde otro archivo.