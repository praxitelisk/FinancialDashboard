# financial indicators

import os
import streamlit as st
import pandas as pd
import tempfile

st.set_page_config(page_title="Financial Indicators", page_icon="🧮")

st.markdown("# Stock Closing Price and Financial Indicators")
st.sidebar.header("Financial Indicators")
st.write(
    """To Be Updated"""
)

def create_temp_file():
    temp_dir = tempfile.gettempdir()
    temp_file_path = temp_dir + '/my_temp_file.txt'

    # Check if the file already exists
    if not os.path.exists(temp_file_path):
        # Create the temporary file
        with open(temp_file_path, 'w') as file:
            file.write("This is my temporary file content")

    return temp_file_path

temp_file_path = create_temp_file()
st.success(f"Temporary file created at {temp_file_path}")

# Display the contents of the temporary file (if it exists)
if 'temp_file_path' in locals():
    with open(temp_file_path, 'r') as file:
        file_content = file.read()
    st.subheader("Temporary File Content:")
    st.text(file_content)