from scsa import *
from player import *
from mastermind import *
import itertools
import random
import time

"""
Base class for different solving strategies
"""
class Solver:
    def __init__(self, board_length, colors):
        self.board_length = board_length
        self.colors = colors
        self.current_guesses = []
        self.last_guess = None
        self.start_time = None
        self.time_limit = 4.9
    
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
        """Check if exceeding time limit"""
        if self.start_time is None:
            self.start_time = time.time()
        return (time.time() - self.start_time) <= self.time_limit


#BASELINE STRATEGIES
"""
Baseline 2
Exhauselively lists all possible combinations of colors of the board length.
After each guess, uses response from it to eliminate all combinations impossible
given the previous guess' result.
"""
class ExhaustiveStrategy(Solver):
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

#GENERAL STRATEGIES
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
RandomSolver
Randomly generates possible combinations of the colors that were counted in the counting phase
before exhaustive elimination
"""
class RandomSolver(HybridStrategy):
    def __init__(self, board_length, colors):
        super().__init__(board_length, colors)

    def generate_combinations(self, color_counts):
        if not self.check_time():
            return [self.colors[0] * self.board_length]
        
        elements = []
        for color, count in color_counts.items():
            elements.extend([color] * count)
            
        combinations = set()  # Use set to avoid duplicates
        max_iterations = min(100000, len(self.colors) ** self.board_length)  # Maximum number of random combinations to try

        #elapsed_time = time.time() - self.start_time
        #print(f"Time {elapsed_time:.2f}s: Max iterations: {max_iterations}")

        for _ in range(max_iterations):
            if not self.check_time():
                if not combinations:  # If we haven't found any combinations yet
                    return [self.colors[0] * self.board_length]
                break
                
            # Generate a random permutation
            perm = list(elements)
            random.shuffle(perm)
            combinations.add(''.join(perm))
            
        return list(combinations)



#SCSA SPECIFIC STRATEGIES
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

    def matches_response(self, candidate: list, last_guess: list, correct_pos: int, correct_color: int) -> bool:
        # Get the first two colors from candidate and guess (which define the pattern)
        candidate_pattern = candidate[:2]
        guess_pattern = last_guess[:2]
        
        # If response is (0,0), eliminate candidates that share any colors
        if correct_pos == 0 and correct_color == 0:
            return len(set(candidate_pattern) & set(guess_pattern)) == 0
        
        # Count exact matches just for the pattern (first two positions)
        pattern_matches = sum(1 for i in range(2) if candidate_pattern[i] == guess_pattern[i])
        
        # If the pattern matches, all even positions will match and all odd positions will match
        # So we can multiply pattern_matches by (board_length // 2) to get total matches
        total_exact_matches = pattern_matches * (len(candidate) // 2)
        if len(candidate) % 2 == 1 and pattern_matches > 0:  # Handle odd length boards
            total_exact_matches += (candidate[-1] == last_guess[-1])
            
        return total_exact_matches == correct_pos

"""
Solves for ABColor
Uses only the colors A and B before exhaustive elimination
"""
class ABColorSolver(ExhaustiveStrategy):
    def initialize(self):
        usable_colors = ["A", "B"]
        self.current_guesses = list(itertools.product(usable_colors, repeat=self.board_length))
        self.current_index = 0

"""
Solves for TwoColor
Uses all possible combinations of two colors before exhaustive elimination
"""
class TwoColorSolver(ExhaustiveStrategy):
    def __init__(self, board_length, colors):
        super().__init__(board_length, colors)

    def initialize(self):
        """Initialize with all possible combinations using exactly two colors"""
        result = []
        # Get all combinations of two colors
        color_pairs = itertools.combinations(self.colors, 2)
        for pair in color_pairs:
            # Generate all tuples with the two colors in each combination
            tuples = itertools.product(pair, repeat=self.board_length)
            result.extend(tuples)
        
        self.current_guesses = [''.join(guess) for guess in result]
        self.current_index = 0
        self.last_guess = None

    def filter_guesses(self, last_response):
        """Filter guesses based on last response"""
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
        
        if not self.current_guesses or self.current_index >= len(self.current_guesses):
            return self.colors[0] * self.board_length
        
        guess = self.current_guesses[self.current_index]
        self.last_guess = guess
        self.current_index += 1
        return guess

"""
Solves for OnlyOnce
Uses only the color A before exhaustive elimination
"""
class OnlyOnceSolver(ExhaustiveStrategy):
    def __init__(self, board_length, colors):
        super().__init__(board_length, colors)
        self.correctA = None
        self.first_phase = True

    def initialize(self):
        # First guess is all 'A's to count how many A's in solution
        self.current_guesses = ['A' * self.board_length]
        self.current_index = 0
        self.last_guess = None

    def filter_guesses(self, last_response):
        if self.last_guess is None:
            return

        # Phase 1: After first all-A guess, determine number of A's
        if self.first_phase:
            self.correctA = last_response[0]
            self.first_phase = False
            
            # Generate all possible permutations using exactly board_length colors
            # Each color appears exactly once
            self.current_guesses = [
                ''.join(p) for p in itertools.permutations(self.colors, self.board_length)
                if p.count('A') == self.correctA  # Only keep guesses with correct number of A's
            ]
            
            self.current_index = 0
            return

        # Standard filtering based on response
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
        
        if not self.current_guesses or self.current_index >= len(self.current_guesses):
            return self.colors[0] * self.board_length
        
        guess = self.current_guesses[self.current_index]
        self.last_guess = guess
        self.current_index += 1
        return guess

"""
Solves for FirstLast
Uses only the first and last color before exhaustive elimination
"""
class FirstLastSolver(ExhaustiveStrategy):
    def __init__(self, board_length, colors):
        super().__init__(board_length, colors)

    def initialize(self):
        """Initialize with patterns matching FirstLast's structure"""
        result = []
        # For each possible first/last color
        for color in self.colors:
            # Generate all combinations for the middle elements
            middle_combinations = itertools.product(self.colors, repeat=(self.board_length-2))
            for middle in middle_combinations:
                # Create pattern with same first/last color
                result.append((color,) + middle + (color,))

        self.current_guesses = [''.join(guess) for guess in result]
        self.current_index = 0
        self.last_guess = None

    def filter_guesses(self, last_response):
        """Filter guesses based on last response"""
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
        
        if not self.current_guesses or self.current_index >= len(self.current_guesses):
            return self.colors[0] * self.board_length
        
        guess = self.current_guesses[self.current_index]
        self.last_guess = guess
        self.current_index += 1
        return guess



