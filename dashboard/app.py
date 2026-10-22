import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("Crypto Prices Dashboard")


@st.cache_resource
def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port=5432,
        database=os.getenv("POSTGRES_DB"),
    )
    return create_engine(url)


@st.cache_data(ttl=30)
def load_data():
    query = """
        SELECT symbol, fetched_minute, avg_price, min_price, max_price, samples
        FROM price_per_minute
        ORDER BY fetched_minute
    """
    df = pd.read_sql(query, get_engine())
    for col in ["avg_price", "min_price", "max_price"]:
        df[col] = df[col].astype(float)
    return df


df = load_data()

if df.empty:
    st.warning("No data yet. Run the pipeline first.")
    st.stop()

symbol = st.selectbox("Symbol", sorted(df["symbol"].unique()))
data = df[df["symbol"] == symbol]

latest = data.iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("Latest avg price", f"{latest['avg_price']:,.2f}")
col2.metric("Lowest price", f"{data['min_price'].min():,.2f}")
col3.metric("Highest price", f"{data['max_price'].max():,.2f}")

st.subheader(f"{symbol} price per minute (UTC)")
st.line_chart(data.set_index("fetched_minute")["avg_price"])

st.subheader("Latest rows")
st.dataframe(data.sort_values("fetched_minute", ascending=False))