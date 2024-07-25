import streamlit as st
import pandas as pd


st.set_page_config(page_title="Stock News", page_icon="📰")

# Title
st.title("Credits Page")

# Description
st.write("This project was made possible thanks to the following libraries and tools:")

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
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the table
st.table(df)

# Additional text
st.write("We are grateful for the developers and maintainers of these amazing libraries and tools.")
