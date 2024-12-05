import argparse
from scsa import *
from player import *
from mastermind import *
import time
import itertools

class Baseline2(Player):
    def __init__(self):
        self.player_name = "Baseline2"
        self.guess_list = None
        self.current_index = 0
        self.last_guess = None
        self.OnlyOnceCounter = 0 
        self.switch_half = False
        self.correctA = 0


    def OnlyOnceSolver2( #could be optimized a bit more in the second half. I think any sort of failure that takes place is due to that 
            self,
            board_length: int,
            colors: list[str],
            scsa_name: str,
            #[correct color in correct position, correct color in wrong position, guesses made]
            last_response: tuple[int, int, int],     
        ) -> str:

        if last_response[2] == 0:  # guesses made is 0
            return "A"*board_length
        if last_response[2] == 1:
            #number of A's in the final response 
            self.correctA = last_response[0]
            print("Number of A's in the final answer:", self.correctA)

            # Generate all permutations of the letters
            permutations = list(itertools.permutations(colors))

            # Append 'AA' to each permutation and format them as strings
            self.guess_list = [''.join(p) + ('A'*(board_length-len(colors))) for p in permutations]
            print(self.guess_list)
        

        if last_response[0] == (self.correctA + len(colors)-1) and self.switch_half == False:
            print("Last Response was the correct first half")
            #need to generate a new search space based on the last response
            #need to create all random letters after the unique letters in the last response 
            print(self.guess_list[self.current_index-1])
            base = self.guess_list[self.current_index-1][:len(colors)] #this is the correct sequence of the unique letters
            combinations = itertools.product(colors, repeat=(board_length-len(colors)))
            self.guess_list = [base + ''.join(combo) for combo in combinations] #this is the refined search space
            self.switch_half = True
            return self.guess_list[1]
        
        if self.switch_half:
            if self.last_guess is not None:
                last_guess_list = list(self.last_guess)
                
                self.guess_list = [
                    guess for guess in self.guess_list 
                    if self._matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
                ]
                self.current_index = 0  # Reset index after filtering


                

        guess = ''.join(self.guess_list[self.current_index%len(self.guess_list)]) 
        self.current_index +=1
        return guess




        
        
        

            
        

    def OnlyOnceSolver( #could be optimized a bit more in the second half. I think any sort of failure that takes place is due to that 
            self,
            board_length: int,
            colors: list[str],
            scsa_name: str,
            #[correct color in correct position, correct color in wrong position, guesses made]
            last_response: tuple[int, int, int],     
        ) -> str:
        
        if last_response[2] == 0:  # guesses made is 0

            if board_length<=len(colors): #if the number of colors is less than the size of the board, then the guess list is all individual combos 
                self.guess_list = list(itertools.permutations(colors, board_length))
                self.switch_half = True
                

            else: #else the guess list is [Ax(#number of colors), all combos possible in remaining positions] -- board length 3 - colors 2 == [('A', 'A', 'A'), ('A', 'A', 'B')]
                combinations = itertools.product(colors, repeat=(board_length-len(colors)))

                # Add ('A', 'A', 'A') as the first x elements for each combination
                self.guess_list = [('A',)*len(colors) + comb for comb in combinations]
                # print(self.guess_list)
                self.current_index = len(self.guess_list)-1


            # This uses the fact that for the first len(colors) elements there will be different letters
            # By setting the first len(color) elements to A we know there would always be at least 1 color in the correct place 
            # The goal is to figure out the last board_length - len(color) elements first and then there should be very limited options to choose from after that 
            # so far I think matches response is the best way to choose those last few elements 
        
            



        if self.switch_half == False and last_response[0]==(board_length-len(colors)+1): #at this point the elements from [len(color):] are in place; can now shift focus to [0:len(color)]
            print(self.last_guess)
            list1 = itertools.permutations(colors, (len(colors)))
            print(len(self.last_guess))
            print(board_length)
            print(len(colors))
            lastFew = self.last_guess[len(colors)-board_length:]

            self.guess_list = []
            for listt in list1:
                self.guess_list.append(list(listt) + list(lastFew))
            self.current_index = len(self.guess_list)-1
            # print(self.guess_list)
            self.switch_half = True
            print("reached")

        # this is where the switch comes into play 
        # The algo has figured out the last random elements, now it has to figure out the elements that are all different from each other 


        
        guess = ''.join(self.guess_list[self.current_index])
        self.current_index -= 1
        self.last_guess = guess
        print(guess)

        return guess
    

    def TwoColorSolver( #could be optimized a bit more in the second half. I think any sort of failure that takes place is due to that 
            self,
            board_length: int,
            colors: list[str],
            scsa_name: str,
            #[correct color in correct position, correct color in wrong position, guesses made]
            last_response: tuple[int, int, int],     
        ) -> str:

        if last_response[2] == 0:  # guesses made is 0
            result = []
            # Get all combinations of two colors
            color_pairs = itertools.combinations(colors, 2)
            for pair in color_pairs:
                # Generate all tuples with the two colors in each combination
                tuples = itertools.product(pair, repeat=board_length)
                result.extend(tuples)
            self.guess_list = list(result)
            # self.guess_list = list(itertools.product(colors, repeat=len(colors))
            # print(self.guess_list)
            self.current_index = 0
            self.last_guess = None

        if self.last_guess is not None:
            last_guess_list = list(self.last_guess)
            
            self.guess_list = [
                guess for guess in self.guess_list 
                if self._matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
            ]
            self.current_index = 0  # Reset index after filtering

        
        guess = ''.join(self.guess_list[self.current_index])
        self.last_guess = guess
        self.current_index += 1
        return guess
        # I cannot think of further ways on how to prune this search space aside from figuring out what the two colors in question are 
        # to my knowledge I think matches response does this already, so I generated a smaller search space that just follows the rules of what type of codes TwoColor creates 
    


    def FirstLastSolver( #could be optimized a bit more in the second half. I think any sort of failure that takes place is due to that 
            self,
            board_length: int,
            colors: list[str],
            scsa_name: str,
            #[correct color in correct position, correct color in wrong position, guesses made]
            last_response: tuple[int, int, int],     
        ) -> str:


        if last_response[2] == 0:  # guesses made is 0
            result = []
            # Generate all combinations for the middle elements
            for color in colors:
                # Fix the first and last color
                middle_combinations = itertools.product(colors, repeat=(board_length-2))
                for middle in middle_combinations:
                    result.append((color, *middle, color))


            self.guess_list = list(result)
            # print(self.guess_list)

            # self.guess_list = list(itertools.product(colors, repeat=board_length))
            self.current_index = 0
            self.last_guess = None

        if self.last_guess is not None:
            last_guess_list = list(self.last_guess)
            
            self.guess_list = [
                guess for guess in self.guess_list 
                if self._matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
            ]
            self.current_index = 0  # Reset index after filtering

        
        guess = ''.join(self.guess_list[self.current_index])
        self.last_guess = guess
        self.current_index += 1
        print(guess)
        return guess
    
        # an idea for optimizing this is further pruning the search space
        # example board length = 5 & colors = 3
        # if ABACA is the code. and the previous guess was BBACB it should return 3 in correct spot 
        # we can then prune every code that does not follow the pattern XBACX
        # this can be done the other way around as well where if ABBBA returns 2 correct and nothing else 
        # we can prune everything else that does not follor the pattern of AXXXA
        # to implement this I would further need to understand the matches response method 

    






    

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        #[correct color in correct position, correct color in wrong position, guesses made]
        last_response: tuple[int, int, int],        
    ) -> str:
    
        if scsa_name == "OnlyOnce":
            return self.OnlyOnceSolver2(board_length, colors, scsa_name, last_response)
        
        if scsa_name == "TwoColor":
            return self.TwoColorSolver(board_length, colors, scsa_name, last_response)
        
        if scsa_name == "FirstLast":
            return self.FirstLastSolver(board_length, colors, scsa_name, last_response)
        

        
        if last_response[2] == 0:  # guesses made is 0
            self.guess_list = list(itertools.product(colors, repeat=board_length))
            self.current_index = 0
            self.last_guess = None

        if self.last_guess is not None:
            last_guess_list = list(self.last_guess)
            
            self.guess_list = [
                guess for guess in self.guess_list 
                if self._matches_response(list(guess), last_guess_list, last_response[0], last_response[1])
            ]
            self.current_index = 0  # Reset index after filtering

        
        guess = ''.join(self.guess_list[self.current_index])
        self.last_guess = guess
        self.current_index += 1
        print(guess)
        return guess

    def _matches_response(self, candidate: list, last_guess: list, correct_pos: int, correct_color: int) -> bool:
        """Helper method to check if a candidate guess could be valid given the last response"""
        exact = sum(1 for i in range(len(candidate)) if candidate[i] == last_guess[i])
        
        color_matches = sum(min(candidate.count(c), last_guess.count(c)) for c in set(candidate))
        
        return exact == correct_pos and (color_matches - exact) == correct_color
    
    


    
    
