
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

def solveTwoColorAlternating():
    None

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
        scsa_name: str,                             #Type of SCSA irrelevant to player
        last_response: tuple[int, int, int],        #No attention paid to responses
    ) -> str:
        
        make_guess = None

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
                self.guess_list = solveTwoColorAlternating()
            
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

            make_guess = ''.join(next(self.guess_list, None))
            self.num_guesses += 1
        
        else:
            make_guess = ''.join(next(self.guess_list, None))
            self.num_guesses += 1
        
        return make_guess
