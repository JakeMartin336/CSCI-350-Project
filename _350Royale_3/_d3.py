from scsa import *
from player import *
from mastermind import *
import itertools


def solveInsertColors(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])

def solveTwoColors(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])

def solveABColor(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])

#Can be further optimized by taking the previous guess and removing certain colors from previous guess.
def solveTwoColorAlternating(board_length: int, colors: list[str]):
    colorPairs = list(itertools.permutations(colors, 2))
    patterns = []
    for pair in colorPairs:
        pattern = []
        for i in range(board_length):
            if i % 2 == 0:
                pattern.append(pair[0])
            else:
                pattern.append(pair[1])
        patterns.append(pattern)
    return itertools.cycle(patterns)

def solveOnlyOnce(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])

def solveFirstLast(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])

def solveUsuallyFewer(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])

def solvePreferFewer(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])

def solveGeneralPurpose(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])


class _350Royale(Player):
    def __init__(self):
        self.player_name = "_350Royale"
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
                self.guess_list = solveInsertColors(board_length, colors)
            
            # Jacob Martin
            elif scsa_name == "TwoColor":
                self.guess_list = solveTwoColors(board_length, colors)
            
             # Jacob Martin
            elif scsa_name == "ABColor":
                self.guess_list = solveABColor(board_length, colors)
            
            # Henry Tse
            elif scsa_name == "TwoColorAlternating":
                self.guess_list = solveTwoColorAlternating(board_length, colors)
            
            # Usman Sheikh
            elif scsa_name == "OnlyOnce":
                self.guess_list = solveOnlyOnce(board_length, colors)
            
            # Usman Sheikh
            elif scsa_name == "FirstLast":
                self.guess_list = solveFirstLast(board_length, colors)
            
            # Jacob Martin
            elif scsa_name == "UsuallyFewer":
                self.guess_list = solveUsuallyFewer(board_length, colors)
            
            # Usman Sheikh 
            elif scsa_name == "PreferFewer":
                self.guess_list = solvePreferFewer(board_length, colors)
            
            # Henry Tse
            else:
                self.guess_list = solveGeneralPurpose(board_length, colors)

        # Get next pattern
        make_guess = next(self.guess_list, None)
            
        self.num_guesses += 1
        return ''.join(make_guess)
