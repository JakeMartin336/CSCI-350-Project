
from scsa import *
from player import *
from mastermind import *
import _350Royale_B1
import time

class TournamentPlayer(Player):
    def __init__(self):
        self.player_name = "350 Royale Tournament Player"
        self.time = None
        self.num_guesses = 0

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,                             #Type of SCSA irrelevant to player
        last_response: tuple[int, int, int],        #No attention paid to responses
    ) -> str:
        
        if scsa_name == "InsertColors":
            make_guess = _350Royale_B1.Baseline1()
        elif scsa_name == "TwoColor":
            make_guess = _350Royale_B1.Baseline1()
        elif scsa_name == "ABColor":
            make_guess = _350Royale_B1.Baseline1()
        elif scsa_name == "TwoColorAlternating":
            make_guess = _350Royale_B1.Baseline1()
        elif scsa_name == "OnlyOnce":
            make_guess = _350Royale_B1.Baseline1()
        elif scsa_name == "FirstLast":
            make_guess = _350Royale_B1.Baseline1()
        elif scsa_name == "UsuallyFewer":
            make_guess = _350Royale_B1.Baseline1()
        elif scsa_name == "PreferFewer":
            make_guess = _350Royale_B1.Baseline1()
        else:
            raise ValueError("Unrecognized SCSA.")
        
        return make_guess
