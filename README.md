# DEADLINE 2: 

Feel free to submit early for confirmation that you are on the right track.

- Player teamName_B#.py where # is 1,2,3, or 4 for exactly one correctly-named, functioning baseline player
that can play a 4-6 tournament in our environment without illegal guesses.

- Output (teamName_B#.txt) from a 4-6 tournament where your baseline played 100 rounds against 2 different
non-trivial SCSAs without illegal guesses. (Which ones are trivial? InsertColors, ABColor, and OnlyOnce. What's so
easy about InsertColors? It is totally random, so easy to compete against but hard to win against.)

## Testing main.py
- run `python main.py --board_length <value> --num_colors <value> --player_name <value> --scsa_name <value> --num_rounds <value>`
- example: `python main.py --board_length 4 --num_colors 6 --player_name Baseline1 --scsa_name TwoColor --num_rounds 100`

