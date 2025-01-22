import streamlit as st
import pandas as pd
from simMatch import Match
from simInputs import Player
from scrapeEloData import scrape_player_names
import plotly.graph_objs as go
import numpy as np
import math
from scipy.stats import gaussian_kde
import statistics

def set_wide():
    '''
    Method to set the page configuration to permanently be wide
    '''
    st.set_page_config(layout="wide")

@st.cache_data
def sim(player1, player2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving, num_sims):
    '''
    Main match simulation call method. Stores the data from the simMatch method call and returns it as a list.
    '''
    sim_data = [[] for _ in range(17)]
        
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
     
@st.cache_data
def p1RetandServe(player1, player2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving):
    matchh = Match(Player(player1), Player(player2), surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving)
    return [matchh.getP1Serve()*100, matchh.getP1Ret()*100]

def main():

    set_wide()

    home, about, contact = st.tabs(['Home', 'About', 'Contact'])

    with home:

        st.title("Tennis Match Simulator")

 
        player_names = scrape_player_names()

        ### Get inputs for the match simulation ###
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

        num_sims = st.number_input("Number of simulations (Max: 100,000)", min_value=1, value=100000, max_value=100000)
        

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


        # Store if the calculation is already done in session state
        if 'sim_data' not in st.session_state:
            st.session_state.sim_data = None
        
        if 'calculate' not in st.session_state:
            st.session_state.calculate = False

        if 'retandserve' not in st.session_state:
            st.session_state.retandserve = None

        # Perform the simulation if not already done
        if calculate:
            st.session_state.calculate = True  # Set calculation to True after button click
            
            st.session_state.sim_data = sim(player1, player2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving, num_sims)

            #st.session_state.retandserve = p1RetandServe(player1, player2, surface, best_out_of, p1SetsWon, p2SetsWon, p1GamesThis, p2GamesThis, p1GamesAll, p2GamesAll, p1PtsThis, p2PtsThis, p1PtsAll, p2PtsAll, p_serving)


                
        # If simulation is done, display results
        if st.session_state.calculate and st.session_state.sim_data: #and st.session_state.retandserve:
            sim_data = st.session_state.sim_data
            #retandserve = st.session_state.retandserve      

            sets, games, points, misc = st.tabs(['Sets', 'Games', 'Points', 'Misc'])


            ########### Sets Tab #############
            with sets:
                play1, graph, play2 = st.columns([0.3, 0.4, 0.3])



                with play1:
                    st.header(player1)

                    prob_win_match1 = (sim_data[0].count(str(player1)) / num_sims) * 100
                    prob_win_set1 = (sim_data[1].count(player1) / num_sims) * 100
                    prob_win_game1 = (sim_data[2].count(player1) / num_sims) * 100


                    st.subheader(f"Probability to win the *match*: {prob_win_match1:.2f}%")
                    st.subheader(f"Probability to win current *set*: {prob_win_set1:.2f}%")
                    st.subheader(f"Probability to win current *game*: {prob_win_game1:.2f}%") 
                    #st.subheader(f"Probability to win a *service point*: {retandserve[0]:.2f}%")
                    #st.subheader(f"Probability to win a *return point*: {retandserve[1]:.2f}%")

                    choice = st.selectbox("Probability to win exactly ___ sets", [0, 1, 2, 3], key=f"play1choice")

                    prob_this_set = (sim_data[3].count(choice) / num_sims) * 100
                    st.write(f"Probability to win {choice} sets: {round(prob_this_set, 2)}%")

                with play2:
                    st.header(player2)

                    prob_win_match2 = (sim_data[0].count(str(player2)) / num_sims) * 100
                    prob_win_set2 = (sim_data[1].count(player2) / num_sims) * 100
                    prob_win_game2 = (sim_data[2].count(player2) / num_sims) * 100 

                    st.subheader(f"Probability to win the *match*: {prob_win_match2:.2f}%")
                    st.subheader(f"Probability to win current *set*: {prob_win_set2:.2f}%")
                    st.subheader(f"Probability to win current *game*: {prob_win_game2:.2f}%") 
                    #st.subheader(f"Probability to win a *service point*: {(100-retandserve[1]):.2f}%")
                    #st.subheader(f"Probability to win a *return point*: {(100-retandserve[0]):.2f}%")

                    choice2 = st.selectbox("Probability to win exactly ___ sets", [0, 1, 2, 3], key=f"play2choice")

                    prob_this_set2 = (sim_data[4].count(choice2) / num_sims) * 100
                    st.write(f"Probability to win {choice2} sets: {prob_this_set2:.2f}%")

                with graph:
                    spread = sim_data[5]

                    @st.cache_data
                    def printGraph1(spread):
                        unique, counts = np.unique(spread, return_counts=True)

                        bar_x = unique
                        bar_y = np.round(counts / num_sims, 4)

                        #kde = gaussian_kde(spread)
                        #x_vals = np.linspace(min(spread) - 1, max(spread) + 1, 500)
                        #kde_y = kde(x_vals)

                        fig = go.Figure()

                        # barplot
                        fig.add_trace(go.Bar(x=bar_x, y=bar_y, name="Probability", marker_color="white"))

                        # distribution curve
                        #fig.add_trace(go.Scatter(x=x_vals, y=kde_y, mode='lines', name="Probability Distribution", line=dict(color='orange', width=2)))

                        # Customize layout
                        fig.update_layout(
                            title={
                                "text": f"<span style='font-size: 30px;'>Sets Spread Probability</span><br>{player2} sets - {player1} sets<sup></sup>",
                                "x": 0.5,  # Center the title
                                "xanchor": "center",
                            },
                            xaxis=dict(
                                title="<span style='font-size: 24px;'>Sets Spread</span>",  # Fix the title syntax here
                                showgrid=True
                            ),
                            yaxis=dict(
                                title="<span style='font-size: 24px;'>Probability</span>",  # Fix the title syntax here
                                showgrid=True
                            ),
                            legend=dict(x=0.7, y=1),
                            template="plotly",
                            height=500
                        )


                        # Display the plot in Streamlit
                        st.plotly_chart(fig, use_container_width=True)

                        spread_mean = round(sum(spread) / num_sims, 2)
                        if spread_mean >= 0: 
                            st.markdown(f'<h3 style="text-align: center;">Mean Sets Spread: +{spread_mean}</h3>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<h3 style="text-align: center;">Mean Sets Spread: {spread_mean}</h3>', unsafe_allow_html=True)

                        spread_std = statistics.stdev(spread)
                        st.markdown(f'<h3 style="text-align: center;">Mean Sets Standard Deviation: +{spread_std:.2f}</h3>', unsafe_allow_html=True)

                    printGraph1(spread)


                    st.write()

                    ######### Output distribution of total sets #############
                    total_sets = sim_data[14]

                    @st.cache_data
                    def printGraph2(total_sets):

                        unique2, counts2 = np.unique(total_sets, return_counts=True)

                        bar_x2 = unique2
                        bar_y2 = np.round(counts2 / num_sims, 4)

                        #kde = gaussian_kde(spread)
                        #x_vals = np.linspace(min(spread) - 1, max(spread) + 1, 500)
                        #kde_y = kde(x_vals)

                        fig2 = go.Figure()

                        # barplot
                        fig2.add_trace(go.Bar(x=bar_x2, y=bar_y2, name="Probability", marker_color="white"))

                        # distribution curve
                        #fig.add_trace(go.Scatter(x=x_vals, y=kde_y, mode='lines', name="Probability Distribution", line=dict(color='orange', width=2)))

                        # Customize layout
                        fig2.update_layout(
                            title={
                                "text": f"<span style='font-size: 30px;'>Number of Sets Probability</span>",
                                "x": 0.5,  # Center the title
                                "xanchor": "center",
                            },
                            xaxis=dict(
                                title="<span style='font-size: 24px;'>Number of Sets</span>",  # Fixed title syntax
                                showgrid=True
                            ),
                            yaxis=dict(
                                title="<span style='font-size: 24px;'>Probability</span>",  # Fixed title syntax
                                showgrid=True
                            ),
                            legend=dict(x=0.7, y=1),
                            template="plotly",
                            height=500
                        )


                        st.plotly_chart(fig2, use_container_width=True)

                        sets_mean = round(sum(total_sets) / num_sims, 2)
                        st.markdown(f'<h3 style="text-align: center;">Mean Total Number of Sets: {sets_mean}</h3>', unsafe_allow_html=True)
                        sets_std = statistics.stdev(total_sets)
                        st.markdown(f'<h3 style="text-align: center;">Total Number of Sets Standard Deviation: {sets_std:.2f}</h3>', unsafe_allow_html=True)


                    printGraph2(total_sets)


                ########## Games Tab ###############
            with games:

                    play1G, graphG, play2G = st.columns([0.3, 0.4, 0.3])

                    with play1G:
                        st.header(player1)
                        games1 = sim_data[6]

                        mean_won = sum(games1) / num_sims
                        highest = max(games1)
                        lowest = min(games1)

                        std = statistics.stdev(games1)

                        st.subheader(f"Mean Games Won: {mean_won:.2f}")
                        st.subheader(f"Highest Number of Games Won: {highest}")
                        st.subheader(f"Lowest Number of Games Won: {lowest}")
                        st.subheader(f"Standard Deviation of Games Won: {std:.2f}")
                        
                        # cover spread probability
                        spreadG = sim_data[8]
                        coverSpread1 = st.text_input("Probability to win by ___ games or more", value='0')
                        coverSpread1 = float(coverSpread1)
                        prob_cover = len([x for x in spreadG if x <= -coverSpread1]) / num_sims
                        st.write(f"Probability to win by {coverSpread1} games or more: {prob_cover:.2f}")

                        st.write("\n")
                    
                        # total games won probability 
                        moreThan1 = st.text_input("Probability to win >= ___ games", value=0, key=f"play1More")
                        moreThan1 = float(moreThan1)
                        prob_more_than = len([x for x in games1 if x >= moreThan1]) / num_sims
                        st.write(f"Probability to win {moreThan1} games or more: {prob_more_than:.2f}")


                    with play2G:
                        st.header(player2)

                        games2 = sim_data[7]

                        mean_won2 = sum(games2) / num_sims
                        highest2 = max(games2)
                        lowest2 = min(games2)

                        std2 = statistics.stdev(games2)

                        st.subheader(f"Mean Games Won: {mean_won2:.2f}")
                        st.subheader(f"Highest Number of Games Won: {highest2}")
                        st.subheader(f"Lowest Number of Games Won: {lowest2}")
                        st.subheader(f"Standard Deviation of Games Won: {std2:.2f}")

                        # cover spread probability 
                        coverSpread2 = st.text_input("Probability to win by ___ games or more", value=0, key=f"cover2")
                        coverSpread2 = float(coverSpread2)
                        prob_cover2 = len([x for x in spreadG if x >= coverSpread2]) / num_sims
                        st.write(f"Probability to win by {coverSpread2} games or more: {prob_cover2:.2f}")

                        st.write("\n")

                        # total games won probability
                        moreThan2 = st.text_input("Probability to win >= ___ games", value=0, key=f"play2More")
                        moreThan2 = float(moreThan2)
                        prob_more_than2 = len([x for x in games2 if x >= moreThan2]) / num_sims
                        st.write(f"Probability to win {moreThan2} games or more: {prob_more_than2:.2f}")                        

                    with graphG:
                        spreadG = sim_data[8]

                        @st.cache_data
                        def printSpreadGraphG(spreadG):
                            '''
                            Method to output the graph of the game spreads
                            We cache this method so that it does not rerun when widget inputs are updated
                            '''
                            spreadG = spreadG

                            uniqueG, countsG = np.unique(spreadG, return_counts=True)

                            bar_xG = uniqueG
                            bar_yG = np.round(countsG / num_sims, 4)

                            kde = gaussian_kde(spreadG)
                            x_vals = np.linspace(min(spreadG) - 1, max(spreadG) + 1, 500)
                            kde_y = kde(x_vals)

                            figG = go.Figure()

                            # barplot
                            figG.add_trace(go.Bar(x=bar_xG, y=bar_yG, name="Probability", marker_color="white"))

                            # distribution curve
                            figG.add_trace(go.Scatter(x=x_vals, y=kde_y, mode='lines', name="Probability Distribution", line=dict(color='orange', width=2)))

                            # Customize layout
                            figG.update_layout(
                                title={
                                    "text": f"<span style='font-size: 30px;'>Games Spread Probability</span><br>{player2} games - {player1} games<sup></sup>",
                                    "x": 0.5,  # Center the title
                                    "xanchor": "center",
                                },
                                xaxis=dict(
                                    title="<span style='font-size: 24px;'>Games Spread</span>",  # Fix the title syntax here
                                    showgrid=True
                                ),
                                yaxis=dict(
                                    title="<span style='font-size: 24px;'>Probability</span>",  # Fix the title syntax here
                                    showgrid=True
                                ),
                                legend=dict(x=0.7, y=1),
                                template="plotly",
                                height=500
                            )

                            # Display the plot in Streamlit
                            st.plotly_chart(figG, use_container_width=True) 

                            # output mean games spread
                            games_spread_mean = sum(spreadG) / num_sims
                            st.markdown(f'<h3 style="text-align: center;">Mean Games Spread: {games_spread_mean:.2f}</h3>', unsafe_allow_html=True)

                            games_spread_std = statistics.stdev(spreadG)
                            st.markdown(f'<h3 style="text-align: center;">Mean Games Standard Deviation: {games_spread_std:.2f}</h3>', unsafe_allow_html=True)


                            # end method

                        printSpreadGraphG(spreadG)      


                        ######## Games Total Graph ###############
                        totG = sim_data[12]

                        @st.cache_data
                        def printGraphTotG(totG):
                            '''
                            Method to output the graph of total number of games
                            We cache this method so that it does not rerun when widget inputs are updated
                            '''

                            uniqueTotG, countsTotG = np.unique(totG, return_counts=True)

                            bar_xTotG = uniqueTotG
                            bar_yTotG = np.round(countsTotG / num_sims, 4)


                            kde2 = gaussian_kde(totG)
                            x_vals2 = np.linspace(min(totG) - 1, max(totG) + 1, 500)
                            kde_y2 = kde2(x_vals2)

                            figTotG = go.Figure()

                            # barplot
                            figTotG.add_trace(go.Bar(x=bar_xTotG, y=bar_yTotG, name="Probability", marker_color="white"))

                            # distribution curve
                            figTotG.add_trace(go.Scatter(x=x_vals2, y=kde_y2, mode='lines', name="Probability Distribution", line=dict(color='orange', width=2)))

                            # Customize layout
                            figTotG.update_layout(
                                title={
                                    "text": f"<span style='font-size: 30px;'>Number of Games Probability</span>",
                                    "x": 0.5,  # Center the title
                                    "xanchor": "center",
                                },
                                xaxis=dict(
                                    title="<span style='font-size: 24px;'>Total Number of Games</span>",  # Fix the title syntax here
                                    showgrid=True
                                ),
                                yaxis=dict(
                                    title="<span style='font-size: 24px;'>Probability</span>",  # Fix the title syntax here
                                    showgrid=True
                                ),
                                legend=dict(x=0.7, y=1),
                                template="plotly",
                                height=500
                            )

                            # Display the plot in Streamlit
                            st.plotly_chart(figTotG, use_container_width=True)     

                            # output mean total games
                            games_total_mean = sum(totG) / num_sims
                            st.markdown(f'<h3 style="text-align: center;">Mean Number of Games: {games_total_mean:.2f}</h3>', unsafe_allow_html=True)

                            games_total_std = statistics.stdev(totG)
                            st.markdown(f'<h3 style="text-align: center;">Mean Number of Games Standard Deviation: {games_total_std:.2f}</h3>', unsafe_allow_html=True)


                            ### end method

                        printGraphTotG(totG)
    


                        # Create option to calculate probability of more than a certain number of games
                        @st.cache_data
                        def precompute_cumulative_counts(totG):
                            '''
                            Method to compute and return the cumulative number of occurences of each number of games in the sim
                            '''
                            totG_sorted = sorted(totG)
                            cumulative_counts = {}
                            n = len(totG_sorted)
                            for i, value in enumerate(totG_sorted):
                                if value not in cumulative_counts:
                                    cumulative_counts[value] = n - i
                            return cumulative_counts

                        # Callback function for dynamic updates
                        def calculate_probability_totG(total_more, cumulative_counts, num_sims):
                            '''
                            Method to compute and return the probability of seeing x number of games or more from the sim
                            '''
                            if total_more in cumulative_counts:
                                return cumulative_counts[total_more] / num_sims
                            elif total_more > max(cumulative_counts.keys()):
                                return 0.0
                            else:
                                return 1.0

                        cum_counts = precompute_cumulative_counts(totG)

                        # Define number input with a callback
                        st.number_input(
                            "Probability of ___ games or more:",
                            min_value=0, 
                            max_value=None,
                            value=0,
                            key="total_more",
                            on_change=lambda: st.session_state.update({
                                "prob_total_more": calculate_probability_totG(
                                    st.session_state['total_more'], cum_counts, num_sims
                                )
                            }),
                        )

                        # Display the result dynamically
                        st.write(
                            f"Probability of {st.session_state.get('total_more', 0)} games or more: "
                            f"{st.session_state.get('prob_total_more', 0.0):.2f}"
                        )         


            ##### Points tab ########
            with points:

                    play1P, graphP, play2P = st.columns([0.3, 0.4, 0.3])
                    points_spread = sim_data[11]

                    with play1P:
                        st.header(player1)

                        points1 = sim_data[9]


                        mean_points1 = sum(points1) / num_sims
                        highestPoints1 = max(points1)
                        lowestPoints1 = min(points1)
                        
                        stdP1 = statistics.stdev(points1)

                        st.subheader(f"Mean Number of Points Won: {mean_points1:.2f}")
                        st.subheader(f"Highest Number of Points Won: {highestPoints1}")
                        st.subheader(f"Lowest Number of Points Won: {lowestPoints1}")
                        st.subheader(f"Standard Deviation of Points Won: {stdP1:.2f}")

                        ### Probability to win by ___ points or more
                        to_cover = st.text_input("Probability to win by ___ points or more", value=0, key='cover1Pt')
                        to_cover = float(to_cover)
                        prob_coverP = len([x for x in points_spread if x <= -to_cover]) / num_sims
                        st.write(f"Probability of winning by {to_cover} points or more: {prob_coverP:.2f}")


                    with play2P:

                        st.header(player2)

                        points2 = sim_data[10]

                        mean_points2 = sum(points2) / num_sims
                        highestPoints2 = max(points2)
                        lowestPoints2 = min(points2)

                        stdP2 = statistics.stdev(points2)

                        st.subheader(f"Mean Number of Points Won: {mean_points2:.2f}")
                        st.subheader(f"Highest Number of Points Won: {highestPoints2}")
                        st.subheader(f"Lowest Number of Points Won: {lowestPoints2}")
                        st.subheader(f"Standard Deviation of Points Won: {stdP2:.2f}")

                        ### Probability to win by ___ points or more
                        to_cover2 = st.text_input("Probability to win by ___ points or more", value=0, key='cover2Pt')
                        to_cover2 = float(to_cover2)
                        prob_coverP2 = len([x for x in points_spread if x >= to_cover2]) / num_sims
                        st.write(f"Probability of winning by {to_cover2} points or more: {prob_coverP2:.2f}")


                    with graphP:


                        @st.cache_data
                        def printPointsSpreadGraph(points_spread):

                            uniquePt, countsPt = np.unique(points_spread, return_counts=True)

                            bar_xPt = uniquePt
                            bar_yPt = np.round(countsPt / num_sims, 4)


                            kdePt = gaussian_kde(points_spread)
                            x_valsPt = np.linspace(min(points_spread) - 1, max(points_spread) + 1, 500)
                            kde_yPt = kdePt(x_valsPt)

                            figPt = go.Figure()

                            # barplot
                            figPt.add_trace(go.Bar(x=bar_xPt, y=bar_yPt, name="Probability", marker_color="white"))

                            # distribution curve
                            figPt.add_trace(go.Scatter(x=x_valsPt, y=kde_yPt, mode='lines', name="Probability Distribution", line=dict(color='orange', width=2)))

                            # Customize layout
                            figPt.update_layout(
                                title={
                                    "text": f"<span style='font-size: 30px;'>Points Spread Probability</span><br>{player2} points - {player1} points<sup></sup>",
                                    "x": 0.5,  # Center the title
                                    "xanchor": "center",
                                },
                                xaxis=dict(
                                    title="<span style='font-size: 24px;'>Points Spread</span>",  # Fix the title syntax here
                                    showgrid=True
                                ),
                                yaxis=dict(
                                    title="<span style='font-size: 24px;'>Probability</span>",  # Fix the title syntax here
                                    showgrid=True
                                ),
                                legend=dict(x=0.7, y=1),
                                template="plotly",
                                height=500
                            )

                            # Display the plot in Streamlit
                            st.plotly_chart(figPt, use_container_width=True)     

                            # output mean total games
                            spread_mean = sum(points_spread) / num_sims
                            st.markdown(f'<h3 style="text-align: center;">Mean Points Spread: {spread_mean:.2f}</h3>', unsafe_allow_html=True) 

                            spread_std = statistics.stdev(points_spread)
                            st.markdown(f'<h3 style="text-align: center;">Mean Points Standard Deviation: {spread_std:.2f}</h3>', unsafe_allow_html=True) 


                        printPointsSpreadGraph(points_spread)
                
            with misc:
                tiebreaker_prob = (sum(sim_data[15]) / num_sims) * 100
                st.markdown(f"<h3 style='text-align: center;'>Probability of a tiebreak: {tiebreaker_prob:.2f}%</h3>", unsafe_allow_html=True)

                #st.subheader(f"Probability of a tiebreak: {tiebreaker_prob:.2f}")

                toNil_prob = (sum(sim_data[16]) / num_sims) * 100
                st.markdown(f"<h3 style='text-align: center;'>Probability of a 6 to Nil set: {toNil_prob:.2f}%</h3>", unsafe_allow_html=True)

                #st.subheader(f"Probability of a 6 to Nil set: {toNil_prob:.2f}")

    with about:
        st.header('Methodology')
        st.markdown('The basis of the simulation starts with determining the probability of each player winning a service and return point. This is first calculated by finding the probability to win any given point.' +
                    ' The probability to win any given point is derived from a players ELO rating on the surface. Looking at historical data, I built a function that outputs the probability '+
                    'of winning a point based on the difference between ELO ratings. From there, we need to find how these wins are split between service and return points. '+
                    'Again, looking at historical data, each player is given a ratio of how often they win service points compared to return points. For a given matchup, these ratios, '+
                    'combined with the point win probability function, determine a service point and return point probability for each player. ' + 
                    'Now that we have those probabilities, we can simulate a tennis match using basic logic, starting from point to point probabilities.')
        st.write('')
        st.header('The Data')
        st.markdown("Now, where does this 'historica data' come from? At the run of each new simulation, player ELO ratings are scraped from [Tennis Abstract](https://tennisabstract.com/reports/atp_elo_ratings.html) " + 
                    "which updates ELO ratings weekly. The service to return point ratio data is calculated from a [Kaggle dataset](https://www.kaggle.com/datasets/mohammadkumail110/tennis-player-data-serve-return-and-raw)" + 
                    " that has match by match historical data.")

    with contact:
        st.header('Grant Hohol')
        st.subheader('I am a sophomore Computer Sciences and Statistics undergraduate at the University of Wisconsin-Madison. You can contact me or see more of my work at the following links.')
        st.markdown("~ Github: [@granthohol](https://github.com/granthohol/)")
        st.markdown("~ [LinkedIn](https://www.linkedin.com/in/grant-hohol-08520b291/)")
        st.markdown("~ X (Twitter): [@granthohol55](https://x.com/granthohol55)")
        st.write("~ Email: ghohol@wisc.edu")
        st.write("~ Phone: 920-370-2380")                    





if __name__ == "__main__":
    main()
