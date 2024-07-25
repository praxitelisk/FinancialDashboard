import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Financial Indicators", page_icon="🧮")

if "ticker_symbol" not in st.session_state:
    st.session_state.ticker_symbol = 'AAPL'

ticker_symbol = st.sidebar.text_input('Type here the stock name IN CAPITAL LETTERS you need for analysis', st.session_state.ticker_symbol)
st.session_state.ticker_symbol = ticker_symbol

st.sidebar.write("In case you need to search for stocks' names")
st.sidebar.link_button("Search stock names in Yahoo finance site", "https://finance.yahoo.com")

# Fetch stock data
def get_stock_data(ticker):
    stock_data = yf.Tickers(ticker)
    return stock_data

st.markdown("# Fundamental Analysis of Stock")

# Display the stock data
st.write(f"Displaying fundamental analysis for {ticker_symbol}")

try:
    ticker = get_stock_data(ticker_symbol)
    #financial_metrics = calculate_fundamental_indicators(stock_data)
    
    # print balance sheet
    st.markdown("### Balance Sheet")
    st.write("The balance sheet displays the company's total assets and how the assets are financed, either through either debt or equity.")
    st.write(ticker.tickers[ticker_symbol].balance_sheet)

    # print financials
    st.markdown("### Financials")
    st.write("The balance sheet provides an overview of assets, liabilities, and shareholders' equity as a snapshot in time.")
    st.write(ticker.tickers[ticker_symbol].financials)

    # print cashflow
    st.markdown("### Cashflow")
    st.write("The cash flow statement (CFS) shows how cash flows throughout a company.")
    st.write(ticker.tickers[ticker_symbol].cashflow)

    ## Profitability Ratios: ##
    # Earnings Per Share (EPS)
    earnings_per_share = ticker.tickers[ticker_symbol].info['trailingEps']
    st.markdown("### Earnings Per Share (EPS)")
    st.write("Measures the portion of a company's profit allocated to each outstanding share of common stock.", earnings_per_share) 

    # Price-to-Earnings (P/E) Ratio
    pe_ratio = ticker.tickers[ticker_symbol].info['trailingPE']
    st.markdown("### Price-to-Earnings (P/E) Ratio")
    st.write("Measures a company's current share price relative to its per-share earnings.", pe_ratio) 
    
    # Return on Equity (ROE)
    net_income = ticker.tickers[ticker_symbol].financials.loc['Net Income'][0]
    total_equity = ticker.tickers[ticker_symbol].balance_sheet.loc['Stockholders Equity'][0]
    roe = net_income / total_equity
    st.markdown("### Return on Equity (ROE)")
    st.write("Measures the profitability of a company in generating profit from its shareholders' equity.", roe) 


    # Return on Assets (ROA)
    net_income = ticker.tickers[ticker_symbol].financials.loc['Net Income'][0]
    total_assets = ticker.tickers[ticker_symbol].balance_sheet.loc['Total Assets'][0]
    roa = net_income / total_assets
    st.markdown("### Return on Assets (ROA)")
    st.write("Indicates how profitable a company is relative to its total assets.", roa) 

    # Gross Profit Margin
    revenue = ticker.tickers[ticker_symbol].financials.loc['Total Revenue'][0]
    cogs = ticker.tickers[ticker_symbol].financials.loc['Cost Of Revenue'][0]
    gross_profit = revenue - cogs
    gross_profit_margin = (gross_profit / revenue) * 100

    st.markdown("### Gross Profit Margin")
    st.write("Shows the percentage of revenue that exceeds the cost of goods sold (COGS)", gross_profit_margin) 


    # Operating Margin
    revenue = ticker.tickers[ticker_symbol].financials.loc['Total Revenue'][0]
    operating_income = ticker.tickers[ticker_symbol].financials.loc['Operating Income'][0]
    operating_margin = (operating_income / revenue) * 100

    st.markdown("### Operating Margin")
    st.write("Measures the percentage of revenue left after paying for variable costs of production.", operating_margin) 


    ## Liquidity Ratios: ##
    # Current Ratio
    total_liabilities = ticker.tickers[ticker_symbol].balance_sheet.loc['Total Liabilities Net Minority Interest'][0]
    debt_to_equity_ratio = total_liabilities / total_equity

    st.markdown("### Liquidity Ratios")
    st.write("Measures a company's financial leverage by comparing its total liabilities to shareholders' equity.", debt_to_equity_ratio) 


    # Quick Ratio (Acid-Test Ratio)
    ebit = ticker.tickers[ticker_symbol].financials.loc['EBIT'][0]
    interest_expense = ticker.tickers[ticker_symbol].financials.loc['Interest Expense'][0]
    interest_coverage_ratio = ebit / interest_expense
    
    st.markdown("### Quick Ratio (Acid-Test Ratio)")
    st.write("Indicates how easily a company can pay interest on its outstanding debt.", interest_coverage_ratio) 

    ## Leverage Ratios: ##
    # Debt-to-Equity Ratio
    total_liabilities = ticker.tickers[ticker_symbol].balance_sheet.loc['Total Liabilities Net Minority Interest'][0]
    debt_to_equity_ratio = total_liabilities / total_equity

    st.markdown("### Leverage Ratios")
    st.write("Debt-to-Equity Ratio for.", debt_to_equity_ratio) 

    # Interest Coverage Ratio
    interest_expense = ticker.tickers[ticker_symbol].financials.loc['Interest Expense'].iloc[0]
    interest_coverage_ratio = ebit / interest_expense

    st.markdown("### Interest Coverage Ratio")
    st.write("Indicates how easily a company can pay interest on its outstanding debt.", interest_coverage_ratio) 

    ### Efficiency Ratios:
    # Asset Turnover Ratio
    total_revenue = ticker.tickers[ticker_symbol].financials.loc['Total Revenue'][0]
        
    total_assets_begin = ticker.tickers[ticker_symbol].balance_sheet.loc['Total Assets'][1]  # Previous period total assets
    total_assets_end = ticker.tickers[ticker_symbol].balance_sheet.loc['Total Assets'][0]    # Current period total assets
    average_total_assets = (total_assets_begin + total_assets_end) / 2
        
    asset_turnover_ratio = total_revenue / average_total_assets

    st.markdown("### Asset Turnover Ratio")
    st.write("Measures the efficiency of a company's use of its assets in generating sales revenue.", asset_turnover_ratio) 


    # Inventory Turnover Ratio
    cogs = ticker.tickers[ticker_symbol].financials.loc['Cost Of Revenue'].iloc[0]  # Cost of Goods Sold (COGS)

    inventory_current = ticker.tickers[ticker_symbol].balance_sheet.loc['Inventory'].iloc[0]
    inventory_previous = ticker.tickers[ticker_symbol].balance_sheet.loc['Inventory'].iloc[1]
    average_inventory = (inventory_current + inventory_previous) / 2

    inventory_turnover_ratio = cogs / average_inventory
    st.markdown("### Inventory Turnover Ratio")
    st.write("Shows how many times a company's inventory is sold and replaced over a period.", inventory_turnover_ratio) 


    ### Valuation Ratios
    ## Price-to-Book (P/B) Ratio
    # Get the current stock price
    stock_price = ticker.tickers[ticker_symbol].history(period='1d')['Close'][0]

    # Get the number of shares outstanding
    shares_outstanding = ticker.tickers[ticker_symbol].info['sharesOutstanding']

    # Calculate Book Value per Share
    book_value_per_share = total_equity / shares_outstanding

    # Calculate P/B Ratio
    pb_ratio = stock_price / book_value_per_share

    st.markdown("### Price-to-Book (P/B) Ratio")
    st.write("Compares a company's market value to its book value.", pb_ratio) 

    # Dividend Yield
    # Get the annual dividend per share
    dividend_yield = ticker.tickers[ticker_symbol].info['dividendYield']

    # Calculate annual dividend per share
    annual_dividend_per_share = dividend_yield * stock_price

    # Calculate Dividend Yield
    dividend_yield_percentage = (annual_dividend_per_share / stock_price) * 100

    st.markdown("### Dividend")
    st.write("Shows % how much a company pays out in dividends each year relative to its share price.", dividend_yield_percentage) 

    ## Growth Ratios
    # Revenue Growth Rate
    revenue_current = ticker.tickers[ticker_symbol].financials.loc['Total Revenue'].iloc[0]  # Most recent period
    revenue_previous = ticker.tickers[ticker_symbol].financials.loc['Total Revenue'].iloc[1]  # Previous period

    # Calculate Revenue Growth Rate
    revenue_growth_rate = ((revenue_current - revenue_previous) / revenue_previous) * 100

    st.markdown("### Revenue Growth Rate")
    st.write("Measures the annual growth rate of revenue from the prior year.", revenue_growth_rate) 


    # Earnings Growth Rate
    # Extract the net income (earnings) for the most recent two periods
    earnings_current = ticker.tickers[ticker_symbol].financials.loc['Net Income'].iloc[0]  # Most recent period
    earnings_previous = ticker.tickers[ticker_symbol].financials.loc['Net Income'].iloc[1]  # Previous period

    # Calculate Earnings Growth Rate
    earnings_growth_rate = ((earnings_current - earnings_previous) / earnings_previous) * 100

    st.markdown("### Earnings Growth Rate")
    st.write("Measures the annual growth rate of revenue from the prior year.", revenue_growth_rate) 


    ## Cash Flow Ratios
    # Free Cash Flow (FCF)
    cash_flow_from_operations = ticker.tickers[ticker_symbol].cashflow.loc['Operating Cash Flow'].iloc[0]  # Most recent period
    capital_expenditures = ticker.tickers[ticker_symbol].cashflow.loc['Capital Expenditure'].iloc[0]  # Most recent period

    # Calculate Free Cash Flow
    free_cash_flow = cash_flow_from_operations - capital_expenditures

    st.markdown("### Free Cash Flow (FCF)")
    st.write("Indicates the cash a company generates after accounting for cash outflows to support operations and maintain capital assets.", free_cash_flow) 

    # Operating Cash Flow Ratio
    operating_cash_flow_ratio = cash_flow_from_operations / total_liabilities

    st.markdown("### Operating Cash Flow Ratio")
    st.write("Measures how well current liabilities are covered by the cash flow generated from a company's operations.", operating_cash_flow_ratio) 



except Exception as e:
    st.error(f"Error fetching data for {ticker_symbol}. Please check the ticker symbol and try again.")