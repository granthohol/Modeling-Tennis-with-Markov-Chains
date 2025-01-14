### 100 pt difference = 64% chance win best of 3
### 200 pt difference = 76% chance
### 300 pt difference = 85% chance

import random


def simulate_game(p_point: float):
    '''
    Simulates a game of tennis match and returns True if player with passed probability wins the game
    '''
    player_score, opponent_score = 0, 0

    while True:
        if random.random() < p_point: # player wins point
            player_score += 1
        else:
            opponent_score += 1
        
        # check if anyone has won game
        if (player_score >= 4) and (player_score - opponent_score > 1):
            return True
        
        if (opponent_score >= 4) and (opponent_score - player_score > 1):
            return False

def simulate_set(p_point: float):
    '''
    Simulates a set of a tennis match and returns True if player with passed probability wins the set
    '''
    player_games, opponent_games = 0, 0

    while True:
        if simulate_game(p_point):
            player_games += 1
        else:
            opponent_games += 1

        # check for tiebreak
        if player_games == 6 and opponent_games == 6:
            if simulate_set_tiebreak(p_point):
                return True
            else: 
                return False
        
        if player_games >= 6 and player_games - opponent_games > 1:
            return True
        
        if opponent_games >= 6 and opponent_games - player_games > 1:
            return False


def simulate_match(p_point: float, outOf: int):
    '''
    Simulates a tennis match and returns True if player with passed probability wins the match
    '''

    player_sets, opponent_sets = 0, 0

    if outOf == 3:
        games_needed = 2
    elif outOf == 5:
        games_needed = 3
    else:
        raise ValueError("Invalid parameter passed for number of sets the match is out of")

    while True:
        if simulate_set(p_point):
            player_sets += 1
        else:
            opponent_sets += 1
        
        if player_sets == games_needed:
            return True
        if opponent_sets == games_needed:
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
        
def find_point_probability(target_match_probability, tolerance=0.0001, simulations = 50000):
    """
    Uses a binary search to estimate the point probability that results in the target match probability.
    """
    low, high = 0.5, 1.0  # Point probabilities range from 0.5 to 1.0 (fair to dominant player)

    while high - low > tolerance:
        mid = (low + high) / 2
        match_wins = sum(simulate_match(mid, 3) for _ in range(simulations))
        match_probability = match_wins / simulations

        if match_probability < target_match_probability:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def main():

    fivehun = find_point_probability(0.95)
    fourhun = find_point_probability(0.91)
    threehun = find_point_probability(0.85)
    twohun = find_point_probability(0.76)
    hun = find_point_probability(0.64)

    print(((fivehun - fourhun) + (fourhun - threehun) + (threehun - twohun) + (twohun - hun) + (hun-0.5))/5)

if __name__ == "__main__":
    main()