from scsa import *
from player import *
from mastermind import *
import itertools

class Solver:
    """Base class for different solving strategies"""
    def __init__(self, board_length, colors):
        self.board_length = board_length
        self.colors = colors
        self.current_guesses = []
        self.last_guess = None
    
    def initialize(self):
        """Initialize the strategy's guess list"""
        raise NotImplementedError
    
    def filter_guesses(self, last_response):
        """Filter guesses based on last response"""
        raise NotImplementedError
    
    def get_next_guess(self):
        """Get the next guess from the strategy"""
        raise NotImplementedError

class ExhaustiveStrategy(Solver):
    """Baseline 2"""
    def matches_response(self, candidate: list, last_guess: list, correct_pos: int, correct_color: int) -> bool:
        # Count exact matches
        exact = sum(1 for i in range(len(candidate)) if candidate[i] == last_guess[i])
        # Count color matches
        color_matches = sum(min(candidate.count(c), last_guess.count(c)) for c in set(candidate))
        
        return exact == correct_pos and (color_matches - exact) == correct_color
    
    def initialize(self):
        self.current_guesses = list(itertools.product(self.colors, repeat=self.board_length))
        self.current_index = 0
    
    def filter_guesses(self, last_response):
        if self.last_guess is not None:
            last_guess_list = list(self.last_guess)
            self.current_guesses = [
                guess for guess in self.current_guesses 
                if self.matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
            ]
            self.current_index = 0
    
    def get_next_guess(self):
        if self.current_index >= len(self.current_guesses):
            return self.colors[0] * self.board_length
        
        guess = ''.join(self.current_guesses[self.current_index])
        self.last_guess = guess
        self.current_index += 1
        return guess
    
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

    return itertools.cycle(guess_list)

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
        self.use_last_guess = False
        self.solver = None

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        #[correct color in correct position, correct color wrong position, guesses made]
        last_response: tuple[int, int, int],
    ) -> str:
        # Initialize generator on first guess
        if last_response[2] == 0:
            # Henry Tse
            if scsa_name == "InsertColors":
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()
            
            # Jacob Martin
            elif scsa_name == "TwoColor":
                self.guess_list = solveTwoColors()
            
             # Jacob Martin
            elif scsa_name == "ABColor":
                self.guess_list = solveABColor()
            
            # Henry Tse
            elif scsa_name == "TwoColorAlternating":
                self.guess_list = solveTwoColorAlternating(board_length, colors)
            
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
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()
        
        elif self.use_last_guess:
            self.solver.filter_guesses(last_response)

        # Get next pattern
        if not self.use_last_guess:
            make_guess = next(self.guess_list, None)
                
            self.num_guesses += 1
            return ''.join(make_guess)
        
        else:
            guess = self.solver.get_next_guess()
            self.num_guesses += 1
            return guess
