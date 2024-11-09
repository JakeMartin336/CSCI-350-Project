from scsa import *
from player import *
from mastermind import *
import _350Royale_B1
import itertools


def solveInsertColors():
    None

def solveTwoColors():
    None

def solveABColor():
    None

#Can be further optimized by taking the previous guess and removing certain colors from previous guess.
def solveTwoColorAlternating(board_length: int, colors: list[str]):
    colorPairs = list(itertools.permutations(colors, 2))

    
    guess_list = []
    for pair in colorPairs:
        pattern = []  # Initialize empty list
        for i in range(board_length):
            if i % 2 == 0:
                pattern.append(pair[0])
            else:
                pattern.append(pair[1])
        guess_list.append(pattern)

    return guess_list

def solveOnlyOnce():
    None

def solveFirstLast():
    None

def solveUsuallyFewer():
    None

def solvePreferFewer():
    None

def solveGeneralPurpose():
    None


class TournamentPlayer(Player):
    def __init__(self):
        self.player_name = "Tournament Player"
        self.num_guesses = 0
        self.guess_list = None

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        #[correct color in correct position, correct color wrong position, guesses made]
        last_response: tuple[int, int, int],
    ) -> str:
        # Initialize generator on first guess
        if self.num_guesses == 0 and self.guess_list == None:
            # Henry Tse
            if scsa_name == "InsertColors":
                self.guess_list = solveInsertColors()
            
            # Jacob Martin
            elif scsa_name == "TwoColor":
                self.guess_list = solveTwoColors()
            
             # Jacob Martin
            elif scsa_name == "ABColor":
                self.guess_list = solveABColor()
            
            # Henry Tse
            elif scsa_name == "TwoColorAlternating":
                self.guess_list = itertools.cycle(solveTwoColorAlternating(board_length, colors))
            
            # Usman Sheikh
            elif scsa_name == "OnlyOnce":
                self.guess_list = solveOnlyOnce()
            
            # Usman Sheikh
            elif scsa_name == "FirstLast":
                self.guess_list = solveFirstLast()
            
            # Jacob Martin
            elif scsa_name == "UsuallyFewer":
                self.guess_list = solveUsuallyFewer()
            
            # Usman Sheikh 
            elif scsa_name == "PreferFewer":
                self.guess_list = solvePreferFewer()
            
            # Henry Tse
            else:
                self.guess_list = solveGeneralPurpose()

        # Get next pattern
        make_guess = next(self.guess_list, None)
            
        self.num_guesses += 1
        return ''.join(make_guess)
