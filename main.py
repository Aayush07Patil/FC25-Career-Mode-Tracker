import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os

# Function to save the data to a CSV file


def main():
    # Sidebar for page navigation
    with st.sidebar:
            page_selected = option_menu(
                menu_title = "Menu",
                options = ["Matchday","ADD Senior Squad Player","ADD Youth Squad Player"],
                default_index = 0
            )
        
    #### Dynamic module import and execution ####
    try:
        if page_selected == "ADD Senior Squad Player":
            import add_player_senior_squad
            add_player_senior_squad.main()
        elif page_selected == "ADD Youth Squad Player":
            import add_player_youth_squad
            add_player_youth_squad.main()
        elif page_selected == "Matchday":
            import match_day
            match_day.main()
    except ImportError as e:
        st.error(f"Error loading module: {e}") 


if __name__ == '__main__':
    main()