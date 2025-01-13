from simInputs import Player

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
    '''