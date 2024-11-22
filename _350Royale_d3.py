from scsa import *
from player import *
from mastermind import *
import itertools
import random

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

"""
Baseline 2
Exhauselively lists all possible combinations of colors of the board length.
After each guess, uses response from it to eliminate all combinations impossible
given the previous guess' result.
"""
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


"""
Inherits matching result  method of Baseline 2 Exhausive solver, 
changes the initial guess list to only permutations of every ordered pair
 of colors
"""
class TwoColorAlternatingSolver(ExhaustiveStrategy):
    def initialize(self):
        colorPairs = list(itertools.permutations(self.colors, 2))
        patterns = []
        for pair in colorPairs:
            pattern = []
            for i in range(self.board_length):
                if i % 2 == 0:
                    pattern.append(pair[0])
                else:
                    pattern.append(pair[1])
            patterns.append(pattern)
        
        self.current_guesses = patterns
        self.current_index = 0


"""
Original 2 Color Alt algorithm
"""
def solveTwoColorAlternating(board_length: int, colors: list[str]):
    # Can be further optimized by taking the previous guess and removing certain colors from previous guess.
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


def solveTwoColors(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])


def solveABColor(board_length: int):
    # Can be further optimized by taking the previous guess and keeping only the indexes where the correct color is in the correct position
    usable_colors = ["A", "B"]
    return itertools.cycle(itertools.product(usable_colors, repeat=board_length))


def solveOnlyOnce(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])


def solveFirstLast(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])


def solveUsuallyFewer(board_length: int, colors: list[str]):
    guess_list = []
    for _ in range(100):
        probability = random.randint(0, 100)
        if probability < 90:
            num_colors = random.randint(2, 3)
            picked_colors = random.sample(colors, k=num_colors)
        else:
            picked_colors = colors
        pattern = random.choices(picked_colors, k=board_length)
        guess_list.append(pattern)
    return itertools.cycle(guess_list)


def solvePreferFewer(board_length: int, colors: list[str]):
    guess_list = []
    for _ in range(100):
        probability = random.randint(0, 100)
        if probability <= 49:
            num_colors = 1
            picked_colors = random.sample(colors, k=num_colors)
        elif probability <= 74:
            num_colors = 2
            picked_colors = random.sample(colors, k=num_colors)
        elif probability <= 87:
            num_colors = min(3, len(colors))
            picked_colors = random.sample(colors, k=num_colors)
        elif probability <= 95:
            num_colors = min(4, len(colors))
            picked_colors = random.sample(colors, k=num_colors)
        elif probability <= 98:
            num_colors = min(5, len(colors))
            picked_colors = random.sample(colors, k=num_colors)
        else:
            picked_colors=colors
        pattern = random.choices(picked_colors, k=board_length)
        guess_list.append(pattern)
    return itertools.cycle(guess_list)



class _350Royale(Player):
    def __init__(self):
        self.player_name = "_350Royale"
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
            
            # Usman Sheikh
            elif scsa_name == "TwoColor":
                self.guess_list = solveTwoColors(board_length, colors)
            
            # Jacob Martin
            elif scsa_name == "ABColor":
                self.guess_list = solveABColor(board_length)
            
            # Henry Tse
            elif scsa_name == "TwoColorAlternating":
                self.use_last_guess = True
                self.solver = TwoColorAlternatingSolver(board_length, colors)
                self.solver.initialize()
                #self.guess_list = solveTwoColorAlternating(board_length, colors)
            
            # Usman Sheikh
            elif scsa_name == "OnlyOnce":
                self.guess_list = solveOnlyOnce(board_length, colors)
            
            # Usman Sheikh
            elif scsa_name == "FirstLast":
                self.guess_list = solveFirstLast(board_length, colors)
            
            # Jacob Martin
            elif scsa_name == "UsuallyFewer":
                # self.guess_list = solveUsuallyFewer(board_length, colors)
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()
            
            # Jacob Martin
            elif scsa_name == "PreferFewer":
                self.guess_list = solvePreferFewer(board_length, colors)

            elif scsa_name == "Mystery1":
                '''
                Mystery 1 seems to favor monochrome codes but has a tendancy to 
                generate some sort of pattern, still not sure what it is
                Seems similar to PreferFewer
                '''
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery2":
                '''
                Essentially, the first 4 colors of the code are generated
                seemingly at random, but then those 4 colors repeat until
                it reaches the lenght of the board
                '''
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery3":
                '''
                Will only use the color A,B,C,F
                Could have a pattern though
                '''
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery4":
                '''
                Strong preference for single color codes
                If there are more than one color, it is either 1 or 2 more colors

                '''
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery5":
                '''
                WIll only use two colors    
                    E.g A and B

                Will start off repeating the two colors in pairs twice
                    BABA

                Then It repeats the pattern in reverse order
                    ABAB

                Finally prints out the second color in the first pair twice
                    AA

                Resulting in the following pattern:
                    BABAABABAA
                    BABA ABAB AA

                Since the example output only is board length 10, the rest of the pattern is assumed to 
                repeat.
                '''
                self.use_last_guess = True
                self.solver = ExhaustiveStrategy(board_length, colors)
                self.solver.initialize()
            
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

"""
Notes for future reference
==========================

Keeping track of the board and color selection size

    Tourys will probably act differently based on the size of the board length and/or the amount
    of possilbe colors. There should be a board length and color check when selecting an SCSA to optimize/maximize
    the number of correct guesses.

    Example:
        TwoColorAlternating is faster under brute force method but
        can only win all 100 rounds given a small board length and color selection.

        When TwoColorAlternating uses elimination from Baseline 2, it is slower but
        is capable of running the max tournament of 100-26 wihtout losing a single round.
 
"""