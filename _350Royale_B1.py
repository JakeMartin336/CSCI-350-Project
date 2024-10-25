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

class _350Royale_B1(Player):
    def __init__(self):
        self.player_name = "_350Royale_B1"
        self.guess_list = None

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:
        
        if self.guess_list is None:
            self.guess_list = itertools.product(colors, repeat=board_length)
        
        new_guess = next(self.guess_list, None)
        
        if new_guess is None:
            return ""
        
        return_guess = ''.join(new_guess)
        
        return return_guess


player = _350Royale_B1()
scsa = ABColor()

colors = ["A","B"]
board_length = 4
num_rounds = 100

mastermind = Mastermind(board_length, colors)
mastermind.play_tournament(player, scsa, 100)
