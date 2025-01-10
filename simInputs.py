from scrapeEloData import scrape_elo
from serveToReturnRatio import getServe, getReturn
import pandas as pd

class Player:
    def __init__(self, name):
        self.name = name

    def getServePerc(self, surface: str):
        return getServe(self.name, surface)
    
    def getRetPerc(self, surface: str):
        return getReturn(self.name, surface)
    
    def getElo(self, surface: str):
        '''
        Returns the elo of the player for the passed surface
        '''
        return scrape_elo(self.name, surface)
    
def p1PtProb(player1: Player, player2: Player, surface: str):
    p1Elo = player1.getElo(surface)
    p2Elo = player2.getElo(surface)

    elo_diff = p1Elo - p2Elo

    # 0.000123 is the ~ percentage increase above 0.5 that 1 elo point has for winning any given point -- see eloReverseEngineer.py
    perc_increase = elo_diff * 0.000123 

    return 0.5 + perc_increase

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
    prob_win_pt = p1ServeRatio(player1, player2, surface)

    ratio = p1ServeRatio(player1, player2, surface) / p1RetRatio(player1, player2, surface)

    return prob_win_pt/((ratio + 1)/2)

def p1ActualServeProb(player1: Player, player2: Player, surface: str):
    '''
    Returns the actual probability of player1 winning a service point against player 2 on given surface.
    Incorporates playstyle ratios while restricted to winning any point prob based off of elo
    '''   
    ratio = p1ServeRatio(player1, player2, surface) / p1RetRatio(player1, player2, surface)

    return ratio * p1ActualRetProb(player1, player2, surface)



def main():
    jannik = Player("Jannik Sinner")
    carlos = Player("Carlos Alcaraz")


if __name__ == "__main__":
    main()
