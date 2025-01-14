import streamlit as st
import pandas as pd

def main():

    home, about, contact = st.tabs(['Home', 'About', 'Contact'])

    with home:

        st.title("Tennis Match Simulator")

        player_data = pd.read_csv('https://raw.githubusercontent.com/granthohol/Modeling-Tennis-with-Markov-Chains/main/Data/golden_ratio_data.csv')
        player_data = player_data.drop_duplicates(subset=['Name'])
        player_names = player_data['Name'].tolist()

        player1 = st.selectbox("Player 1",
                              player_names,
                              key="player1")
        
        player2 = st.selectbox("Player 2", 
                               player_names, 
                               key="player2")
        
        surface = st.selectbox("Surface", ["Grass", "Hard", "Clay"])

        best_out_of = st.selectbox("Best out of how many sets", [3, 5])

        serving = st.selectbox("Player Who Is Set to Serve", [player1, player2])

        # Dynamically adjust the max_value of the slider based on the best_out_of selection
        max_sets = 2 if best_out_of == 5 else 1

        p1, p2 = st.columns([0.5, 0.5])

        with p1:
            st.subheader(player1)

            p1SetsWon = st.number_input("Sets Won", min_value=0, max_value=max_sets, value=0, key = f"p1_sets_won")
            p1GamesAll = st.number_input("Games Won All Match", min_value=0, max_value=best_out_of*7, value=0, key=f"p1_games_all")
            p1GamesThis = st.number_input("Games Won This Set", min_value=0, max_value=7, value=0, key=f"p1_games_this")
            p1PtsAll = st.number_input("Points Won All Match", min_value=0, max_value=None, value=0, key=f"p1_pts_all")
            p1PtsThis = st.number_input("Points Won This Game", min_value=0, max_value=None, value=0, key=f"p1_pts_this")

        with p2:
            st.subheader(player2)

            p2SetsWon = st.number_input("Sets Won", min_value=0, max_value=max_sets, value=0, key=f"p2_sets_won")
            p2GamesAll = st.number_input("Games Won All Match", min_value=0, max_value=best_out_of*7, value=0, key=f"p2_games_all")
            p2GamesThis = st.number_input("Games Won This Set", min_value=0, max_value=7, value=0, key=f"p2_games_this")
            p2PtsAll = st.number_input("Points Won All Match", min_value=0, max_value=None, value=0, key=f"p2_pts_all")
            p2PtsThis = st.number_input("Points Won This Game", min_value=0, max_value=None, value=0, key=f"p2_pts_this")

        
        calculate = st.button("Run Simulation")






if __name__ == "__main__":
    main()