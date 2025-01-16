import streamlit as st
import pandas as pd
from simMatch import Match
from simInputs import Player

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
        if serving == player1:
            p_serving = 1 # convert to int to pass to sim method
        else:
            p_serving = 2

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

        ###### Sim Matchup #########

        # list of lists that hold all of the sim data from the simulations
        sim_data = [[] for _ in range(14)]
        
        num_sims = 1000


        if calculate:
            p1 = Player(player1)
            p2 = Player(player2)

            matchup = Match(p1, p2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving)
            p1_serve = matchup.getP1Serve()
            p1_ret = matchup.getP1Ret()

            for _ in range(num_sims):
                matchup = Match(p1, p2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving)
                matchup.simMatch(p1_serve, p1_ret)
                match_data = matchup.get_data()

                # add the data from this sim to the dictionary
                for i, data in enumerate(match_data):
                    sim_data[i].append(data) 

            sets, games, points = st.tabs(['Sets', 'Games', 'Points'])

            with sets:
                play1, graph, play2 = st.columns([0.25, 0.5, 0.25])

                with play1:
                    st.subheader(player1)

                    prob_win_match1 = (sim_data[0].count(str(player1)) / num_sims) * 100
                    prob_win_set1 = (sim_data[1].count(player1) / num_sims) * 100
                    prob_win_game1 = (sim_data[2].count(player1) / num_sims) * 100

                    st.write(f"Probability to win the match: {round(prob_win_match1, 4)}%")
                    st.write(f"Probability to win next (or current) set: {round(prob_win_set1, 4)}%")
                    st.write(f"Probability to win next (or current) game: {round(prob_win_game1, 4)}%") 

                with play2:
                    st.subheader(player1)

                    prob_win_match2 = (sim_data[0].count(str(player2)) / num_sims) * 100
                    prob_win_set2 = (sim_data[1].count(player2) / num_sims) * 100
                    prob_win_game2 = (sim_data[2].count(player2) / num_sims) * 100 

                    st.write(f"Probability to win the match: {round(prob_win_match2, 4)}%")
                    st.write(f"Probability to win next (or current) set: {round(prob_win_set2, 4)}%")
                    st.write(f"Probability to win next (or current) game: {round(prob_win_game2, 4)}%")                     






if __name__ == "__main__":
    main()