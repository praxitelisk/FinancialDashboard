import streamlit as st
import time
import numpy as np
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

import pandas as pd
import streamlit as st
import yfinance as yf


#The code below writes the header for the web application 
st.write("""
# Stock Price Web Application

 
Shown are the stock closing **price** and ***volume*** of Amazon!

**Period**: May 2012 - May 2022
         
""")

ticker_symbol = 'AMZN'

#get ticker data by creating a ticker object

tickerDF = yf.download(ticker_symbol, start="2010-01-01")

#columns: Open, High, Low Close, Volume, Dividends and Stock Splits

st.write("""
         ## Stock Closing Price in USD
         """    )
st.line_chart(tickerDF.Close)

st.write("""
         ## Stock Volume in USD
         """    )
st.line_chart(tickerDF.Volume)


st.dataframe(tickerDF)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")