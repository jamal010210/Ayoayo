"""Tests for the bot_logic module."""

# pylint: disable=too-few-public-methods

from bot.bot_logic import choose_move, get_legal_moves


class FakePlayer:
    """Minimal fake player."""

    def __init__(self, name):
        self.name = name


class FakeFieldCollection:
    """Fake field collection for testing legal moves."""

    def __init__(self, legal_moves):
        self.fields = [0] * 12
        self.legal_moves = legal_moves

    def can_seed_from(self, index, _player):
        """Return whether move is legal."""
        return index in self.legal_moves


class FakeBoard:
    """Minimal fake board for bot tests."""

    def __init__(self, legal_moves=None):
        if legal_moves is None:
            legal_moves = []

        self.player1 = FakePlayer("P1")
        self.player2 = FakePlayer("P2")

        self.field_collection = FakeFieldCollection(legal_moves)

        self.bank = {
            self.player1: 0,
            self.player2: 0,
        }

    def clone_deep(self):
        """Return a cloned board."""
        clone = FakeBoard(self.field_collection.legal_moves)
        clone.bank = self.bank.copy()
        clone.player1 = self.player1
        clone.player2 = self.player2
        return clone

    def seed_from_field(self, move, player):
        """Simulate a move by increasing score."""
        self.bank[player] += move


def test_get_legal_moves():
    """Test legal move detection."""
    board = FakeBoard([1, 3, 5])

    moves = get_legal_moves(board, board.player1)

    assert moves == [1, 3, 5]


def test_get_legal_moves_empty():
    """Test empty legal move list."""
    board = FakeBoard([])

    moves = get_legal_moves(board, board.player1)

    assert not moves


def test_choose_move_best_score_depth_one():
    """Test bot chooses highest scoring move."""
    board = FakeBoard([1, 2, 5])

    move = choose_move(board, board.player1, 1)

    assert move == 5


def test_choose_move_returns_none_without_moves():
    """Test bot returns None when no legal moves exist."""
    board = FakeBoard([])

    move = choose_move(board, board.player1, 1)

    assert move is None


def test_choose_move_recursive():
    """Test recursive move selection."""
    board = FakeBoard([2, 4])

    move = choose_move(board, board.player1, 2)

    assert move in [2, 4]
