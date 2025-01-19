from scrapeEloData import scrape_elo
import pandas as pd
import pickle

class Player:
    def __init__(self, name):
        self.name = name
        self.ratio_data = pd.read_csv('D:/tennisModeling/Modeling-Tennis-with-Markov-Chains/Data/golden_ratio_data.csv')

    def getServePerc(self, surface: str):
        player_data = self.ratio_data[self.ratio_data['Name'] == self.name]
        surface_data = player_data[player_data['Surface'] == surface]
        return surface_data['SPW'].iloc[0]
    
    def getRetPerc(self, surface: str):
        player_data = self.ratio_data[self.ratio_data['Name'] == self.name]
        surface_data = player_data[player_data['Surface'] == surface]
        return surface_data['RPW'].iloc[0]
    
    def getElo(self, surface: str):
        '''
        Returns the elo of the player for the passed surface
        '''
        return scrape_elo(self.name, surface)
    
    def getName(self):
        return self.name
    
    
def p1PtProb(player1: Player, player2: Player, surface: str):
    p1Elo = player1.getElo(surface)
    p2Elo = player2.getElo(surface)

    elo_diff = p1Elo - p2Elo

    # function to determine probability to win a point based off of elo difference
    with open('point_by_elo.pkl', 'rb') as file:
        point_by_elo_func = pickle.load(file)

    # 0.000123 is the ~ percentage increase above 0.5 that 1 elo point has for winning any given point -- see eloReverseEngineer.py
    #perc_increase = elo_diff * 0.00012359619140625 

    #return 0.5 + perc_increase

    return point_by_elo_func(elo_diff)

def p1ServeRatio(player1: Player, player2: Player, surface: str):
    '''
    Returns the ratio at which player 1 wins a service point against player 2
    '''
    return (player1.getServePerc(surface) + (1 - player2.getRetPerc(surface))) / 2

def p1RetRatio(player1: Player, player2: Player, surface: str):
    '''
    Returns the ratio at which player 1 wins a return point against player 2
    '''
    return (player1.getRetPerc(surface) + (1 - player2.getServePerc(surface))) / 2

def p1ActualRetProb(player1: Player, player2: Player, surface: str):
    '''
    Returns the actual probability of player1 winning a return point against player 2 on given surface.
    Incorporates playstyle ratios while restricted to winning any point prob based off of elo
    '''
    prob_win_pt = p1PtProb(player1, player2, surface)

    ratio = p1ServeRatio(player1, player2, surface) / p1RetRatio(player1, player2, surface)

    return round(prob_win_pt/((ratio + 1)/2), 4)

def p1ActualServeProb(player1: Player, player2: Player, surface: str):
    '''
    Returns the actual probability of player1 winning a service point against player 2 on given surface.
    Incorporates playstyle ratios while restricted to winning any point prob based off of elo
    '''   
    ratio = p1ServeRatio(player1, player2, surface) / p1RetRatio(player1, player2, surface)

    return round(ratio * p1ActualRetProb(player1, player2, surface), 4)



def main():
    # test code
    jannik = Player("Jannik Sinner")
    carlos = Player("Carlos Alcaraz")

    print(f"Jannik Sinner probability to win a return point against Carlos Alcaraz on grass: {p1ActualRetProb(jannik, carlos, 'Grass')}")
    print(f"Jannik Sinner probability to win a service point against Carlos Alcaraz on grass: {p1ActualServeProb(jannik, carlos, 'Grass')}")


if __name__ == "__main__":
    main()
