import streamlit as st
import pandas as pd
import tabulate


st.set_page_config(page_title="Stock News", page_icon="📰")

# Title
st.title("Credits Page")

# Description
st.write("This project was made possible thanks to the following libraries and tools:")

# Data for the table
# Data for the table
data = {
    "Library/Tool": ["Streamlit", "Python", "Scikit-Learn", "YFinance", "Pandas", "News-API"],
    "Description": [
        "A web app framework for Python.",
        "A powerful programming language.",
        "A machine learning library.",
        "A library for accessing financial data.",
        "A data manipulation and analysis library.",
        "A service for fetching news data."
    ],
    "Website": [
        "[Streamlit](https://streamlit.io/)",
        "[Python](https://www.python.org/)",
        "[Scikit-Learn](https://scikit-learn.org/)",
        "[YFinance](https://pypi.org/project/yfinance/)",
        "[Pandas](https://pandas.pydata.org/)",
        "[News-API](https://newsapi.org/)"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Display the table as Markdown
st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

# Additional text
st.write("We are grateful for the developers and maintainers of these amazing libraries and tools.")
