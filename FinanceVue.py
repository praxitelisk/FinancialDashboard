import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="FinanceVue",
    page_icon="🏛️",
)

if "ticker_symbol" not in st.session_state:
    # set the initial default value of the slider widget
    st.session_state.ticker_symbol = 'AAPL'

st.write("# Welcome to FinanceVue! 🗠")

st.markdown("FinanceVue is a financial stock dashboard that provides a comprehensive overview of key financial and market data related to stocks and securities. It is designed to help investors, traders, and financial professionals monitor and analyze stock market performance, make informed decisions, and track their investments. A stock dashboard typically includes various financial and market indicators, charts, and data presented in a user-friendly format.")

st.markdown("### Created and designed by [Praxitelis-Nikolaos Kouroupetroglou](https://praxitelisk.github.io/)")
st.markdown("#### Supervised by: Prof. [Alkiviadis Tsimpiris](http://teachers.cm.ihu.gr/tsimpiris/index.php/en/)")

st.markdown("## [International Helenic University](https://www.ihu.gr/ucips/)")
image = Image.open('images/IHU_logo.png')
st.image(image)

st.markdown("## [Department of Computer, Informatics and Telecommunications Engineering](https://ict.ihu.gr/en/home)")
image = Image.open('images/dept.jpg')
st.image(image)

st.markdown("## [Master In Applied Informatics](https://ict.ihu.gr/en/home)")
image = Image.open('images/dark-blue.jpg')
st.image(image)


st.write("## What is streamLit?")
st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)