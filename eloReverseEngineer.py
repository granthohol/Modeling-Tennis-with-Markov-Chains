### 100 pt difference = 64% chance win best of 3
### 200 pt difference = 76% chance
### 300 pt difference = 85% chance

import random
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import pickle


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
        
def find_point_probability(target_match_probability, best_out_of, tolerance=0.001, simulations = 10000):
    """
    Uses a binary search to estimate the point probability that results in the target match probability.
    """
    low, high = 0.5, 1.0  # Point probabilities range from 0.5 to 1.0 (fair to dominant player)

    while high - low > tolerance:
        mid = (low + high) / 2
        match_wins = sum(simulate_match(mid, best_out_of) for _ in range(simulations))
        match_probability = match_wins / simulations

        if match_probability < target_match_probability:
            low = mid
        else:
            high = mid

    return (low + high) / 2

def fiveOdds(p3):
    '''
    Method to determine odds to win a best of 5 set match from the odds to win a best of 3
    '''
    p1 = np.roots([-2, 3, 0, -1*p3])[1]
    p5 = (p1**3)*(4 - 3*p1 + (6*(1-p1)*(1-p1)))
    return p5    


def main():
    points5 = [[0, 0.5], [100, fiveOdds(0.64)], [200, fiveOdds(0.76)], [300, fiveOdds(0.85)], [400, fiveOdds(0.91)], [500, fiveOdds(0.95)]]

    x5, y5 = zip(*points5)

    fiveSetFunc = CubicSpline(x5, y5) # determines winning percentage on 5 set matches from elo difference

    points3 = [[0, 0.5], [100, 0.64], [200, 0.76], [300, 0.85], [400, 0.91], [500, 0.95]] 

    x3, y3 = zip(*points3)

    threeSetFunc = CubicSpline(x3, y3) # determines winning percentage on 3 set matches from elo difference  

    point_probs = []
    for i in range(1, 501):
        point_prob = find_point_probability(fiveSetFunc(i), 5)
        point_prob2 = find_point_probability(threeSetFunc(i), 3)
        avg = (point_prob + point_prob2)/2
        point_probs.append([i, avg])


    x, y = zip(*point_probs)

    cs = CubicSpline(x, y)

     # save the function to a file
    with open('point_prob_by_elo.pkl', 'wb') as file:
        pickle.dump(cs, file)  



    # Generate a range of x values for a smooth curve
    x_smooth = np.linspace(min(x), max(x), 500)

    # Evaluate the cubic spline at these x values
    y_smooth = cs(x_smooth)

    # Plot the original points
    plt.scatter(x, y, color='red', label='Original Points')

    # Plot the cubic spline curve
    plt.plot(x_smooth, y_smooth, label='Cubic Spline', color='blue')

    # Add labels and legend
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Cubic Spline Interpolation')
    plt.legend()

    # Show the plot
    plt.grid()
    plt.show() 

if __name__ == "__main__":
    main()