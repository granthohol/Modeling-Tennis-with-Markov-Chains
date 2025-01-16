import streamlit as st
import pandas as pd
from simMatch import Match
from simInputs import Player
import plotly.graph_objs as go
import numpy as np
from scipy.stats import gaussian_kde

@st.cache_data
def sim(player1, player2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving, num_sims):
    sim_data = [[] for _ in range(14)]
    
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

    return sim_data

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
        
        num_sims = 1000

        if calculate:
            sim_data = sim(player1, player2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving, num_sims)

            sets, games, points = st.tabs(['Sets', 'Games', 'Points'])

            with sets:
                play1, graph, play2 = st.columns([0.3, 0.4, 0.3])

                with play1:
                    st.header(player1)

                    prob_win_match1 = (sim_data[0].count(str(player1)) / num_sims) * 100
                    prob_win_set1 = (sim_data[1].count(player1) / num_sims) * 100
                    prob_win_game1 = (sim_data[2].count(player1) / num_sims) * 100

                    st.subheader(f"Probability to win the match: {round(prob_win_match1, 4)}%")
                    st.subheader(f"Probability to win current set: {round(prob_win_set1, 4)}%")
                    st.subheader(f"Probability to win current game: {round(prob_win_game1, 4)}%") 

                    choice = st.selectbox("Probability to win ___ sets", [0, 1, 2, 3])

                    
                    prob_this_set = (sim_data[3].count(choice) / num_sims) * 100
                    st.write(f"Probability to win {choice} sets: {round(prob_this_set, 4)}%")



                with play2:
                    st.header(player2)

                    prob_win_match2 = (sim_data[0].count(str(player2)) / num_sims) * 100
                    prob_win_set2 = (sim_data[1].count(player2) / num_sims) * 100
                    prob_win_game2 = (sim_data[2].count(player2) / num_sims) * 100 

                    st.subheader(f"Probability to win the match: {round(prob_win_match2, 4)}%")
                    st.subheader(f"Probability to win current set: {round(prob_win_set2, 4)}%")
                    st.subheader(f"Probability to win current game: {round(prob_win_game2, 4)}%")      


                with graph:

                    spread = sim_data[5]

                    unique, counts = np.unique(spread, return_counts=True)

                    bar_x = unique
                    bar_y = np.round(counts / num_sims, 4)

                    kde = gaussian_kde(spread)
                    x_vals = np.linspace(min(spread) - 1, max(spread) + 1, 500)
                    kde_y = kde(x_vals)

                    fig = go.Figure()

                    # barplot
                    fig.add_trace(go.Bar(x=bar_x, y=bar_y, name="Probability", marker_color="white"))

                    # distribution curve
                    fig.add_trace(go.Scatter(x=x_vals, y=kde_y, mode='lines', name="Probability Distribution", line=dict(color='orange', width=2)))

                    # Customize layout
                    fig.update_layout(
                        title={
                            "text": f"Sets Spread Probability<br>{player2} sets - {player1} sets<sup></sup>",
                            "x": 0.5,  # Center the title
                            "xanchor": "center",
                        },
                        xaxis=dict(title="Sets Spread", showgrid=True),
                        yaxis=dict(title="Probability", showgrid=True),
                        legend=dict(x=0.7, y=1),
                        template="plotly",
                        height=500
                    )

                    # Display the plot in Streamlit
                    st.plotly_chart(fig)




if __name__ == "__main__":
    main()