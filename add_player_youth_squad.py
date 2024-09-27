import streamlit as st
from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
DB_NAME = "FC25_Chelsea_CM_tracker"  # Name of your database
COLLECTION_NAME = "youth_squad_players_season_1"  # Name of your collection

# Create a MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_data_to_mongodb(data):
    # Insert the data into MongoDB
    collection.insert_one(data)

def main():
    # Streamlit UI for inputs
    st.title('Add Youth Squad Players')

    col1, col2 = st.columns(2, gap='small')
    first_name = col1.text_input('First Name') or ""
    last_name = col1.text_input('Last Name') or ""
    nation = col1.text_input('Nation') or ""
    age = col1.number_input('Age', min_value=0, max_value=100, step=1)
    height = col1.number_input('Height (cm)', min_value=100, max_value=250, step=1)
    weight = col1.number_input('Weight (kg)', min_value=30, max_value=200, step=1)
    preferred_foot = col1.text_input('Preferred Foot', placeholder='R/L') or ""
    overall = col2.number_input('Overall', min_value=0, max_value=100, step=1)
    position1 = col2.selectbox('Position 1',[' ','GK','LB','LWB','CB','RB','RWB','CDM','CM','LM','RM','CAM','LW','RW','LF','RF','CF','ST']) or ""
    position2 = col2.selectbox('Position 2',[' ','GK','LB','LWB','CB','RB','RWB','CDM','CM','LM','RM','CAM','LW','RW','LF','RF','CF','ST']) or ""
    position3 = col2.selectbox('Position 3',[' ','GK','LB','LWB','CB','RB','RWB','CDM','CM','LM','RM','CAM','LW','RW','LF','RF','CF','ST']) or ""
    position4 = col2.selectbox('Position 4',[' ','GK','LB','LWB','CB','RB','RWB','CDM','CM','LM','RM','CAM','LW','RW','LF','RF','CF','ST']) or ""
    position5 = col2.selectbox('Position 5',[' ','GK','LB','LWB','CB','RB','RWB','CDM','CM','LM','RM','CAM','LW','RW','LF','RF','CF','ST']) or ""
    position6 = col2.selectbox('Position 6',[' ','GK','LB','LWB','CB','RB','RWB','CDM','CM','LM','RM','CAM','LW','RW','LF','RF','CF','ST']) or ""

    # Create a dictionary with the data
    player_data = {
        'First Name': first_name,
        'Last Name': last_name,
        'Nation': nation,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'Preferred Foot': preferred_foot,
        'Overall': overall,
        'Position 1': position1,
        'Position 2': position2,
        'Position 3': position3,
        'Position 4': position4,
        'Position 5': position5,
        'Position 6': position6
    }

    # Button to save data
    if st.button('Submit'):
        # Save data even if some fields are empty
        save_data_to_mongodb(player_data)
        st.success('Data saved successfully!')

if __name__ == '__main__':
    main()
