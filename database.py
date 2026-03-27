import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# Подключение к MySQL
engine = create_engine('mysql+pymysql://root:Anastasiia184@localhost/test_db')

# Загрузка данных через yfinance
ticker = yf.Ticker("AAPL")
df = ticker.history(period="1y")  # данные за год

# Сброс индекса (дата становится колонкой)
df.reset_index(inplace=True)

# Запись в MySQL
df.to_sql(
    name='apple_stocks',      # название таблицы
    con=engine,
    if_exists='replace',      # 'replace' / 'append' / 'fail'
    index=False
)
