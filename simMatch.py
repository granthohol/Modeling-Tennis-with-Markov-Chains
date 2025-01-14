from simInputs import Player
import random

# assumes player1 is to serve
def simMatch(player1: Player, player2: Player, surface: str, best_out_of: int, p1Sets: int, p2Sets: int, p1Games: int, p2Games: int, p1GamesTot: int, p2GamesTot: int, p1Pts: int, p2Pts: int, p1PtsTot: int, p2PtsTot: int):
    '''
    The main method used to simulate a match between two players on a given surface

    Parameters:
    - player1: The player object that is to serve
    - player2: The player object that is to return
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
    - p1Pts: how many points player1 has won ALL MATCH
    - p2Pts: how many points player2 has won ALL MATCH

    Returns: A dictionary with the following information
    - Winner: the winner of the match
    - Next set winner: The winner of the next (or current) set
    - Next game winner: The winner of the next (or current) game
    - Sets spread: The difference in sets won between player1 and player2
    - Games spread: The difference in games won between player1 and player2
    - Points spread: The difference in points won between player1 and player2
    - Total games: Total # of games played
    '''

def simulate_game(p_point: float, p1_pts: int, p2_pts: int):
    '''
    Simulates a game of tennis match and returns True if player with passed probability wins the game

    Parameters: 
    - p_point: Probability of player1 (the serving player) scoring a point
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
            return True
        
        if (p1_score >= 4) and (p2_score - p1_score > 1):
            return False

def simulate_set(p1_serve: float, p2_serve: float, p1_games: int, p2_games: int, p1_pts: int, p2_pts: int):
    '''
    Simulates a set of a tennis match and returns True if player1 wins the set. Player1 is to serve the next game.

    Parameters:
    - p1_serve: the probability that player1 wins a serve point
    - p2_serve: the probability that player2 wins a serve point
    - p1_games: the number of games that player1 has won in this set
    - p2_games: the number of games that player2 has won in this set
    - p1_pts: the number of points player1 has won this game
    - p2_pts: the number of points player2 has won this game
    '''
    player1_games, player2_games = p1_games, p2_games

    if player1_games > 7 or player2_games > 7:
        raise ValueError("Invalid number of current games won passed as parameter")
    
    p1Serving = True
    firstGame = True

    while True:
        if p1Serving:
            if firstGame: # first game in sim, need to account for current points scored in this game
                firstGame = False
                if simulate_game(p1_serve, p1_pts, p2_pts):
                    player1_games += 1
                else:
                    player2_games += 1
            else: # not first game in sim, each player at 0 points
                if simulate_game(p1_serve, 0, 0):
                    player1_games += 1
                else:
                    player2_games += 1
        else: # Player 2 is serving
            if simulate_game(p2_serve, 0, 0):
                player2_games += 1
            else:
                player1_games += 1

        # check for tiebreak
        if player1_games == 6 and player2_games == 6:
            if simulate_set_tiebreak((p1_serve + (1 - p2_serve))/2): # pass the probability of player1 winning any point since tiebreaks are ~ even on serves
                return True
            else: 
                return False
        
        if player1_games >= 6 and player1_games - player2_games > 1:
            return True
        
        if player2_games >= 6 and player2_games - player1_games > 1:
            return False


def simulate_set_tiebreak(p_point: float):
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