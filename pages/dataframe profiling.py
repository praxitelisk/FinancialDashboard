import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Stock Data")

st.sidebar.write("Stock name:")
ticker_symbol = st.sidebar.text_input('Type here the stock name IN CAPITAL LETTERS you need for analysis', 'AAPL')

tickers = yf.Tickers(ticker_symbol)
equity_name =  tickers.tickers[ticker_symbol].info['shortName']

st.sidebar.write("In case you need to search for stocks' names")
st.sidebar.link_button("Search stock names in Yahoo finance site", "https://finance.yahoo.com")



today = datetime.datetime.now()
earliest_year = today.year - 5
earliest_date = datetime.date(earliest_year, 1, 1)

dates = st.sidebar.date_input(
    "Select time period of historical data",
    (datetime.date(earliest_year, 1, 1), today),
    earliest_date,
    today,
    format="YYYY.MM.DD",
)


st.write(
    """This page illustrates pertinent information regarding financial assets and plotting with
Streamlit. Enjoy!"""
)


#The code below writes the header for the web application 
st.write("""
### Financial Assets - Historical Data

##### Financial Asset we are interested in: """+equity_name+"""

**Period**:"""+str(dates))

earliest_date = dates[0]
latest_date = dates[1]

#get ticker data by creating a ticker object

tickerDF = yf.download(ticker_symbol, 
start=''+str(dates[0].year)+'-'+str(dates[0].month)+'-'+str(dates[0].day), 
end=''+str(dates[1].year)+'-'+str(dates[1].month)+'-'+str(dates[1].day))

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
st.write("""
         ## Stock Closing Price candlestick
         """    )
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