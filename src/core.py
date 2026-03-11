"""core.py

Task:
    Core logic of the game

Input:
    Player number and the number of field chosen

Output:
    The next state and player

"""

# [TODO] Move functions around and group
# [TODO] Type descriptions
# [TODO] Documentation


import sys

import numpy as np

# -------------------------------------------------
# Game constants
# -------------------------------------------------

ROWS = 2
COLS = 6
BOARD_SIZE = 12

WIN_SCORE = 25
DRAW_SCORE = 24

VALID_HOLES = {1, 2, 3, 4, 5, 6}
VALID_COMMANDS = {0, 10}
VALID_INPUTS = VALID_HOLES | VALID_COMMANDS


def get_names():
    """
    Gets names.
    """
    player1 = input("Player 1 name: ")
    player2 = input("Player 2 name: ")
    return player1, player2


# -------------------------------------------------
# Game state container
# -------------------------------------------------


def create_state(player1, player2):
    """1"""
    return {
        "board": [[1, 4, 4, 4, 4, 1], [1, 4, 4, 4, 4, 1]],
        "score": [24, 22],
        "player": [player1, player2],
        "current_player": np.random.randint(1, 3),
    }


def show_state(state):
    """1"""

    board = state["board"]
    score = state["score"]

    print("\n==============================")

    print(f"{state['player'][0]} | Captured: {score[0]}")
    print("   ", np.flip(board[0]))

    print("   ", np.array(board[1]))

    print(f"{state['player'][1]} | Captured: {score[1]}")

    print("==============================")


def initiate_game():
    """1"""
    player1, player2 = get_names()
    new_game = create_state(player1, player2)
    show_state(new_game)
    return new_game


# -------------------------------------------------
# Endgame detection
# -------------------------------------------------
def endgame_detection(state: dict) -> bool:
    """1"""

    if state["score"][0] or state["score"][1] >= WIN_SCORE:
        return True

    if state["score"][0] and state["score"][1] == DRAW_SCORE:
        return True

    return False


def winner_detection(state: dict) -> str | None:
    """Detects winner"""

    if state["score"][0] >= WIN_SCORE:
        return state["player"][0]

    if state["score"][1] >= WIN_SCORE:
        return state["player"][1]

    if (state["score"][0] and state["score"][1]) == DRAW_SCORE:
        return "draw"

    return None


# -------------------------------------------------
# Input helpers
# -------------------------------------------------
def get_current_player_nr(state) -> int:
    """1"""
    return state["current_player"] - 1


def has_seeds(state, hole) -> bool:
    """1"""
    current_player = get_current_player_nr(state)
    hole_nr = get_current_hole_nr(hole)
    return state["board"][current_player][hole_nr] > 0


def input_guardian(state: dict, cmd: int) -> bool:
    """1"""

    if cmd not in VALID_INPUTS:
        print(f"\nInvalid input: {input}")
        return False

    if cmd in VALID_HOLES:
        return has_seeds(state, cmd)

    if cmd in VALID_COMMANDS:
        return True

    print(f"Hole nr {cmd} is empty, Choose other hole.")
    return False


def get_input(state):
    """1"""
    current_player = get_current_player_nr(state)
    print("(0: new game, 10: end game.)")
    input_str = input(
        f"{state['player'][current_player]} choose hole from 1-6! \n"
    )
    while True:
        try:
            input_nr = int(input_str)
            break
        except ValueError:
            print("Invalid command.")
            input_str = input(
                f"{state['player'][current_player]} choose hole from 1-6! \n"
            )

    is_valid_input = input_guardian(state, input_nr)

    if is_valid_input:
        return input_nr

    return get_input(state)


# -------------------------------------------------
# Game helpers
# -------------------------------------------------
def can_capture(state, flat_board, hole_nr, seeds_in_hand):
    """1"""
    player_nr = get_current_player_nr(state)
    if (
        player_nr == 0
        and hole_nr > 5
        and flat_board[hole_nr] <= 2
        and seeds_in_hand == 1
    ):
        return True
    if (
        player_nr == 1
        and hole_nr < 6
        and flat_board[hole_nr] <= 2
        and seeds_in_hand == 1
    ):
        return True
    return False


def flatten_board(state):
    """1"""
    return [hole for player in state["board"] for hole in player]


def get_current_hole_nr(hole):
    """1"""
    return hole - 1


def take_seeds(state, hole):
    """1"""
    player_nr = get_current_player_nr(state)
    hole_nr = get_current_hole_nr(hole)
    seeds_in_hand = state["board"][player_nr][hole_nr]
    state["board"][player_nr][hole_nr] = 0
    return state, seeds_in_hand


def update_player(state):
    """1"""
    if state["current_player"] == 1:
        state["current_player"] = 2
    else:
        state["current_player"] = 1
    return state


def update_state(state, flat_board):
    """1"""
    state = update_player(state)
    state["board"][0] = flat_board[:6]
    state["board"][1] = flat_board[6:]
    return state


def sow_seeds(state, hole):
    """1"""
    state, seeds_in_hand = take_seeds(state, hole)
    flat_board = flatten_board(state)

    player_nr = get_current_player_nr(state)
    if player_nr == 1:
        hole += 6

    initial_input = hole

    # the while loop should probably be the sowing fun
    while seeds_in_hand > 0:
        hole_nr = get_current_hole_nr(hole)
        if initial_input != hole and seeds_in_hand > 1:
            flat_board[hole_nr] += 1
            seeds_in_hand -= 1

        elif initial_input != hole and can_capture(
            state, flat_board, hole_nr, seeds_in_hand
        ):
            state["score"][player_nr] += flat_board[hole_nr] + 1
            flat_board[hole_nr] = 0
            seeds_in_hand -= 1

        elif initial_input != hole:
            flat_board[hole_nr] += 1
            seeds_in_hand -= 1

        hole = (hole % 12) + 1

    new_state = update_state(state, flat_board)
    return new_state


def input_after_game():
    """1"""
    return input("0: new game, 10: end game")


def end_or_new_game(x):
    """1"""
    if x == 0:
        play()
    elif x == 10:
        sys.exit("Goodbye.")


# -------------------------------------------------
# Game loop
# -------------------------------------------------
def game_loop(state):
    """1"""
    hole = get_input(state)
    end_or_new_game(hole)

    new_state = sow_seeds(state, hole)
    show_state(new_state)
    game_ended = endgame_detection(state)
    if game_ended:
        winner = winner_detection(state)
        if winner == "draw":
            print("It's a tie!")
        else:
            print(f"{winner} wins!")

        x = None
        while True:
            try:
                x = int(input_after_game().strip())
            except ValueError:
                print("Please enter a number.")
                continue

            if x in VALID_COMMANDS:
                break

            print("Invalid command.")

        end_or_new_game(x)

    game_loop(new_state)


def play():
    """1"""
    new_game = initiate_game()
    game_loop(new_game)

    return True


if __name__ == "__main__":
    play()
