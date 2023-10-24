import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import time
import datetime

import plotly.graph_objects as go
import plotly.express  as ex

st.set_page_config(page_title="Dataframe Profiling", page_icon="📈")

# sidebar
st.sidebar.header("Financial Stock Data Profiling")

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

with st.container():
    st.markdown("# Inspecting Stock Data")
    st.write(
    """This page illustrates pertinent information regarding financial assets and plotting with Streamlit. Enjoy! 🧐"""
)
 
# equity_name =  tickers.tickers[ticker_symbol].info['shortName']

with st.container():
    st.markdown("""## Info and historical Data 📜""")
    
    tab1, tab2, tab3 = st.tabs(["Stock Info", "Company Summary", "Historical Data"])
    
    with tab1:
        st.markdown("## Stock info: ")
        st.markdown("### Due to API issues this page is not available at the moment")
        # st.markdown("- Full stock name: "+equity_name)
        # st.markdown("- Address: "+tickers.tickers[ticker_symbol].info['address1'])
        # st.markdown("- City: "+tickers.tickers[ticker_symbol].info['city'])
        # st.markdown("- Country: "+tickers.tickers[ticker_symbol].info['country'])
        # st.markdown("- Website: "+tickers.tickers[ticker_symbol].info['website'])
        # st.markdown("- Industry: "+tickers.tickers[ticker_symbol].info['industry'])
        # st.markdown("- Sector: "+tickers.tickers[ticker_symbol].info['sector'])
        
    with tab2:
        st.markdown("## Company's summary: ")
        st.markdown("### Due to API issues this page is not available at the moment")
        # st.markdown("- "+tickers.tickers[ticker_symbol].info['longBusinessSummary'])
    
    with tab3:
        st.markdown("## Historical Data timeline: ")
        st.markdown(str(dates))
        earliest_date = dates[0]
        latest_date = dates[1]

        #get ticker data by creating a ticker object
        tickerDF = yf.download(ticker_symbol, 
        start=''+str(earliest_date.year)+'-'+str(earliest_date.month)+'-'+str(earliest_date.day), 
        end=''+str(latest_date.year)+'-'+str(latest_date.month)+'-'+str(latest_date.day))

        #columns: Open, High, Low, Close, Adj Close and Volume
        st.dataframe(tickerDF)

# get financial currency
# financialCurrency =  tickers.tickers[ticker_symbol].info['financialCurrency']

# close price tabs and plots
with st.container():

    st.write("## Stock's Closing Price plots 💸")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Time Series", "Candlestick plot", 
    "Annual evolution", "Histogram", "Violin plot"])
       
    with tab1:
        # st.write("### Stock Closing Price in " + financialCurrency)
        st.write("### Stock Closing Price")
        st.line_chart(tickerDF.Close)
        
    with tab2:
        # candlestick plot
        # st.write("### Stock Closing Price candlestick plot in "+ financialCurrency)
        st.write("### Stock Closing Price candlestick plot in ")
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=tickerDF.index, 
        open=tickerDF['Open'], 
        high=tickerDF['High'], 
        low=tickerDF['Low'], 
        close=tickerDF['Close']) )

        st.plotly_chart(fig)

    with tab3:
        # price over years
        mean_closing_price_per_year = tickerDF.groupby(tickerDF.index.year)['Close'].mean()

        # Plot the result
        # st.write("### Mean closing price over the years in "+ financialCurrency)
        st.write("### Mean closing price over the years")
        st.bar_chart(mean_closing_price_per_year)
        
    with tab4:
        # price histogram
        # st.write("### Closing price histogram in "+ financialCurrency)
        st.write("### Closing price histogram")
        fig = ex.histogram(tickerDF, x="Close", nbins=20)
        st.plotly_chart(fig, use_container_width=True)
        
    with tab5:
        # closing price violinplot
        fig = ex.violin(tickerDF, y="Close", box=True, # draw box plot inside the violin
                points='all', # can be 'outliers', or False
               )
        st.plotly_chart(fig, use_container_width=True)



# linechart for all features
with st.container():
    st.markdown("## Stock price movements 📊")
    
    tab1, tab2 = st.tabs(["Scatterplots", "Violinplots"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
           # st.write("#### Stock's Open price in "+ financialCurrency)
           st.write("#### Stock's Open price")
           st.line_chart(tickerDF["Open"])

        with col2:
           # st.write("#### Stock's High price in "+ financialCurrency)
           st.write("#### Stock's High price")
           st.line_chart(tickerDF["High"])

        with col3:
           # st.write("#### Stock's Low price in "+ financialCurrency)
           st.write("#### Stock's Low price")
           st.line_chart(tickerDF["Low"])
           

        col1, col2, col3 = st.columns(3)
        with col1:
           # st.write("#### Stock's Close price in "+ financialCurrency)
           st.write("#### Stock's Close price")
           st.line_chart(tickerDF["Close"])

        with col2:
           # st.write("#### Stock's Adj Close price in "+ financialCurrency)
           st.write("#### Stock's Adj Close price")
           st.line_chart(tickerDF["Adj Close"])

        with col3:
           st.write("#### Stock's Volume over time")
           st.line_chart(tickerDF["Volume"])
    
    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            fig = ex.violin(tickerDF, y="Open", box=True, # draw box plot inside the violin
                    points='all', # can be 'outliers', or False
                   )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = ex.violin(tickerDF, y="High", box=True, # draw box plot inside the violin
                    points='all', # can be 'outliers', or False
                   )
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            fig = ex.violin(tickerDF, y="Low", box=True, # draw box plot inside the violin
                    points='all', # can be 'outliers', or False
                   )
            st.plotly_chart(fig, use_container_width=True)
           

        col1, col2, col3 = st.columns(3)
        with col1:
            fig = ex.violin(tickerDF, y="Close", box=True, # draw box plot inside the violin
                    points='all', # can be 'outliers', or False
                   )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = ex.violin(tickerDF, y="Adj Close", box=True, # draw box plot inside the violin
                    points='all', # can be 'outliers', or False
                   )
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            fig = ex.violin(tickerDF, y="Volume", box=True, # draw box plot inside the violin
                    points='all', # can be 'outliers', or False
                   )
            st.plotly_chart(fig, use_container_width=True)
   
   
# Create a correlation plot
# https://stackoverflow.com/questions/72195177/correlation-matrix-in-plotly
with st.container():
    st.write("## Bivariate analysis 📉")
    
    tab1, tab2, tab3 = st.tabs(["Scatterplots", "kdeplots", "Correlation Coefficient"])
    
    with tab1:
        st.markdown("#### Stock price movements Scatterplots")
        fig = ex.scatter_matrix(tickerDF)
        fig.update_layout(height=600, width=850)

        st.plotly_chart(fig)
        
    with tab2:
        st.markdown("#### Stock price movements Kdeplots")
        
        options = st.multiselect('Choose 2 features', ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'],
        default=["Open", "Close"], max_selections=2)
        
        fig = ex.density_contour(tickerDF, x=options[0], y=options[1], marginal_x="histogram", marginal_y="histogram")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:

        st.write("#### Correlations between stock's movements")
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