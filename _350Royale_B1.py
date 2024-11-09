"""
#1: Implement a general-purpose player. Your program should be able to play for any number of pegs and
colors. It should also make reasonable guesses based on the responses it has receive

Functioning baseline player that can play a 4-6 tournament in our environment without illegal guesses.

B1: Exhaustively enumerate all possibilities. Guess each possibility in lexicographic order one at a time, and pay
no attention to the system’s responses. For example, if pegs p = 4 and colors c = 3, guess AAAA, AAAB, AAAC,
AABA, AABB, AABC and so on. This method will take at most (c^p) guesses.

"""

import argparse
from scsa import *
from player import *
from mastermind import *
import time
import itertools

class Baseline1(Player):
    def __init__(self):
        self.player_name = "Baseline1"
        self.guess_list = None

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        #[correct color in correct position, correct color wrong position, guesses made]
        last_response: tuple[int, int, int],        
    ) -> str:
        
        if self.guess_list is None:

            self.guess_list = itertools.cycle(      #Iterates repeatably if all possible guesses are enumerated
                itertools.product(                  #Creates a list of all possible guesses
                    colors, 
                    repeat=board_length
                )
            )

        guess = ''.join(next(self.guess_list, None)) 
        
        return guess