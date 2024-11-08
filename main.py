# Main file to run game of Mastermind based on command-line arguments.
# See example.ipynb for other ways to use the Mastermind representation.

# To run:
# python main.py --board_length 4 --num_colors 4 --player_name Baseline1 --scsa_name InsertColors --num_rounds 5
# python main.py --board_length 4 --num_colors 4 --player_name TournamentPlayer --scsa_name InsertColors --num_rounds 5



import argparse
import _350Royale_B1
import _350Royale_d3
from scsa import *
from player import *
from mastermind import *


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
    choices=["RandomFolks", "Boring", "Baseline1", 'TournamentPlayer'],
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

    elif player_name == 'TournamentPlayer':
        player = _350Royale_d3.TournamentPlayer()

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

mastermind = Mastermind(args.board_length, colors)
mastermind.play_tournament(player, scsa, args.num_rounds)

###################################################################################

# num_rounds = 100
# guess_cutoff = 250  # Default is 100 guesses
# round_time_cutoff = 10  # Default is 5 seconds
# tournament_time_cutoff = 1000  # Default is 300 seconds

# mastermind = Mastermind(args.board_length, colors, guess_cutoff, round_time_cutoff, tournament_time_cutoff)
# mastermind.play_tournament(player, scsa, num_rounds)



# 7 pegs
# 5 colors
