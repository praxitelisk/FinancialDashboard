import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Stock Price Forecasting", page_icon="🤖")


if "ticker_symbol" not in st.session_state:
    # set the initial default value of the slider widget
    st.session_state.ticker_symbol = 'AAPL'

### sidebar
st.sidebar.header("Stock Data Forecasting")

st.sidebar.write("Type the stock name:")
ticker_symbol = st.sidebar.text_input('Type here the stock name IN CAPITAL LETTERS you need for analysis', st.session_state.ticker_symbol)
st.session_state.ticker_symbol = ticker_symbol

tickers = yf.Tickers(ticker_symbol)
# equity_name =  tickers.tickers[ticker_symbol].info['shortName']

st.sidebar.write("In case you need to search for stocks' names")
st.sidebar.link_button("Search stock names in Yahoo finance site", "https://finance.yahoo.com")

# set dates
today = datetime.now()
#earliest_year = today.year - 5

# Define a timedelta of 10 days
ten_days = timedelta(days=10)

# Calculate the date 10 days from today
past_date = today - ten_days

#earliest_date = datetime.date(earliest_year, 1, 1)

# dates = st.sidebar.write(
#     "Select time period of historical data",
#     (past_date, today),
#     past_date,
#     today,
#     format="YYYY.MM.DD",
# )

st.sidebar.write("last 10 days of closing price")

st.sidebar.write(str(past_date.year) +"/"+ str(past_date.month) +"/"+ str(past_date.day), " - " , 
                 str(today.year) +"/"+ str(today.month) +"/"+ str(today.day))

# days_for_forecasting
days_for_forecasting = st.sidebar.slider('Select the days for forecasting', 1, 10, 1)

### main window
st.markdown("# Stock Data Forecasting")
st.write(
    """Stock Forecasting is a tool to predict future stock price based on past historical data"""
)

#get ticker data by creating a ticker object
end = datetime.now()
start = datetime(end.year - 9, end.month, end.day)
main_df = yf.download(ticker_symbol, start, end)

st.dataframe(main_df.sort_index(ascending=False))

# prepare the targets
main_df['Open_target'] = main_df['Open'].shift(-1)
main_df['High_target'] = main_df['High'].shift(-1)
main_df['Low_target'] = main_df['Low'].shift(-1)
main_df['Close_target'] = main_df['Close'].shift(-1)
main_df['Adj Close_target'] = main_df['Adj Close'].shift(-1)
main_df['Volume_target'] = main_df['Volume'].shift(-1)

# select model for forecasting
option = st.selectbox(
    'Which model should make the forecasts?',
    ('Random Forest', 'XGBoost'),
    index=None,
    placeholder="Select model to create forecasts",)

st.write('You selected:', option)

# Random Forest forecasting
def simulate_randon_forest_forecasting(main_df, days_for_forecasting):
        
    for i in range(days_for_forecasting):        
        
        # for each day for forecasting predict the open, high, low, volume using linear regression
        new_date = main_df.index[-1]

        # Increment the timestamp by 1 day
        new_date = new_date + timedelta(days=1)

        # if the new date is on Saturday or Sunday the stock market is closed. So increment the new date until
        if new_date.weekday() in [5,6]:
            while new_date.weekday() in [5,6]:
                new_date = new_date + timedelta(days=1)

        ### Open
        #Predict the latest next day Open price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Open_target'][:-1]
        
        # build random forest model to predict the next open value
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        open_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))

        

        ### High
        #Predict the latest next day High price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['High_target'][:-1]
        
        # build random forest model to predict the next high value
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        high_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        ### Low
        #Predict the latest next day Open price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Low_target'][:-1]
        
        # build random forest model to predict the next Low price
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        low_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        ### Volume
        #Predict the latest next day Volume with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Volume_target'][:-1]
        
        # build random forest model to predict the next 
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        volume_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))

        
        ### Close
        #Predict the latest next day Close price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Close_target'][:-1]
        
        # build random forest model to predict the next 
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        close_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        ### Adj Close
        #Predict the next day Adj Close price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Adj Close_target'][:-1]
        
        # build random forest model to predict the next 
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        adj_close_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        # save the new predictions to targets
        main_df['Open_target'].iloc[-1] = open_pred[0]
        main_df['High_target'].iloc[-1] = high_pred[0]
        main_df['Low_target'].iloc[-1] = low_pred[0]
        main_df['Close_target'].iloc[-1] = close_pred[0]
        main_df['Adj Close_target'].iloc[-1] = adj_close_pred[0]
        main_df['Volume_target'].iloc[-1] = np.round(volume_pred[0])
        
        
        # Append the next case/forecast to dataframe
        new_case = [main_df['Open_target'][-1], 
                main_df['High_target'][-1], 
                main_df['Low_target'][-1], 
                main_df['Close_target'][-1], 
                main_df['Adj Close_target'][-1], 
                main_df['Volume_target'][-1],
               np.NaN,
               np.NaN,
               np.NaN,
               np.NaN,
               np.NaN,
               np.NaN]

        main_df.loc[new_date] = new_case
                
    return main_df


