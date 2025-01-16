from simInputs import Player, p1ActualRetProb, p1ActualServeProb
import random


class Match():
       
    def __init__(self, player1: Player, player2: Player, surface: str, best_out_of: int, p1Sets: int, p2Sets: int, p1Games: int, p2Games: int, p1GamesTot: int, p2GamesTot: int, p1Pts: int, p2Pts: int, p1PtsTot: int, p2PtsTot: int, serving: int):

        self.match_winner = None
        self.set_winner = None
        self.game_winner = None
        self.player1 = player1
        self.player2 = player2
        self.surface = surface
        self.best_out_of = best_out_of
        self.p1Sets = p1Sets
        self.p2Sets = p2Sets
        self.p1Games = p1Games
        self.p2Games = p2Games
        self.p1GamesTot = p1GamesTot
        self.p2GamesTot = p2GamesTot
        self.p1Pts = p1Pts
        self.p2Pts = p2Pts
        self.p1PtsTot = p1PtsTot
        self.p2PtsTot = p2PtsTot
        self.serving = serving

        ''' Parameters:
        - player1: The player object 
        - player2: The player object 
        - surface: the surface type being played on 
        - best_out_of: how many sets the game is being played out of 
        - p1Sets: how many sets player1 has won
        - p2sets: how many sets player2 has won
        - p1Games: how many games player1 has won THIS SET
        - p2Games: how many games player2 has won THIS SET
        - p1GamesTot: how many games player1 has won ALL MATCH
        - p2GamesTot: how many games player2 has won ALL MATCH 
        - p1Pts: how many points player1 has won THIS GAME
        - p2Pts: how many points player2 has won THIS GAME
        - p1PtsTot: how many points player1 has won ALL MATCH
        - p2PtsTot: how many points player2 has won ALL MATCH 
        - serving: Either 1 or 2, the player that is serving or about to serve'''


    def getP1Serve(self):
        return p1ActualServeProb(self.player1, self.player2, self.surface)

    def getP1Ret(self):
        return p1ActualRetProb(self.player1, self.player2, self.surface)


    # assumes player1 is to serve
    def simMatch(self, p1_serve_prob, p1_ret_prob):
        '''
        The main method used to simulate a match between two players on a given surface

        Parameters:
        - p1_serve_prob: the probability of p1 winning a serve point
        - p1_ret_prob: the probability of p1 winning a return point

        '''

        if self.best_out_of == 5:
            sets_needed = 3
        elif self.best_out_of == 3:
            sets_needed = 2
        else:
            raise ValueError("Invalid parameter passed for 'best_out_of' parameter")
        

        liveSet = True # denotes whether there is a possibility of it being a live set and number of games won or points scored so far can be passed

        max_iter = 100
        iter = 0
        while True:
            iter += 1
            if iter > max_iter:
                print("Infinite Loop in sim match")
                return

            if self.serving == 1: # player 1 is serving first
                if liveSet:
                    liveSet = False
                    if self.simulate_set(p1_serve_prob, p1_ret_prob, self.p1Games, self.p2Games, self.p1Pts, self.p2Pts, True):
                        self.p1Sets += 1
                    else:
                        self.p2Sets += 1
                else:
                    if self.simulate_set(p1_serve_prob, p1_ret_prob, 0, 0, 0, 0, True):
                        self.p1Sets += 1
                    else:
                        self.p2Sets += 1
            else: # player 2 is serving first
                if liveSet:
                    liveSet = False
                    if self.simulate_set(p1_serve_prob, p1_ret_prob, self.p1Games, self.p2Games, self.p1Pts, self.p2Pts, False):
                        self.p1Sets += 1
                    else:
                        self.p2Sets += 1
                else:
                    if self.simulate_set(p1_serve_prob, p1_ret_prob, 0, 0, 0, 0, False):
                        self.p1Sets += 1
                    else:
                        self.p2Sets += 1

            # check if anyone has won
            if self.p1Sets == sets_needed:
                self.match_winner = self.player1
                return

            if self.p2Sets == sets_needed:
                self.match_winner = self.player2
                return


    def simulate_game(self, p_point: float, p1_pts: int, p2_pts: int):
        '''
        Simulates a game of tennis match and returns True if player1 wins the game. 
        Updates player points total

        Parameters: 
        - p_point: Probability of player1 scoring a point (dependent on serving vs returning)
        - p1_score: the current number of points for player1
        - p2_score: the current number of points for player2
        '''
        p1_score, p2_score = p1_pts, p2_pts

        max_iter = 100
        iter = 0
        while True:
            iter += 1
            if iter > max_iter:
                print("Infinite Loop in sim game")
                return
            
            if random.random() < p_point: # player wins point
                p1_score += 1
            else:
                p2_score += 1
            
            # check if anyone has won game
            if (p1_score >= 4) and (p1_score - p2_score > 1):
                self.p1PtsTot += p1_score
                self.p2PtsTot += p2_score
                if self.game_winner == None:
                    self.game_winner = self.player1
                return True
            
            if (p2_score >= 4) and (p2_score - p1_score > 1):
                self.p1PtsTot += p1_score
                self.p2PtsTot += p2_score
                if self.game_winner == None:
                    self.game_winner = self.player2
                return False

    def simulate_set(self, p1_serve: float, p1_ret: float, p1_games: int, p2_games: int, p1_pts: int, p2_pts: int, player1_serving: bool):
        '''
        Simulates a set of a tennis match and returns True if player1 wins the set.

        Parameters:
        - p1_serve: the probability that player1 wins a serve point
        - p2_ret: the probability that player1 wins a return point
        - p1_games: the number of games that player1 has won in this set
        - p2_games: the number of games that player2 has won in this set
        - p1_pts: the number of points player1 has won this game
        - p2_pts: the number of points player2 has won this game
        '''
        player1_games, player2_games = p1_games, p2_games

        if player1_games > 7 or player2_games > 7:
            raise ValueError("Invalid number of current games won passed as parameter")
        
        p1_serving = player1_serving
        liveGame = True

        max_iter = 100
        iter = 0
        while True:
            iter += 1
            if iter > max_iter:
                print("Infinite Loop in sim set")
                return

            if p1_serving:
                if liveGame: # first game in sim, need to account for current points scored in this game
                    liveGame = False
                    if self.simulate_game(p1_serve, p1_pts, p2_pts):
                        player1_games += 1
                        self.set_winner = self.player1
                        p1_serving = False
                    else:
                        player2_games += 1
                        self.set_winner = self.player2
                        p1_serving = False

                else: # not first game in sim, each player at 0 points
                    if self.simulate_game(p1_serve, 0, 0):
                        player1_games += 1
                        p1_serving = False
                    else:
                        player2_games += 1
                        p1_serving = False
            else: # Player 2 is serving
                if liveGame:
                    liveGame = False
                    if self.simulate_game(p1_ret, p1_pts, p2_pts):
                        player1_games += 1
                        self.set_winner = self.player1
                        p1_serving = True
                    else:
                        player2_games += 1
                        self.set_winner = self.player2
                        p1_serving = True
                else:
                    if self.simulate_game(p1_ret, 0, 0):
                        player1_games += 1
                        p1_serving = True
                    else:
                        player2_games += 1
                        p1_serving = True

            # check for tiebreak
            if player1_games == 6 and player2_games == 6:
                # player 1 wins tiebreak and set
                if self.simulate_set_tiebreak((p1_serve + p1_ret)/2): # pass the probability of player1 winning any point since tiebreaks are ~ even on serves
                    self.p1GamesTot += 7 
                    self.p2GamesTot += 6

                    # if it is p1 turn to serve, set self.serving = 1 so that sim next set knows
                    if p1_serving == True:
                        self.serving = 1
                    else: 
                        self.serving = 2

                    return True
                
                # player 2 wins tiebreak and set
                else: 
                    self.p2GamesTot += 7
                    self.p1GamesTot += 6
                    # if it is p1 turn to serve, set self.serving = 1 so that sim next set knows
                    if p1_serving == True:
                        self.serving = 1
                    else: 
                        self.serving = 2

                    return False
                
            # Player 1 wins set
            if player1_games >= 6 and player1_games - player2_games > 1:
                self.p1GamesTot += player1_games
                self.p2GamesTot += player2_games

                # if it is p1 turn to serve, set self.serving = 1 so that sim next set knows
                if p1_serving == True:
                    self.serving = 1
                else: 
                    self.serving = 2
                return True
            
            # player 2 wins set
            if player2_games >= 6 and player2_games - player1_games > 1:
                self.p1GamesTot += player1_games
                self.p2GamesTot += player2_games

                # if it is p1 turn to serve, set self.serving = 1 so that sim next set knows
                if p1_serving == True:
                    self.serving = 1
                else: 
                    self.serving = 2
                return False


    def simulate_set_tiebreak(self, p_point: float):
        '''
        Simulates a tiebreaker set where returns True if the player with passed probability wins the tiebreaker
        '''

        player_score, opponent_score = 0, 0

        while True:
            if random.random() < p_point:
                player_score += 1
            else:
                opponent_score += 1
            
            if player_score >= 7 and player_score - opponent_score > 1:
                return True
            
            if opponent_score >= 7 and opponent_score - player_score > 1:
                return False 
            
    def get_data(self):
        match_data = [
            self.match_winner.getName(), # winner
            self.set_winner.getName(), # set winner
            self.game_winner.getName(), # game winner
            self.p1Sets,
            self.p2Sets,
            self.p1Sets - self.p2Sets, 
            self.p1GamesTot,
            self.p2GamesTot,
            self.p1GamesTot - self.p2GamesTot, 
            self.p1PtsTot,
            self.p2PtsTot,
            self.p1PtsTot - self.p2PtsTot,
            self.p1GamesTot + self.p2GamesTot,
            self.p1PtsTot + self.p2PtsTot
        ]

        return match_data
    

    
def main():

    carlos = Player("Carlos Alcaraz")
    jannik = Player("Jannik Sinner")

    matchup = Match(carlos, jannik, "Grass", 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2)
    p1Serve = matchup.getP1Serve()
    p1Ret = matchup.getP1Ret()

    sim_data = [[] for _ in range(14)]

    
    for _ in range(100000):
        matchup = Match(carlos, jannik, "Grass", 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2)
        matchup.simMatch(p1Serve, p1Ret)
        match_data = matchup.get_data()

        # add the data from this sim to the dictionary
        for i, data in enumerate(match_data):
            sim_data[i].append(data) 

    prob_win_match1 = round(sim_data[0].count("Jannik Sinner") / 100000, 4)
    prob_win_set1 = round(sim_data[1].count('Jannik Sinner') / 100000, 4)
    prob_win_game1 = round(sim_data[2].count('Jannik Sinner') / 100000, 4)

    print(f"Probability to win the match: {prob_win_match1}")
    print(f"Probability to win next (or current) set: {prob_win_set1}")
    print(f"Probability to win next (or current) game: {prob_win_game1}")     

    print(sim_data[0])   

    '''print("\nMatch Summary:")
    for i in range(14):
        print(sim_data[i])'''

if __name__ == "__main__":
    main()