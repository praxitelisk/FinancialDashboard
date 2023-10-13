import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import time
import datetime

import plotly.graph_objects as go
import plotly.express  as ex

st.set_page_config(page_title="Dataframe Profiling", page_icon="📈")

st.markdown("# Plotting Stock Data")
st.sidebar.header("Stock Data Profiling")

st.sidebar.write("Stock name:")
ticker_symbol = st.sidebar.text_input('Type here the stock name IN CAPITAL LETTERS you need for analysis', 'AAPL')

tickers = yf.Tickers(ticker_symbol)

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
    """This page illustrates pertinent information regarding financial assets and plotting with Streamlit. Enjoy!"""
)


#The code below writes the header for the web application 
equity_name =  tickers.tickers[ticker_symbol].info['shortName']
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

#columns: Open, High, Low, Close, Adj Close and Volume
st.dataframe(tickerDF)

# close price time series
financialCurrency =  tickers.tickers[ticker_symbol].info['financialCurrency']
st.write("## Stock Closing Price in " + financialCurrency)
st.line_chart(tickerDF.Close)

# candlestick plot
st.write("## Stock Closing Price candlestick plot in "+ financialCurrency)
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Candlestick(x=tickerDF.index, 
open=tickerDF['Open'], 
high=tickerDF['High'], 
low=tickerDF['Low'], 
close=tickerDF['Close']) )

st.plotly_chart(fig)

# price over years
mean_closing_price_per_year = tickerDF.groupby(tickerDF.index.year)['Close'].mean()

# Plot the result
st.write("#### Mean closing price over the years in "+ financialCurrency)
st.bar_chart(mean_closing_price_per_year)


# price histogram
st.write("#### Closing price histogram in "+ financialCurrency)
fig = ex.histogram(tickerDF, x="Close", nbins=20)
st.plotly_chart(fig, use_container_width=True)


# linechart for all features
col1, col2, col3 = st.columns(3)
with col1:
   st.write("#### Stock's Open price in "+ financialCurrency)
   st.line_chart(tickerDF["Open"])

with col2:
   st.write("#### Stock's High price in "+ financialCurrency)
   st.line_chart(tickerDF["High"])

with col3:
   st.write("#### Stock's Low price in "+ financialCurrency)
   st.line_chart(tickerDF["Low"])
   

col1, col2, col3 = st.columns(3)
with col1:
   st.write("#### Stock's Close price in "+ financialCurrency)
   st.line_chart(tickerDF["Close"])

with col2:
   st.write("#### Stock's Adj Close price in "+ financialCurrency)
   st.line_chart(tickerDF["Adj Close"])

with col3:
   st.write("#### Stock's Volume price in "+ financialCurrency)
   st.line_chart(tickerDF["Volume"])
   
   
# Create a correlation plot
# https://stackoverflow.com/questions/72195177/correlation-matrix-in-plotly
st.write("#### Correlations between stock's features")
df_corr = tickerDF.corr()

fig = go.Figure()
fig.add_trace(
    go.Heatmap(
        x = df_corr.columns,
        y = df_corr.index,
        z = np.array(df_corr),
        text=df_corr.values,
        texttemplate='%{text:.2f}'
    )
)
st.plotly_chart(fig)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")