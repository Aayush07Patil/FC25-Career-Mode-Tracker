import streamlit as st
import pandas as pd
from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
DB_NAME = "FC25_Chelsea_CM_tracker"# Name of your database
COLLECTION_NAME_PLAYERS = "senior_squad_players_season_1"
COLLECTION_NAME_MATCHDAY = "Matchday_Records_season_1"  # Name of your collection

# Create a MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection_players = db[COLLECTION_NAME_PLAYERS]
collection_matchday = db[COLLECTION_NAME_MATCHDAY]

# Initialize session state to store player stats
if 'player_stats' not in st.session_state:
    st.session_state.player_stats = {
        'Goals': {},
        'Assists': {},
        'Yellow Cards': {},
        'Red Cards': {}
    }

def save_data_to_mongodb(data):
    # Insert the data into MongoDB
    collection_matchday.insert_one(data)

def get_players_from_mongodb():
    # Fetch player names from MongoDB
    players = collection_players.find({}, {"First Name": 1, "Last Name": 1})  # Modify the projection based on your schema
    player_names = [f"{player['First Name']} {player['Last Name']}" for player in players]
    return player_names

def main():
    player_options = get_players_from_mongodb()

    # Streamlit UI for inputs
    st.title('Match Day')

    # Input fields for match data
    competition_name = st.selectbox('Competition Name', ['Premier League', 'Champions League', 'FA Cup', 'Carabao Cup', 'UEFA Conference League', 'Pre Season Friendlies'])
    stage = st.selectbox('Stage', ['Regular Season', 'Group Stage', 'Play Offs', 'Round of 64', 'Round of 32', 'Round of 16', 'Quarter Finals', 'Semi Finals', 'Final'])
    opposition = st.text_input('Opposition')
    fixture_location = st.selectbox('Fixture Location', ['Home', 'Away', 'Neutral'])

    team_score = st.number_input('Team Score', min_value=0, step=1)
    opposition_score = st.number_input('Opposition Score', min_value=0, step=1)

    team_possession = st.number_input('Team Possession (%)', min_value=0, max_value=100, step=1)
    opposition_possession = 100 - team_possession

    team_shots = st.number_input('Team Shots', min_value=0, step=1)
    opposition_shots = st.number_input('Opposition Shots', min_value=0, step=1)

    # Player Stats Inputs
    st.title("Players Stats") 
    
    selected_player = st.selectbox('Select Player', player_options)
    
    # Inputs for stats
    goals = st.number_input('Goals', min_value=0, step=1)
    assists = st.number_input('Assists', min_value=0, step=1)
    yc = st.number_input('Yellow Cards', min_value=0, step=0)
    rc = st.number_input('Red Cards', min_value=0, step=0)

    # Button to submit individual player stats
    if st.button('Submit Stat'):
        # Update player stats in session state
        if goals > 0:
            st.session_state.player_stats['Goals'][selected_player] = st.session_state.player_stats['Goals'].get(selected_player, 0) + goals
        if assists > 0:
            st.session_state.player_stats['Assists'][selected_player] = st.session_state.player_stats['Assists'].get(selected_player, 0) + assists
        if yc > 0:
            st.session_state.player_stats['Yellow Cards'][selected_player] = st.session_state.player_stats['Yellow Cards'].get(selected_player, 0) + yc
        if rc > 0:
            st.session_state.player_stats['Red Cards'][selected_player] = st.session_state.player_stats['Red Cards'].get(selected_player, 0) + rc

        st.success(f'Statistics for {selected_player} submitted successfully!')

    # Display current player stats
    st.write("Current Player Stats:")
    st.write(st.session_state.player_stats)

    # Button to submit match info
    if st.button('Submit Info'):
        # Create a dictionary with the match data
        match_data = {
            'Competition Name': competition_name,
            'Stage': stage,
            'Opposition': opposition,
            'Fixture Location': fixture_location,
            'Team Score': team_score,
            'Opposition Score': opposition_score,
            'Team Possession (%)': team_possession,
            'Opposition Possession (%)': opposition_possession,
            'Team Shots': team_shots,
            'Opposition Shots': opposition_shots,
            'Goals': st.session_state.player_stats['Goals'],
            'Assists': st.session_state.player_stats['Assists'],
            'Yellow Cards': st.session_state.player_stats['Yellow Cards'],
            'Red Cards': st.session_state.player_stats['Red Cards']
        }
        
        # Save match data to MongoDB
        save_data_to_mongodb(match_data)
        st.success('Match data saved successfully!')
        
        # Reset player stats after submission
        st.session_state.player_stats = {
            'Goals': {},
            'Assists': {},
            'Yellow Cards': {},
            'Red Cards': {}
        }

if __name__ == '__main__':
    main()
