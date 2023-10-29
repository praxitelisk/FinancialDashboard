import streamlit as st
import pandas as pd

st.set_page_config(page_title="Financial Indicators", page_icon="🧮")

if "ticker_symbol" not in st.session_state:
    # set the initial default value of the slider widget
    st.session_state.ticker_symbol = 'AAPL'

ticker_symbol = st.sidebar.text_input('Type here the stock name IN CAPITAL LETTERS you need for analysis', st.session_state.ticker_symbol)
st.session_state.ticker_symbol = ticker_symbol

st.markdown("# Stock Closing Price and Financial Indicators")
st.sidebar.header("Financial Indicators")
st.write(
    """To Be Updated"""
)