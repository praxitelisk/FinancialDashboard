import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title and description
st.title("Iris Dataset Analysis")
st.write("This app performs descriptive analysis and visualization on the Iris dataset.")

# Load the Iris dataset
@st.cache  # Use caching to load the data only once
def load_data():
    data = sns.load_dataset("iris")
    return data

data = load_data()

# Display raw data
st.subheader("Raw Data")
st.write(data)

# Descriptive statistics
st.subheader("Descriptive Statistics")
st.write(data.describe())

# Sidebar options
selected_feature = st.sidebar.selectbox("Select a feature", data.columns[:-1])
selected_species = st.sidebar.multiselect("Select species", data["species"].unique())

# Filtering based on sidebar inputs
filtered_data = data[data["species"].isin(selected_species)]

# Display scatter plot
st.subheader("Scatter Plot")
plt.figure(figsize=(8, 6))
sns.scatterplot(x=selected_feature, y="sepal_width", hue="species", data=filtered_data)
plt.xlabel(selected_feature)
plt.ylabel("Sepal Width")
plt.title(f"{selected_feature} vs Sepal Width")
st.pyplot()

# Display box plot
st.subheader("Box Plot")
plt.figure(figsize=(8, 6))
sns.boxplot(x="species", y=selected_feature, data=filtered_data)
plt.xlabel("Species")
plt.ylabel(selected_feature)
plt.title(f"{selected_feature} by Species")
st.pyplot()

# Display pair plot
st.subheader("Pair Plot")
sns.pairplot(data=filtered_data, hue="species")
st.pyplot()
