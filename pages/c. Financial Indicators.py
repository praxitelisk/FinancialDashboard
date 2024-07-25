import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Financial Indicators", page_icon="🧮")

if "ticker_symbol" not in st.session_state:
    st.session_state.ticker_symbol = 'AAPL'

ticker_symbol = st.sidebar.text_input('Type here the stock name IN CAPITAL LETTERS you need for analysis. E.g. AAPL, MSFT, TSLA, AMZN, NVDA', st.session_state.ticker_symbol)
st.session_state.ticker_symbol = ticker_symbol

st.sidebar.write("In case you need to search for stocks' names")
st.sidebar.link_button("Search stock names in Yahoo finance site", "https://finance.yahoo.com")

# Fetch stock data
def get_stock_data(ticker):
    stock_data = yf.download(ticker, start="2020-01-01")
    return stock_data

# Calculate financial indicators
def calculate_indicators(data, indicators):
    results = pd.DataFrame(index=data.index)
    if 'Moving Average' in indicators:
        results['Moving Average'] = data['Close'].rolling(window=20).mean()
    if 'Exponential Moving Average' in indicators:
        results['Exponential Moving Average'] = data['Close'].ewm(span=20, adjust=False).mean()
    if 'RSI' in indicators:
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        results['RSI'] = 100 - (100 / (1 + rs))
    if 'MACD' in indicators:
        ema12 = data['Close'].ewm(span=12, adjust=False).mean()
        ema26 = data['Close'].ewm(span=26, adjust=False).mean()
        results['MACD'] = ema12 - ema26
        results['MACD Signal'] = results['MACD'].ewm(span=9, adjust=False).mean()
    if 'ATR' in indicators:
        high_low = data['High'] - data['Low']
        high_close = (data['High'] - data['Close'].shift()).abs()
        low_close = (data['Low'] - data['Close'].shift()).abs()
        tr = high_low.combine(high_close, max).combine(low_close, max)
        results['ATR'] = tr.rolling(window=14).mean()
    return results

st.markdown("# Stock Closing Price and Financial Indicators 💹")
st.sidebar.header("Financial Indicators")

# Define list of available indicators
available_indicators = ['Moving Average', 'Exponential Moving Average', 'RSI', 'MACD', 'ATR']
selected_indicators = st.sidebar.multiselect('Select Indicators', available_indicators)

# Display the stock data
st.write(f"Displaying the flactuations of closing price for {ticker_symbol} stock")

try:
    stock_data = get_stock_data(ticker_symbol)
    
    # Plot closing price and selected indicators
    chart_data = pd.DataFrame({'Close': stock_data['Close']})
    
    if selected_indicators:
        st.markdown("## Financial Indicators")
        indicators = calculate_indicators(stock_data, selected_indicators)
        chart_data = pd.concat([chart_data, indicators], axis=1)
    
    st.line_chart(chart_data)

    if 'Moving Average' in selected_indicators:
        st.markdown("## Moving Average")
        st.write("The Moving Average is a statistical calculation used to analyze data points by creating a series of averages of different subsets of the full data set. It helps smooth out price data to identify trends and patterns by filtering out the \"noise\" from random price fluctuations. Traders use MAs to identify the direction of the trend and determine support and resistance levels. It's a lagging indicator that helps to confirm trends rather than predict them.")
        st.line_chart(indicators['Moving Average'])


    if 'Exponential Moving Average' in selected_indicators:
        st.markdown("## Exponential Moving Average")
        st.write("The Exponential Moving Average is a type of moving average that gives more weight to the most recent data points, making it more responsive to new information than the simple moving average. Like the MA, the EMA is used to identify trends and potential buy or sell signals. Due to its sensitivity to recent price movements, it's particularly useful in fast-moving markets.")
        st.line_chart(indicators['Exponential Moving Average'])


    if 'MACD' in selected_indicators:
        st.markdown("## Moving Average Convergence Divergence")
        st.write(" The MACD is a trend-following momentum indicator that shows the relationship between two moving averages of an asset’s price. Traders use the MACD to identify changes in the strength, direction, momentum, and duration of a trend. A common signal is when the MACD line crosses above the signal line (bullish signal) or below it (bearish signal).")
        st.line_chart(indicators['MACD'])
    
    if 'RSI' in selected_indicators:
        st.markdown("## RSI (Relative Strength Index)")
        st.write("The Relative Strength Index is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100. RSI values above 70 generally indicate that an asset is overbought, while values below 30 suggest it is oversold. Traders use these signals to identify potential reversal points.")
        st.line_chart(indicators['RSI'])
    
    if 'ATR' in selected_indicators:
        st.markdown("## ATR (Average True Range)")
        st.write("The Average True Range is a volatility indicator that measures the degree of price movement for an asset. ATR provides insight into how much an asset typically moves over a given period, helping traders set stop-loss orders and determine the volatility of the market. Higher ATR values indicate more significant volatility, while lower values suggest lower volatility.")
        st.line_chart(indicators['ATR'])
        
except Exception as e:
    st.error(f"Error fetching data for {ticker_symbol}. Please check the ticker symbol and try again.")
