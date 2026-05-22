"""Tests for the Board_renderer module."""

# pylint: disable=no-member, too-few-public-methods

import os

import pygame

from Board_renderer import Renderer
from GameMode import GameMode

os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
pygame.image.load = lambda _: pygame.Surface((10, 10))


class FakePlayer:
    """Minimal fake player for renderer tests."""

    def __init__(self, name):
        self.name = name


class FakeBoard:
    """Minimal fake board for renderer tests."""

    def __init__(self):
        self.field_collection = type("FC", (), {})()
        self.field_collection.fields = [
            type("F", (), {"bean_positions": []})() for _ in range(12)
        ]
        self.bank = {}


class FakeGame:
    """Minimal fake game for renderer tests."""

    def __init__(self):
        self.player_1 = FakePlayer("P1")
        self.player_2 = FakePlayer("P2")
        self.board = FakeBoard()
        self.mode = None

    def current_player(self):
        """Return the current player."""
        return self.player_1


def test_undo_button_collision_true():
    """Test collision detection inside undo button."""
    game = FakeGame()
    renderer = Renderer(game)

    x, y = renderer.undo_button.center
    assert renderer.get_undo_button_collision((x, y)) is True


def test_undo_button_collision_false():
    """Test collision detection outside undo button."""
    game = FakeGame()
    renderer = Renderer(game)

    assert renderer.get_undo_button_collision((0, 0)) is False


def test_mode_selection_hit():
    """Test mode selection button detection."""
    game = FakeGame()
    renderer = Renderer(game)

    for mode, rect in renderer.mode_buttons.items():
        x, y = rect.center
        assert renderer.get_mode_from_position((x, y)) == mode


def test_depth_selection():
    """Test depth selection button detection."""
    game = FakeGame()
    renderer = Renderer(game)

    for depth, rect in renderer.depth_buttons.items():
        x, y = rect.center
        assert renderer.get_depth_from_position((x, y)) == depth


def test_history_suggestion_none():
    """Test that no suggestion is returned for invalid positions."""
    game = FakeGame()
    renderer = Renderer(game)

    assert renderer.get_history_suggestion_at_position((9999, 9999)) is None


def test_history_input_click_inside():
    """Test activating history input field."""
    game = FakeGame()
    renderer = Renderer(game)

    pos = renderer.history_input_field.center

    assert renderer.handle_history_input_click(pos) is True
    assert renderer.history_input_active is True


def test_history_input_click_outside():
    """Test deactivating history input field."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.history_input_active = True

    assert renderer.handle_history_input_click((0, 0)) is False
    assert renderer.history_input_active is False


def test_history_input_key_add_character():
    """Test typing into history input."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.history_input_active = True

    event = pygame.event.Event(
        pygame.KEYDOWN,
        {"unicode": "a", "key": pygame.K_a},
    )

    renderer.handle_history_input_key(event)

    assert renderer.history_player_text == "a"


def test_history_input_key_backspace():
    """Test deleting history input text."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.history_input_active = True
    renderer.history_player_text = "abc"

    event = pygame.event.Event(
        pygame.KEYDOWN,
        {"key": pygame.K_BACKSPACE, "unicode": ""},
    )

    renderer.handle_history_input_key(event)

    assert renderer.history_player_text == "ab"


def test_history_input_key_return():
    """Test pressing enter in history input."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.history_input_active = True

    event = pygame.event.Event(
        pygame.KEYDOWN,
        {"key": pygame.K_RETURN, "unicode": ""},
    )

    assert renderer.handle_history_input_key(event) is True


def test_get_history_input_value_strips_spaces():
    """Test stripping whitespace from history input."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.history_player_text = "  Alice  "

    assert renderer.get_history_input_value() == "Alice"


def test_name_input_click_player1():
    """Test selecting player1 input field."""
    game = FakeGame()
    renderer = Renderer(game)

    pos = renderer.name_input_fields["player1"].center

    renderer.handle_name_input_click(pos, GameMode.HUMAN_VS_HUMAN)

    assert renderer.active_field == "player1"


def test_name_input_click_player2():
    """Test selecting player2 input field."""
    game = FakeGame()
    renderer = Renderer(game)

    pos = renderer.name_input_fields["player2"].center

    renderer.handle_name_input_click(pos, GameMode.HUMAN_VS_HUMAN)

    assert renderer.active_field == "player2"


def test_name_input_key_add_character():
    """Test typing into active name field."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.active_field = "player1"

    event = pygame.event.Event(
        pygame.KEYDOWN,
        {"unicode": "x", "key": pygame.K_x},
    )

    renderer.handle_name_input_key(event, GameMode.HUMAN_VS_HUMAN)

    assert renderer.player_names["player1"] == "x"


def test_name_input_key_backspace():
    """Test deleting character from name input."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.active_field = "player1"
    renderer.player_names["player1"] = "Max"

    event = pygame.event.Event(
        pygame.KEYDOWN,
        {"key": pygame.K_BACKSPACE, "unicode": ""},
    )

    renderer.handle_name_input_key(event, GameMode.HUMAN_VS_HUMAN)

    assert renderer.player_names["player1"] == "Ma"


def test_name_input_return_switches_field():
    """Test enter switches from player1 to player2."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.active_field = "player1"
    renderer.player_names["player1"] = "Alice"

    event = pygame.event.Event(
        pygame.KEYDOWN,
        {"key": pygame.K_RETURN, "unicode": ""},
    )

    result = renderer.handle_name_input_key(
        event,
        GameMode.HUMAN_VS_HUMAN,
    )

    assert result is False
    assert renderer.active_field == "player2"


def test_name_input_return_finishes():
    """Test enter confirms second player."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.active_field = "player2"
    renderer.player_names["player2"] = "Bob"

    event = pygame.event.Event(
        pygame.KEYDOWN,
        {"key": pygame.K_RETURN, "unicode": ""},
    )

    result = renderer.handle_name_input_key(
        event,
        GameMode.HUMAN_VS_HUMAN,
    )

    assert result is True


def test_get_player_names_defaults():
    """Test default player names."""
    game = FakeGame()
    renderer = Renderer(game)

    assert renderer.get_player_names() == ("Player 1", "Player 2")


def test_get_player_names_custom():
    """Test custom player names."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.player_names["player1"] = "Alice"
    renderer.player_names["player2"] = "Bob"

    assert renderer.get_player_names() == ("Alice", "Bob")


def test_draw_winner_draw():
    """Test draw winner screen branch."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer._draw_winner("draw")


def test_draw_winner_player1():
    """Test player1 winner branch."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer._draw_winner(game.player_1)


def test_draw_winner_player2():
    """Test player2 winner branch."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer._draw_winner(game.player_2)


def test_draw_history_screen_empty():
    """Test history screen with no games."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.draw_history_screen([])


def test_draw_history_screen_with_error():
    """Test history screen with error message."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.draw_history_screen(None, "Error")


def test_draw_history_screen_with_suggestions():
    """Test history suggestions rendering."""
    game = FakeGame()
    renderer = Renderer(game)

    renderer.history_suggestions = [
        (1, "Alice"),
        (2, "Bob"),
    ]

    renderer.draw_history_screen([])
