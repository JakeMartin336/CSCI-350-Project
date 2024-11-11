import argparse
from scsa import *
from player import *
from mastermind import *
import time
import itertools
from collections import Counter
from itertools import permutations

class Baseline3(Player):
    def __init__(self):
        self.player_name = "Baseline3"
        self.guess_list = None
        self.current_index = 0
        self.last_guess = None
        self.color_counts = {}
        self.counting_phase = True

    def generate_combinations(self, color_counts):
        elements = []
        for color, count in color_counts.items():
            elements.extend([color] * count)
        
        return [''.join(p) for p in set(permutations(elements))]

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],        
    ) -> str:
        # Reset
        if last_response[2] == 0:
            self.guess_list = []
            for color in colors[:-1]:  # Skip the last color
                self.guess_list.append(color * board_length)
            self.current_index = 0
            self.last_guess = None
            self.color_counts = {}
            self.counting_phase = True

        if self.last_guess is not None and self.counting_phase:
            total_matches = last_response[0] + last_response[1]
            color = self.last_guess[0]
            self.color_counts[color] = total_matches
            
            if len(self.color_counts) == len(colors) - 1:
                # Deduce last color count
                known_sum = sum(self.color_counts.values())
                last_color = colors[-1]
                self.color_counts[last_color] = board_length - known_sum
                print(f"Color counts found: {self.color_counts}")
                
                # Generate new guess list based on color counts
                self.guess_list = self.generate_combinations(self.color_counts)
                self.current_index = 0
                self.counting_phase = False

        # Next guess
        if self.current_index >= len(self.guess_list):
            return colors[0] * board_length
        
        guess = self.guess_list[self.current_index]
        self.last_guess = guess
        self.current_index += 1
        return guess

        
