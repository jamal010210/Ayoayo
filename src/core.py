"""
core.py

Contains the core logic for the game.

This module manages:
- Game state creation and updates
- Player moves and seed distribution
- Input handling and validation
- Endgame detection and winner determination
- The main game loop

All functions operate on the game state and handle the flow of the game.
"""

# [TODO] Implement game history

import sys

import numpy as np

# Game Constants
# ----------------------------------------------------------------------------

ROWS = 2
COLS = 6
BOARD_SIZE = 12

WIN_SCORE = 25
DRAW_SCORE = 24

VALID_HOLES = {1, 2, 3, 4, 5, 6}
VALID_COMMANDS = {0, 10}
VALID_INPUTS = VALID_HOLES | VALID_COMMANDS

# Player and Input Handling
# ----------------------------------------------------------------------------


def get_names() -> tuple[str, str]:
    """
    Gets names.
    """
    return input("Player 1 name: "), input("Player 2 name: ")


def get_current_hole_idx(hole: int) -> int:
    """
    Gets the current hole index.
    """
    return hole - 1


def get_current_player_idx(state: dict) -> int:
    """
    Gets the current player index.
    """
    return state["current_player"] - 1


def has_seeds(state: dict, hole: int) -> bool:
    """
    Checks if a hole has any seeds in it.
    """
    player_idx = get_current_player_idx(state)
    hole_idx = get_current_hole_idx(hole)
    return state["board"][player_idx][hole_idx] > 0


def is_valid_input(state: dict, cmd: int) -> bool:
    """
    Checks if a given command is valid for the current game state.
    """

    if cmd not in VALID_INPUTS:
        print(f"\nInvalid input: {input}")
        return False

    if cmd in VALID_HOLES:
        if has_seeds(state, cmd):
            return True
        print(f"Hole nr {cmd} is empty, Choose other hole.")
        return False

    return True


def get_input(state: dict) -> int:
    """
    Prompts the current player until a valid command is entered.
    Returns the valid integer command.
    """
    player_idx = get_current_player_idx(state)
    prompt = (
        f"{state['player'][player_idx]} choose hole from 1-6! "
        "(0: new game, 10: end game)\n"
    )
    while True:
        input_str = input(prompt)
        try:
            input_nr = int(input_str)
        except ValueError:
            print("Invalid command. Please enter a number.")
            continue

        if is_valid_input(state, input_nr):
            return input_nr


def end_or_new_game(cmd: int) -> None:
    """
    Handles post-game commands.

    Starts a new game if the command is 0 or exits the program if the
    command is 10.

    Args:
        cmd: Integer command entered by the user.
    """
    if cmd == 0:
        play()
    elif cmd == 10:
        sys.exit("Goodbye.")


# Game State Management
# ----------------------------------------------------------------------------


def create_state(player1: str, player2: str) -> dict:
    """
    Creates a new board, given two player names as strings and chooses
    the starting player randomly.

    Args:
        player1: Name of player 1
        player2: Name of player 2
    """
    return {
        "board": [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]],
        "score": [0, 0],
        "player": [player1, player2],
        "current_player": np.random.randint(1, 3),
    }


def show_state(state: dict) -> None:
    """
    Pretty prints the state of a game in the console.
    """

    board = state["board"]
    score = state["score"]

    print("\n==============================")

    print(f"{state['player'][0]} | Captured: {score[0]}")
    print("   ", np.flip(board[0]))

    print("   ", np.array(board[1]))

    print(f"{state['player'][1]} | Captured: {score[1]}")

    print("==============================")


def initiate_game() -> dict:
    """
    Creates a new game and displays it.
    """
    player1, player2 = get_names()
    new_game = create_state(player1, player2)
    show_state(new_game)
    return new_game


def update_player(state: dict) -> dict:
    """
    Switches the current player.
    """
    state["current_player"] = 3 - state["current_player"]
    return state


def flatten_board(state: dict) -> list[int]:
    """
    Flattens the board to make the sowing easier.
    """
    return [hole for player in state["board"] for hole in player]


def take_seeds(state: dict, hole: int) -> tuple[dict, int]:
    """
    Removes all seeds from the selected hole and returns them.

    Args:
        state: Current game state.
        hole: Hole number chosen by the current player.

    Returns:
        The updated state and the number of seeds taken.
    """
    player_idx = get_current_player_idx(state)
    hole_idx = get_current_hole_idx(hole)
    seeds_in_hand = state["board"][player_idx][hole_idx]
    state["board"][player_idx][hole_idx] = 0
    return state, seeds_in_hand


