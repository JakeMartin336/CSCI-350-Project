# Main file to run game of Mastermind based on command-line arguments.
# See example.ipynb for other ways to use the Mastermind representation.

# To run:
# python main.py --board_length 4 --num_colors 4 --player_name Baseline1 --scsa_name InsertColors --num_rounds 5
# python main.py --board_length 4 --num_colors 4 --player_name _350Royale --scsa_name InsertColors --num_rounds 5



import argparse
import _350Royale_B1
import _350Royale_B2
import _350Royale_d3
from scsa import *
from player import *
from mastermind import *
import time


parser = argparse.ArgumentParser(description="Play a game of Mastermind.")
parser.add_argument("--board_length", nargs="?", type=int, required=True)
parser.add_argument(
    "--num_colors", nargs="?", type=int, required=True, choices=range(1, 27)
)
parser.add_argument(
    "--player_name",
    nargs="?",
    type=str,
    required=True,
    choices=["RandomFolks", "Boring", "Baseline1", "Baseline2", '_350Royale'],
)
parser.add_argument(
    "--scsa_name",
    nargs="?",
    type=str,
    required=True,
    choices=[
        "InsertColors",
        "TwoColor",
        "ABColor",
        "TwoColorAlternating",
        "OnlyOnce",
        "FirstLast",
        "UsuallyFewer",
        "PreferFewer",
        "Mystery2",
    ],
)
parser.add_argument("--num_rounds", nargs="?", type=int, required=True)

args = parser.parse_args()

def str_to_player(player_name: str) -> Player:

    if player_name == "RandomFolks":
        player = RandomFolks()

    elif player_name == "Boring":
        player = Boring()

    elif player_name == "Baseline1":
        player = _350Royale_B1.Baseline1()

    elif player_name == "Baseline2":
        player = _350Royale_B2.Baseline2()

    elif player_name == '_350Royale':
        player = _350Royale_d3._350Royale()

    else:
        raise ValueError("Unrecognized Player.")

    return player


def str_to_scsa(scsa_name: str) -> SCSA:

    if scsa_name == "InsertColors":
        scsa = InsertColors()

    elif scsa_name == "TwoColor":
        scsa = TwoColor()

    elif scsa_name == "ABColor":
        scsa = ABColor()

    elif scsa_name == "TwoColorAlternating":
        scsa = TwoColorAlternating()

    elif scsa_name == "OnlyOnce":
        scsa = OnlyOnce()

    elif scsa_name == "FirstLast":
        scsa = FirstLast()

    elif scsa_name == "UsuallyFewer":
        scsa = UsuallyFewer()

    elif scsa_name == "PreferFewer":
        scsa = PreferFewer()

    elif scsa_name == "Mystery2":
        scsa = Mystery2()

    else:
        raise ValueError("Unrecognized SCSA.")

    return scsa



# Output (teamName_d3.txt) from 5-7 tournaments where your current tournament player played 100 rounds in 
# a 5-7 tournament against each of the 13 SCSAs and made no illegal guesses. 
# • Output (teamName_B#.txt) from 5-7 tournaments where your baseline player played 100 rounds in a 5-7 
# tournament against each of the 13 SCSAs and made no illegal guesses.


player = str_to_player(args.player_name)
scsa = str_to_scsa(args.scsa_name)
colors = [chr(i) for i in range(65, 91)][: args.num_colors]

# Add tournament timing
start_time = time.time()
mastermind = Mastermind(args.board_length, colors)
results = mastermind.play_tournament(player, scsa, args.num_rounds)
end_time = time.time()

# Print tournament summary
print(f"\nTournament Time:")
print(f"Time taken: {end_time - start_time:.4f} seconds")
print(f"Average time per round: {(end_time - start_time)/args.num_rounds:.4f} seconds")

###################################################################################

# num_rounds = 100
# guess_cutoff = 250  # Default is 100 guesses
# round_time_cutoff = 10  # Default is 5 seconds
# tournament_time_cutoff = 1000  # Default is 300 seconds

# mastermind = Mastermind(args.board_length, colors, guess_cutoff, round_time_cutoff, tournament_time_cutoff)
# mastermind.play_tournament(player, scsa, num_rounds)