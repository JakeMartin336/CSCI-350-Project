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

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        #[correct color in correct position, correct color in wrong position, guesses made]
        last_response: tuple[int, int, int],        
    ) -> str:
        
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

        if self.current_index >= len(self.guess_list):
            # If we've somehow run out of valid guesses, return first color repeated
            return colors[0] * board_length
        
        guess = ''.join(self.guess_list[self.current_index])
        self.last_guess = guess
        self.current_index += 1
        return guess

    def _matches_response(self, candidate: list, last_guess: list, correct_pos: int, correct_color: int) -> bool:
        """Helper method to check if a candidate guess could be valid given the last response"""
        exact = sum(1 for i in range(len(candidate)) if candidate[i] == last_guess[i])
        
        color_matches = sum(min(candidate.count(c), last_guess.count(c)) for c in set(candidate))
        
        return exact == correct_pos and (color_matches - exact) == correct_color