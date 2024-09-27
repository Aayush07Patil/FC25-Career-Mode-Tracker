import streamlit as st
import pandas as pd

# Load the CSV file
csv_file_path = "data/senior_squad_player_data.csv"  # Update with the path to your CSV file
data = pd.read_csv(csv_file_path)

# Streamlit UI to display the DataFrame
st.title("Senior Squad")

# Display the DataFrame
st.dataframe(data)