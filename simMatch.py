from simInputs import Player
import random


class Match():

       
    def __init__(self, player1: Player, player2: Player, surface: str, best_out_of: int, p1Sets: int, p2Sets: int, p1Games: int, p2Games: int, p1GamesTot: int, p2GamesTot: int, p1Pts: int, p2Pts: int, p1PtsTot: int, p2PtsTot: int):

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

        ''' Parameters:
        - player1: The player object that is to serve or serving
        - player2: The player object that is to return or returning
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
        - p2PtsTot: how many points player2 has won ALL MATCH '''

    # assumes player1 is to serve
    def simMatch(self):
        '''
        The main method used to simulate a match between two players on a given surface

        '''

        # dictionary to hold results to return

        games_needed = 0
        if self.best_out_of == 5:
            games_needed = 3
        elif self.best_out_of == 3:
            games_needed = 2
        else:
            raise ValueError("Invalid parameter passed for 'best_out_of' parameter")
        

    


    def simulate_game(self, p1_pts, p2_pts, p_point):
        '''
        Simulates a game of tennis match and returns True if player1 wins the game. 
        Updates player points total

        Parameters: 
        - p_point: Probability of player1 scoring a point (dependent on serving vs returning)
        - p1_score: the current number of points for player1
        - p2_score: the current number of points for player2
        '''
        p1_score, p2_score = p1_pts, p2_pts

        while True:
            if random.random() < p_point: # player wins point
                p1_score += 1
            else:
                p1_score += 1
            
            # check if anyone has won game
            if (p1_score >= 4) and (p1_score - p2_score > 1):
                self.p1PtsTot += p1_score
                self.p2PtsTot += p2_score
                return True
            
            if (p1_score >= 4) and (p2_score - p1_score > 1):
                self.p1PtsTot += p1_score
                self.p2PtsTot += p2_score
                return False

    def simulate_set(self, p1_serve: float, p1_ret: float, p1_games: int, p2_games: int, p1_pts: int, p2_pts: int, p1_serving: bool):
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
        
        p1_serving = p1_serving
        firstGame = True

        while True:
            if p1_serving:
                if firstGame: # first game in sim, need to account for current points scored in this game
                    firstGame = False
                    if self.simulate_game(p1_serve, p1_pts, p2_pts):
                        player1_games += 1
                    else:
                        player2_games += 1
                else: # not first game in sim, each player at 0 points
                    if self.simulate_game(p1_serve, 0, 0):
                        player1_games += 1
                    else:
                        player2_games += 1
            else: # Player 2 is serving
                if firstGame:
                    firstGame = False
                    if self.simulate_game(p1_ret, p1_pts, p2_pts):
                        player1_games += 1
                    else:
                        player2_games += 1
                else:
                    if self.simulate_game(p1_ret, 0, 0):
                        player1_games += 1
                    else:
                        player2_games += 1

            # check for tiebreak
            if player1_games == 6 and player2_games == 6:
                # player 1 wins tiebreak and set
                if self.simulate_set_tiebreak((p1_serve + p1_ret)/2): # pass the probability of player1 winning any point since tiebreaks are ~ even on serves
                    self.p1GamesTot += 7 
                    self.p2GamesTot += 6
                    return True
                # player 2 wins tiebreak and set
                else: 
                    self.p2GamesTot += 7
                    self.p1GamesTot += 6
                    return False
                
            # Player 1 wins set
            if player1_games >= 6 and player1_games - player2_games > 1:
                self.p1GamesTot += player1_games
                self.p2GamesTot += player2_games
                return True
            
            # player 2 wins set
            if player2_games >= 6 and player2_games - player1_games > 1:
                self.p1GamesTot += player1_games
                self.p2GamesTot += player2_games
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
            
    def get_dict(self):
        match_dict = {
            "Winner" : None,
            "Next Set Winner": None,
            "Next Game Winner": None, 
            "Player 1 Sets": self.p1Sets,
            "Player 2 Sets": self.p2Sets,
            "Sets Spread": self.p1Sets - self.p2Sets, 
            "Player 1 Games": self.p1GamesTot,
            "Player 2 Games": self.p2GamesTot,
            "Games Spread": self.p1GamesTot - self.p2GamesTot, 
            "Player 1 Points": self.p1PtsTot,
            "Player 2 Poitns": self.p2PtsTot,
            "Points Spread": self.p1PtsTot - self.p2PtsTot,
            "Total Games": self.p1GamesTot + self.p2GamesTot
        }