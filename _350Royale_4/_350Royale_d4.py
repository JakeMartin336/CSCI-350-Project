from scsa import *
from player import *
from mastermind import *
import itertools
import random
import time

class Solver:
    """Base class for different solving strategies"""
    def __init__(self, board_length, colors):
        self.board_length = board_length
        self.colors = colors
        self.current_guesses = []
        self.last_guess = None
        self.start_time = None
        self.time_limit = 4.9  # Slightly under 5 seconds to allow for overhead
    
    def initialize(self):
        """Initialize the strategy's guess list"""
        raise NotImplementedError
    
    def filter_guesses(self, last_response):
        """Filter guesses based on last response"""
        raise NotImplementedError
    
    def get_next_guess(self):
        """Get the next guess from the strategy"""
        raise NotImplementedError
        
    def check_time(self):
        """Check if we've exceeded time limit"""
        if self.start_time is None:
            self.start_time = time.time()
        return (time.time() - self.start_time) <= self.time_limit

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
Baseline 3
Counts the number of times each color appears in the code
and then generates all possible combinations of the colors
that could be in the code
"""   
class CountingStrategy(Solver):
    def __init__(self, board_length, colors):
        super().__init__(board_length, colors)
        self.color_counts = {}
        self.counting_phase = True
        self.current_index = 0
        self.current_guesses = []

    def generate_combinations(self, color_counts):
        elements = []
        for color, count in color_counts.items():
            elements.extend([color] * count)
        return list(set(itertools.permutations(elements)))

    def initialize(self):
        # Initialize with monochrome guesses for all colors except the last
        self.current_guesses = []
        for color in self.colors[:-1]:
            self.current_guesses.append(color * self.board_length)
        self.current_index = 0
        self.color_counts = {}
        self.counting_phase = True

    def filter_guesses(self, last_response):
        if self.last_guess is not None and self.counting_phase:
            total_matches = last_response[0] + last_response[1]
            color = self.last_guess[0]
            self.color_counts[color] = total_matches
            
            if len(self.color_counts) == len(self.colors) - 1:
                # Deduce last color count
                known_sum = sum(self.color_counts.values())
                last_color = self.colors[-1]
                self.color_counts[last_color] = self.board_length - known_sum
                
                # Generate new guess list based on color counts
                self.current_guesses = [''.join(p) for p in self.generate_combinations(self.color_counts)]
                self.current_index = 0
                self.counting_phase = False

    def get_next_guess(self):
        if self.current_index >= len(self.current_guesses):
            return self.colors[0] * self.board_length
        
        guess = self.current_guesses[self.current_index]
        self.last_guess = guess
        self.current_index += 1
        return guess

"""
Hybrid Strategy
Combines CountingStrategy's color counting with ExhaustiveStrategy's elimination (Baseline 2 + 3 combined)
"""
class HybridStrategy(Solver):
    def __init__(self, board_length, colors):
        super().__init__(board_length, colors)
        self.color_counts = {}
        self.counting_phase = True
        self.current_index = 0

    def matches_response(self, candidate: list, last_guess: list, correct_pos: int, correct_color: int) -> bool:
        # Count exact matches
        exact = sum(1 for i in range(len(candidate)) if candidate[i] == last_guess[i])
        # Count color matches
        color_matches = sum(min(candidate.count(c), last_guess.count(c)) for c in set(candidate))
        
        return exact == correct_pos and (color_matches - exact) == correct_color

    def generate_combinations(self, color_counts):
        if not self.check_time():
            return [self.colors[0] * self.board_length]
        
        elements = []
        for color, count in color_counts.items():
            elements.extend([color] * count)
        
        # Get permutations iterator instead of generating all at once
        perms = itertools.permutations(elements)
        combinations = []
        max_combinations = 100000  # Limit number of combinations to prevent excessive processing
        
        # Take permutations until time runs out or max limit reached
        for i, p in enumerate(perms):
            if not self.check_time() or i >= max_combinations:
                if not combinations:  # If we haven't found any combinations yet
                    return [self.colors[0] * self.board_length]
                break
            combinations.append(''.join(p))
        
        return list(set(combinations))  # Remove duplicates

    def initialize(self):
        # Start with counting phase - monochrome guesses
        self.current_guesses = []
        for color in self.colors[:-1]:
            self.current_guesses.append(color * self.board_length)
            if not self.check_time():
                break
        self.current_index = 0
        self.color_counts = {}
        self.counting_phase = True

    def filter_guesses(self, last_response):
        
        if self.counting_phase:
            if self.last_guess is not None:
                total_matches = last_response[0] + last_response[1]
                color = self.last_guess[0]
                self.color_counts[color] = total_matches
                
                if len(self.color_counts) == len(self.colors) - 1:
                    # Deduce last color count
                    known_sum = sum(self.color_counts.values())
                    last_color = self.colors[-1]
                    self.color_counts[last_color] = self.board_length - known_sum
                    # Generate initial guess list based on color counts
                    self.current_guesses = self.generate_combinations(self.color_counts)
                    self.current_index = 0
                    self.counting_phase = False
        else:
            
            # Use exhaustive elimination on the remaining guesses
            if self.last_guess is not None:
                last_guess_list = list(self.last_guess)
                self.current_guesses = [
                    guess for guess in self.current_guesses 
                    if self.matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
                ]
                self.current_index = 0

    def get_next_guess(self):
        if not self.check_time():
            return self.colors[0] * self.board_length
        
        if self.current_index >= len(self.current_guesses):
            return self.colors[0] * self.board_length
        
        guess = self.current_guesses[self.current_index]
        self.last_guess = guess
        self.current_index += 1
        return guess



"""
Solves for TwoColorAlternating
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
Solves for Mystery2 SCSAs based on the following analysis:
Essentially, the first 4 colors of the code are generated
seemingly at random, but then those 4 colors repeat until
it reaches the lenght of the board
"""
class Mystery2Solver(HybridStrategy):
    def initialize(self):
        # Start with counting phase - monochrome guesses
        self.current_guesses = []
        for color in self.colors:  # Try all colors since we don't know which 4 are used
            self.current_guesses.append(color * self.board_length)
        self.current_index = 0
        self.color_counts = {}
        self.counting_phase = True

    def filter_guesses(self, last_response):
        if self.counting_phase:
            if self.last_guess is not None:
                total_matches = last_response[0] + last_response[1]
                if total_matches > 0:  # Only store colors that are actually used
                    color = self.last_guess[0]
                    self.color_counts[color] = total_matches
                
                # If we've found exactly 4 colors with matches, we can stop counting
                if sum(count > 0 for count in self.color_counts.values()) == 4:
                    # Generate all possible 4-color permutations from the used colors
                    used_colors = list(self.color_counts.keys())
                    four_color_perms = list(itertools.permutations(used_colors, 4))
                    
                    # For each permutation, create the full pattern by repeating it
                    patterns = []
                    for perm in four_color_perms:
                        pattern = list(perm)
                        while len(pattern) < self.board_length:
                            next_pos = len(pattern)
                            pattern.append(perm[next_pos % 4])
                        patterns.append(''.join(pattern))
                    
                    self.current_guesses = patterns
                    self.current_index = 0
                    self.counting_phase = False
        else:
            # Use exhaustive elimination on the remaining guesses
            if self.last_guess is not None:
                last_guess_list = list(self.last_guess)
                self.current_guesses = [
                    guess for guess in self.current_guesses 
                    if self.matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
                ]
                self.current_index = 0


class ABColorSolver(ExhaustiveStrategy):
    def initialize(self):
        usable_colors = ["A", "B"]
        self.current_guesses = list(itertools.product(usable_colors, repeat=self.board_length))
        self.current_index = 0


def solveTwoColors(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])
    

def solveOnlyOnce(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])


def solveFirstLast(board_length: int, colors: list[str]):
    pattern = [colors[0]] * board_length
    return itertools.cycle([pattern])



"""
Player class for _350Royale
Will select solver based on the SCSAs name
"""
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
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()
            
            # Usman Sheikh
            elif scsa_name == "TwoColor":
                self.guess_list = solveTwoColors(board_length, colors)
            
            # Jacob Martin
            elif scsa_name == "ABColor":
                self.use_last_guess = True
                self.solver = ABColorSolver(board_length, colors)
                self.solver.initialize()
                
            # Henry Tse
            elif scsa_name == "TwoColorAlternating":
                self.use_last_guess = True
                self.solver = TwoColorAlternatingSolver(board_length, colors)
                self.solver.initialize()
                #self.guess_list = solveTwoColorAlternating(board_length, colors)
            
            # Usman Sheikh
            elif scsa_name == "OnlyOnce":
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()
            
            # Usman Sheikh
            elif scsa_name == "FirstLast":
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()
            
            # Jacob Martin
            elif scsa_name == "UsuallyFewer":
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()
            
            # Jacob Martin
            elif scsa_name == "PreferFewer":
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery1":
                '''
                Mystery 1 seems to favor monochrome codes but has a tendancy to 
                generate some sort of pattern, still not sure what it is
                Seems similar to PreferFewer
                '''
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery2":
                '''
                Essentially, the first 4 colors of the code are generated
                seemingly at random, but then those 4 colors repeat until
                it reaches the length of the board
                '''
                self.use_last_guess = True
                self.solver = Mystery2Solver(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery3":
                '''
                Will only use the color A,B,C,F
                Could have a pattern though
                '''
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()

            elif scsa_name == "Mystery4":
                '''
                Strong preference for single color codes
                If there are more than one color, it is either 1 or 2 more colors

                '''
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
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
                self.solver = HybridStrategy(board_length, colors)
                self.solver.initialize()
            
            # Henry Tse
            else:
                self.use_last_guess = True
                self.solver = HybridStrategy(board_length, colors)
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
