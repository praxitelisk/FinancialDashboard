import streamlit as st
import pandas as pd


st.set_page_config(page_title="Stock News", page_icon="📰")

# Title
st.title("Credits Page")

# Description
st.write("This project was made possible thanks to the following libraries and tools:")

# Data for the table
# Data for the table
# Markdown table format
table = """
| Library/Tool  | Description                                       | Website                                                   |
|---------------|---------------------------------------------------|-----------------------------------------------------------|
| Streamlit     | A web app framework for Python.                   | [Streamlit](https://streamlit.io/)                        |
| Python        | A powerful programming language.                  | [Python](https://www.python.org/)                          |
| Scikit-Learn  | A machine learning library.                       | [Scikit-Learn](https://scikit-learn.org/)                  |
| YFinance      | A library for accessing financial data.           | [YFinance](https://pypi.org/project/yfinance/)             |
| Pandas        | A data manipulation and analysis library.         | [Pandas](https://pandas.pydata.org/)                       |
| News-API      | A service for fetching news data.                 | [News-API](https://newsapi.org/)                           |
"""

# Display the table as Markdown
st.markdown(table)

# Additional text
st.write("We are grateful for the developers and maintainers of these amazing libraries and tools.")
