import unittest
import time
from mastermind import *
from player import Player


class InvalidGuessFailureTestPlayer(Player):
    def __init__(self, regular_guess: str, invalid_guess: str, num_guesses: int):

        self.regular_guess = regular_guess
        self.invalid_guess = invalid_guess
        self.num_guesses = num_guesses

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:

        if last_response[2] == self.num_guesses - 1:

            return self.invalid_guess

        else:

            return self.regular_guess


class WinTestPlayer(Player):
    def __init__(self, regular_guess: str, winning_guess: str, num_guesses: int):

        self.regular_guess = regular_guess
        self.winning_guess = winning_guess
        self.num_guesses = num_guesses

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:

        if last_response[2] == self.num_guesses - 1:

            return self.winning_guess

        else:

            return self.regular_guess


class LossTestPlayer(Player):
    def __init__(self, incorrect_guess: str):

        self.incorrect_guess = incorrect_guess

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:

        return self.incorrect_guess


class TimeLossTestPlayer(Player):
    def __init__(self, sleep_time: float):

        self.sleep_time = sleep_time

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:

        time.sleep(self.sleep_time)


class TestRound(unittest.TestCase):
    def test_valid_guess(self):

        round = Round(
            board_length=5,
            colors=["A", "B", "C"],
            answer="ABCBA",
            scsa_name="InsertColors",
        )

        # Tests incorrect length and correct colors
        self.assertFalse(round.valid_guess("ABC"))
        self.assertFalse(round.valid_guess("ABCABC"))

        # Tests correct length and correct colors
        self.assertTrue(round.valid_guess("ABCBA"))

        # Tests correct length and non-existent colors
        self.assertFalse(round.valid_guess("ABCDE"))

    def test_count_colors(self):

        round = Round(
            board_length=5,
            colors=["A", "B", "C"],
            answer="ABCBA",
            scsa_name="InsertColors",
        )

        # All valid colors present
        guess = "ABCBA"
        correct_color_counts = [2, 2, 1]
        color_counts = round.count_colors(guess)
        self.assertEqual(color_counts, correct_color_counts)

        # Some valid colors present
        guess = "AAACC"
        correct_color_counts = [3, 0, 2]
        color_counts = round.count_colors(guess)
        self.assertEqual(color_counts, correct_color_counts)

        # Contains invalid colors
        guess = "DECF"
        with self.assertRaises(IndexError):
            color_counts = round.count_colors(guess)

    def test_process_guess(self):

        round = Round(
            board_length=5,
            colors=["A", "B", "C", "D", "E"],
            answer="ABCBA",
            scsa_name="InsertColors",
        )

        # No exact and no other
        guess = "DEDED"
        correct_response = (0, 0)
        response = round.process_guess(guess)
        self.assertEqual(response, correct_response)

        # Some exact and some other
        guess = "AACBB"
        correct_response = (3, 2)
        response = round.process_guess(guess)
        self.assertEqual(response, correct_response)

        # No exact and some other
        guess = "BCDEB"
        correct_response = (0, 3)
        response = round.process_guess(guess)
        self.assertEqual(response, correct_response)

        # Some exact and no other
        guess = "AECBD"
        correct_response = (3, 0)
        response = round.process_guess(guess)
        self.assertEqual(response, correct_response)

        # Answer
        guess = "ABCBA"
        correct_response = (5, 0)
        response = round.process_guess(guess)
        self.assertEqual(response, correct_response)

    def test_respond_to_guess(self):

        round = Round(
            board_length=5,
            colors=["A", "B", "C", "D", "E"],
            answer="ABCBA",
            scsa_name="InsertColors",
        )

        # Valid, some exact and some other
        guess = "AACBB"
        correct_response = (Result.VALID, 3, 2, 1)
        response = round.respond_to_guess(guess)
        self.assertEqual(response, correct_response)

        # Valid, no exact and some other
        guess = "BCDEB"
        correct_response = (Result.VALID, 0, 3, 2)
        response = round.respond_to_guess(guess)
        self.assertEqual(response, correct_response)

        # Valid, some exact and no other
        guess = "AECBD"
        correct_response = (Result.VALID, 3, 0, 3)
        response = round.respond_to_guess(guess)
        self.assertEqual(response, correct_response)

        # Invalid guess
        guess = "AECBF"
        correct_response = (Result.FAILURE, 0, 0, 4)
        response = round.respond_to_guess(guess)
        self.assertEqual(response, correct_response)

        # Answer
        guess = "ABCBA"
        correct_response = (Result.WIN, 5, 0, 5)
        response = round.respond_to_guess(guess)
        self.assertEqual(response, correct_response)

    def test_play_round(self):

        round = Round(
            board_length=5,
            colors=["A", "B", "C", "D", "E"],
            answer="ABCBA",
            scsa_name="InsertColors",
            time_cutoff=1,
        )

        # Invalid guess failure on guess 10
        invalid_guess_failure_player = InvalidGuessFailureTestPlayer(
            regular_guess="CBCDA", invalid_guess="ABCFEE", num_guesses=10
        )
        correct_response = (Result.FAILURE, 10)
        response = round.play_round(invalid_guess_failure_player)
        self.assertEqual(response, correct_response)

        # Win on guess 5
        winning_player = WinTestPlayer(
            regular_guess="BCBAD", winning_guess="ABCBA", num_guesses=5
        )
        correct_response = (Result.WIN, 5)
        response = round.play_round(winning_player)
        self.assertEqual(response, correct_response)

        # Max number of guesses loss
        losing_player = LossTestPlayer(incorrect_guess="DABCE")
        correct_response = (Result.LOSS, 100)
        response = round.play_round(losing_player)
        self.assertEqual(response, correct_response)

        # Time-out loss
        time_loss_player = TimeLossTestPlayer(sleep_time=2)
        correct_response = (Result.LOSS, 1)
        response = round.play_round(time_loss_player)
        self.assertEqual(response, correct_response)


if __name__ == "__main__":
    unittest.main()
