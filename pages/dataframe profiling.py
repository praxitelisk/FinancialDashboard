import streamlit as st
import time
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Stocks")
st.sidebar.header("Plotting Stocks")
st.write(
    """This page illustrates pertinent information regarding financial assets, plotting and animation with
Streamlit. Enjoy!"""
)


#The code below writes the header for the web application 
st.write("""
### Stock Price Web Application

 
Shown are the stock closing **price** and ***volume*** of Amazon!

**Period**: May 2012 - May 2022
         
""")

ticker_symbol = 'AMZN'

#get ticker data by creating a ticker object

tickerDF = yf.download(ticker_symbol, start="2010-01-01")

#columns: Open, High, Low Close, Volume, Dividends and Stock Splits
st.dataframe(tickerDF)

st.write("""
         ## Stock Closing Price in USD
         """    )
st.line_chart(tickerDF.Close)

st.write("""
         ## Stock Volume in USD
         """    )
st.line_chart(tickerDF.Volume)


# candlestick
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Candlestick(x=tickerDF.index, 
open=tickerDF['Open'], 
high=tickerDF['High'], 
low=tickerDF['Low'], 
close=tickerDF['Close']) )

st.plotly_chart(fig)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")