def simulate_xgboost_forecasting(main_df, days_for_forecasting):
        
    for i in range(days_for_forecasting):        
        
        # for each day for forecasting predict the open, high, low, volume using linear regression
        new_date = main_df.index[-1]

        # Increment the timestamp by 1 day
        new_date = new_date + timedelta(days=1)

        # if the new date is on Saturday or Sunday the stock market is closed. So increment the new date until
        if new_date.weekday() in [5,6]:
            while new_date.weekday() in [5,6]:
                new_date = new_date + timedelta(days=1)
        
        
        train_features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

        ### Open
        #Predict the latest next day Open price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Open_target'][:-1]
        
        # build random forest model to predict the next open value
        model = xgb.XGBRegressor(n_estimators=100, seed=42)
        model.fit(X_train, y_train)
        open_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))

        

        ### High
        #Predict the latest next day High price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['High_target'][:-1]
        
        # build random forest model to predict the next high value
        model = xgb.XGBRegressor(n_estimators=100, seed=42)
        model.fit(X_train, y_train)
        high_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        ### Low
        #Predict the latest next day Open price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Low_target'][:-1]
        
        # build random forest model to predict the next Low price
        model = xgb.XGBRegressor(n_estimators=100, seed=42)
        model.fit(X_train, y_train)
        low_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        ### Volume
        #Predict the latest next day Volume with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Volume_target'][:-1]
        
        # build random forest model to predict the next 
        model = xgb.XGBRegressor(n_estimators=100, seed=42)
        model.fit(X_train, y_train)
        volume_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))

        
        ### Close
        #Predict the latest next day Close price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Close_target'][:-1]
        
        # build random forest model to predict the next 
        model = xgb.XGBRegressor(n_estimators=100, seed=42)
        model.fit(X_train, y_train)
        close_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        ### Adj Close
        #Predict the next day Adj Close price with baseline random forest model
        X_train = main_df.drop(['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False)[:-1]
        
        y_train = main_df['Adj Close_target'][:-1]
        
        # build random forest model to predict the next 
        model = xgb.XGBRegressor(n_estimators=100, seed=42)
        model.fit(X_train, y_train)
        adj_close_pred = model.predict(main_df.drop(
            ['Open_target', 'High_target', 'Low_target', 'Close_target', 'Adj Close_target', 'Volume_target'], 
                               axis=1, inplace=False).tail(1))
        
        
        # save the new predictions to targets
        main_df['Open_target'].iloc[-1] = open_pred[0]
        main_df['High_target'].iloc[-1] = high_pred[0]
        main_df['Low_target'].iloc[-1] = low_pred[0]
        main_df['Close_target'].iloc[-1] = close_pred[0]
        main_df['Adj Close_target'].iloc[-1] = adj_close_pred[0]
        main_df['Volume_target'].iloc[-1] = np.round(volume_pred[0])
        
        
        # Append the next case/forecast to dataframe
        new_case = [main_df['Open_target'][-1], 
                main_df['High_target'][-1], 
                main_df['Low_target'][-1], 
                main_df['Close_target'][-1], 
                main_df['Adj Close_target'][-1], 
                main_df['Volume_target'][-1],
               np.NaN,
               np.NaN,
               np.NaN,
               np.NaN,
               np.NaN,
               np.NaN]

        main_df.loc[new_date] = new_case
                
    return main_df


forecasted_df = pd.DataFrame()
if option is None:
    st.markdown("Select a model to produce forecasts")

elif option == 'Random Forest':
    forecasted_df = simulate_randon_forest_forecasting(main_df.copy(), days_for_forecasting)

    forecasted_df.tail(days_for_forecasting)

    # print forecasts
    st.markdown("### Forecasts made by: "+option)
    st.dataframe(forecasted_df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].tail(days_for_forecasting))


    # Visualise Forecasts
    st.markdown("### Visualise Forecasts")

    # Create a figure
    fig, ax = plt.subplots()

    # Plot the forecasts with a scatterplot
    ax.scatter(forecasted_df.index[-days_for_forecasting:], forecasted_df['Close'].tail(days_for_forecasting), s=10, marker='o', color='blue', alpha=0.65)
    ax.plot(forecasted_df.index[-days_for_forecasting:], forecasted_df['Close'].tail(days_for_forecasting), color='blue', linewidth=2, alpha=0.65)


    # Plot the historical data with a lineplot
    historical_data_plot_interval = 10
    ax.scatter(forecasted_df.index[len(main_df)-historical_data_plot_interval:len(main_df)], forecasted_df['Close'][len(main_df)-historical_data_plot_interval:len(main_df)], s=10, marker='x', color='red', alpha=0.5)
    ax.plot(forecasted_df.index[len(main_df)-historical_data_plot_interval:len(main_df)], forecasted_df['Close'][len(main_df)-historical_data_plot_interval:len(main_df)], color='red', linewidth=2, alpha=0.5)

    # Rotating X-axis labels
    plt.xticks(rotation = 75)

    # Set the axis labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.set_title('Scatterplot and Lineplot of {}'.format('Close price'))
    st.pyplot(fig)


elif option == 'XGBoost':
    forecasted_df = simulate_randon_forest_forecasting(main_df.copy(), days_for_forecasting)

    forecasted_df.tail(days_for_forecasting)

    # print forecasts
    st.markdown("### Forecasts made by: "+option)
    st.dataframe(forecasted_df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].tail(days_for_forecasting))


    # Visualise Forecasts
    st.markdown("### Visualise Forecasts")

    # Create a figure
    fig, ax = plt.subplots()

    # Plot the forecasts with a scatterplot
    ax.scatter(forecasted_df.index[-days_for_forecasting:], forecasted_df['Close'].tail(days_for_forecasting), s=10, marker='o', color='blue', alpha=0.65)
    ax.plot(forecasted_df.index[-days_for_forecasting:], forecasted_df['Close'].tail(days_for_forecasting), color='blue', linewidth=2, alpha=0.65)


    # Plot the historical data with a lineplot
    historical_data_plot_interval = 10
    ax.scatter(forecasted_df.index[len(main_df)-historical_data_plot_interval:len(main_df)], forecasted_df['Close'][len(main_df)-historical_data_plot_interval:len(main_df)], s=10, marker='x', color='red', alpha=0.5)
    ax.plot(forecasted_df.index[len(main_df)-historical_data_plot_interval:len(main_df)], forecasted_df['Close'][len(main_df)-historical_data_plot_interval:len(main_df)], color='red', linewidth=2, alpha=0.5)

    # Rotating X-axis labels
    plt.xticks(rotation = 75)

    # Set the axis labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.set_title('Scatterplot and Lineplot of {}'.format('Close price'))
    st.pyplot(fig)
    
else:
    st.markdown("#### more models will be updated soon")