def update_state(state: dict, flat_board: list[int]) -> dict:
    """
    Updates the game state after a move.

    Switches the current player and reconstructs the board
    from the flattened board representation.
    """
    state = update_player(state)
    state["board"][0] = flat_board[:6]
    state["board"][1] = flat_board[6:]
    return state


# Game Rules and Logic
# ----------------------------------------------------------------------------


def can_capture(
    state: dict, flat_board: list[int], hole_idx: int, seeds_in_hand: int
) -> bool:
    """
    Determines if the current player can capture seeds from a hole.

    Seeds can be captured if the last seed lands in an opponent's hole that
    contains 1 or 2 seeds and the player has only 1 seed in hand.
    """
    player_idx = get_current_player_idx(state)

    opponent_hole = (player_idx == 0 and hole_idx > 5) or (
        player_idx == 1 and hole_idx < 6
    )

    return opponent_hole and flat_board[hole_idx] <= 2 and seeds_in_hand == 1


def sow_seeds(
    state: dict, hole: int, seeds_in_hand: int
) -> tuple[list[int], dict]:
    """
    Distributes seeds from the chosen hole across the board, handling captures
    according to the game rules.

    Args:
        state: Current game state.
        hole: Hole number where seeds are taken from.
        seeds_in_hand: Number of seeds currently in hand.

    Returns:
        A tuple containing the updated flat board and the updated game state.
    """

    flat_board = flatten_board(state)
    player_idx = get_current_player_idx(state)

    if player_idx == 1:
        hole += 6

    initial_input = hole

    while seeds_in_hand > 0:
        hole_idx = get_current_hole_idx(hole)
        if initial_input != hole and seeds_in_hand > 1:
            flat_board[hole_idx] += 1
            seeds_in_hand -= 1

        elif initial_input != hole and can_capture(
            state, flat_board, hole_idx, seeds_in_hand
        ):
            state["score"][player_idx] += flat_board[hole_idx] + 1
            flat_board[hole_idx] = 0
            seeds_in_hand -= 1

        elif initial_input != hole:
            flat_board[hole_idx] += 1
            seeds_in_hand -= 1

        hole = (hole % 12) + 1

    return flat_board, state


def move_seeds(state: dict, hole_nr: int) -> dict:
    """
    Executes a player's move by taking seeds from the chosen hole,
    distributing them across the board, handling captures,
    and updating the game state.

    Args:
        state: Current game state.
        hole_nr: Hole number chosen by the current player.

    Returns:
        The updated game state after the move.
    """
    state, seeds_in_hand = take_seeds(state, hole_nr)
    flat_board, state = sow_seeds(state, hole_nr, seeds_in_hand)
    return update_state(state, flat_board)


# Endgame Detection
# ----------------------------------------------------------------------------


def has_game_ended(state: dict) -> bool:
    """
    Checks whether the game has ended.

    Args:
        state: Current game state containing the players' scores.

    Returns:
        True if the game has ended, False otherwise.
    """
    if state["score"][0] >= WIN_SCORE or state["score"][1] >= WIN_SCORE:
        return True

    if state["score"][0] == DRAW_SCORE and state["score"][1] == DRAW_SCORE:
        return True

    return False


def winner_detection(state: dict) -> str | None:
    """
    Determines the winner of the game.

    Returns the winning player's name, "draw" if tied, or None if the game
    is still ongoing.
    """

    if state["score"][0] >= WIN_SCORE:
        return state["player"][0]

    if state["score"][1] >= WIN_SCORE:
        return state["player"][1]

    if state["score"][0] == DRAW_SCORE and state["score"][1] == DRAW_SCORE:
        return "draw"

    return None


# Game loop
# ----------------------------------------------------------------------------


def handle_player_input(state) -> int:
    """Prompts the player until a valid command is entered."""
    hole = get_input(state)
    end_or_new_game(hole)
    return hole


def handle_endgame(state: dict) -> None:
    """
    Checks if the game has ended and
    handles winner display and post-game commands.
    """
    if has_game_ended(state):
        winner = winner_detection(state)
        if winner == "draw":
            print("It's a tie!")
        else:
            print(f"{winner} wins!")

        while True:
            try:
                x = int(input("0: new game, 10: end game").strip())
            except ValueError:
                print("Please enter a number.")
                continue

            if x in VALID_COMMANDS:
                break

            print("Invalid command.")

        end_or_new_game(x)


def game_loop(state) -> None:
    """Main game loop: orchestrates player moves until the game ends."""
    hole = handle_player_input(state)
    new_state = move_seeds(state, hole)
    show_state(new_state)
    handle_endgame(new_state)
    game_loop(new_state)


def play() -> None:
    """
    Starts a new game and enters the main game loop.
    """
    new_game = initiate_game()
    game_loop(new_game)


if __name__ == "__main__":
    play()
