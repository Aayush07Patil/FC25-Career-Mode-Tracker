import streamlit as st
import pandas as pd
import os

# Define a function to save the data to a CSV file
def save_match_data_to_csv(data, file_name="data/match_data.csv"):
    df = pd.DataFrame([data])
    # Check if the file exists, if not create a new CSV, else append to it
    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, mode='a', index=False, header=False)

def main():
    
    csv_file_path = "data/senior_squad_player_data.csv"  # Update the path to your CSV file
    players_df = pd.read_csv(csv_file_path)

    # Combine 'First name' and 'Last name' into a full name for multiselect options
    players_df['Full Name'] = players_df['First Name'] + ' ' + players_df['Last Name']

    # Convert the full names to a list for the multiselect
    player_options = players_df['Full Name'].tolist()

    # Streamlit UI for inputs
    st.title('Match Day')

    # Input fields
    competition_name = st.selectbox('Competition Name', ['Premier League', 'Champions League', 'FA Cup', 'Carabao Cup','UEFA Conference League','Pre Season Friendlies'])
    stage = st.selectbox('Stage', ['Regular Season','Group Stage','Play Offs','Round of 64','Round of 32','Round of 16','Quarter Finals', 'Semi Finals', 'Final'])
    opposition = st.text_input('Opposition')
    fixture_location = st.selectbox('Fixture Location', ['Home', 'Away', 'Neutral'])

    team_score = st.number_input('Team Score', min_value=0, step=1)
    opposition_score = st.number_input('Opposition Score', min_value=0, step=1)

    team_possession = st.number_input('Team Possession (%)', min_value=0, max_value=100, step=1)
    opposition_possession = 100 - team_possession

    team_shots = st.number_input('Team Shots', min_value=0, step=1)
    opposition_shots = st.number_input('Opposition Shots', min_value=0, step=1)

    # Create a dictionary with the data
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
        'Oppostion Shots': opposition_shots
    }

    # Button to save data
    if st.button('Submit'):
        # Save match data to CSV
        save_match_data_to_csv(match_data)
        st.success('Match data saved successfully!')
        
    st.title("Players played in the match")
    selected_players = st.multiselect('Select Players', player_options)
    
    goal_scorer = st.selectbox('Goal scorer', selected_players)
    goals = st.number_input('Goals',min_value=1,step=1)
    
    assist_giver = st.selectbox('Assist Giver',selected_players)
    assists = st.number_input('Assists',min_value=1,step=1)
    
    yellow_card_receiver = st.selectbox('Yellow Card Receiver',selected_players)
    yc = st.number_input('YC',min_value=1,step=1)
    
    red_card_receiver = st.selectbox('Red Card Receiver',selected_players)
    rc = st.number_input('RC',min_value=1,step=1)
        
if __name__ == '__main__':
    main()
    