#MYSTERY SCSA SPECIFIC STRATEGIES
"""
Solves for Mystery2 SCSAs based on the following analysis:
    The first 4 colors of the code are generated
    seemingly at random, but then those 4 colors repeat until
    it reaches the length of the board
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

"""
Solves for Mystery5 according to the following analysis:
    Will only use two colors: E.g A and B
    Will start off repeating the two colors in pairs twice: BABA
    Then It repeats the pattern in reverse order: ABAB
    Finally prints out the second color in the first pair twice: AA
    Resulting in the following pattern:
        BABAABABAA
        BABA ABAB AA
    Since the example output only is board length 10, the rest of the pattern is assumed to 
    repeat.
"""
class Mystery5Solver(ExhaustiveStrategy):
    def initialize(self):
        """Initialize with patterns matching Mystery5's structure"""
        # Will only generate patterns using two colors in the specific sequence:
        # BABA ABAB AA + repeat
        
        patterns = []
        # Try each possible pair of colors
        for color1, color2 in itertools.permutations(self.colors, 2):
            # Build the base pattern: BABAABABAA
            base_pattern = []
            
            # First part: BABA (alternating starting with first color)
            base_pattern.extend([color1, color2, color1, color2])
            
            # Second part: ABAB (alternating starting with second color)
            base_pattern.extend([color2, color1, color2, color1])
            
            # Third part: AA (two of the first color)
            base_pattern.extend([color1, color1])
            
            # If board length > 10, repeat the pattern
            full_pattern = []
            while len(full_pattern) < self.board_length:
                remaining = self.board_length - len(full_pattern)
                # Add as much of the pattern as will fit
                full_pattern.extend(base_pattern[:remaining])
            
            patterns.append(''.join(full_pattern))
        
        self.current_guesses = patterns
        self.current_index = 0
    
    def filter_guesses(self, last_response):
        """Filter guesses based on last response"""
        if self.last_guess is not None:
            last_guess_list = list(self.last_guess)
            self.current_guesses = [
                guess for guess in self.current_guesses 
                if self.matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
            ]
            self.current_index = 0



#PLAYER
"""
Main Player class for _350Royale
Will select solver based on the SCSAs name
"""
class _350Royale(Player):
    def __init__(self):
        self.player_name = "_350Royale"
        self.num_guesses = 0
        self.guess_list = None
        self.solver = None

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:
        
        # Initialize generator on first guess
        if last_response[2] == 0:

            if scsa_name == "InsertColors":
                self.solver = RandomSolver(board_length, colors)
            
            elif scsa_name == "TwoColor":
                if board_length > 12 or len(colors) > 10:
                    self.solver = HybridStrategy(board_length, colors)
                else:
                    self.solver = TwoColorSolver(board_length, colors)
            
            elif scsa_name == "ABColor":
                if board_length > 14:
                    self.solver = HybridStrategy(board_length, colors)
                else:
                    self.solver = ABColorSolver(board_length, colors)
                
            elif scsa_name == "TwoColorAlternating":
                self.solver = TwoColorAlternatingSolver(board_length, colors)
            
            elif scsa_name == "OnlyOnce":
                if board_length > 7 or len(colors) > 9:
                    self.solver = HybridStrategy(board_length, colors)
                else:
                    self.solver = OnlyOnceSolver(board_length, colors)
            
            elif scsa_name == "FirstLast":
                if board_length > 7 or len(colors) > 9:
                    self.solver = HybridStrategy(board_length, colors)
                else:
                    self.solver = FirstLastSolver(board_length, colors)
            
            elif scsa_name == "UsuallyFewer":
                self.solver = HybridStrategy(board_length, colors)            

            elif scsa_name == "PreferFewer":
                self.solver = HybridStrategy(board_length, colors)

            elif scsa_name == "Mystery1":
                self.solver = HybridStrategy(board_length, colors)

            elif scsa_name == "Mystery2":
                self.solver = Mystery2Solver(board_length, colors)

            elif scsa_name == "Mystery3":
                self.solver = HybridStrategy(board_length, colors)

            elif scsa_name == "Mystery4":
                self.solver = HybridStrategy(board_length, colors)

            elif scsa_name == "Mystery5":      
                self.solver = Mystery5Solver(board_length, colors)
            
            #Default to RandomSolver if SCSAs name is not recognized
            else:
                self.solver = RandomSolver(board_length, colors)
            
            self.solver.initialize()
        
        else:
            self.solver.filter_guesses(last_response)

        guess = self.solver.get_next_guess()
        self.num_guesses += 1
        return guess