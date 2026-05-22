"""Tests for FieldCollection."""

import pytest

from game_logic.Field import Field
from game_logic.FieldCollection import FieldCollection
from game_logic.Player import Player


def create_collection():
    """Create a reusable test collection."""
    player_1 = Player("P1")
    player_2 = Player("P2")
    return FieldCollection(player_1, player_2), player_1, player_2


def test_create_fields():
    """Test correct field ownership."""
    collection, player_1, player_2 = create_collection()

    assert collection.fields[0].owner is player_1
    assert collection.fields[5].owner is player_1
    assert collection.fields[6].owner is player_2
    assert collection.fields[11].owner is player_2


def test_clone():
    """Test cloning field collection."""
    collection, _, _ = create_collection()

    clone = collection.clone()

    assert clone is not collection
    assert clone.fields is not collection.fields
    assert len(clone.fields) == len(collection.fields)


def test_get_next_index_wraps():
    """Test next index wrapping."""
    collection, _, _ = create_collection()

    assert collection.get_next_index(11) == 0


def test_get_previous_index_wraps():
    """Test previous index wrapping."""
    collection, _, _ = create_collection()

    assert collection.get_previous_index(0) == 11


def test_get_field_index():
    """Test retrieving field index."""
    collection, _, _ = create_collection()

    field = collection.fields[3]

    assert collection.get_field_index(field) == 3


def test_get_field_index_invalid():
    """Test error on missing field."""
    collection, _, _ = create_collection()

    fake_field = Field(Player("X"))  # or any Field not in collection

    with pytest.raises(ValueError):
        collection.get_field_index(fake_field)


def test_opponent_has_no_beans_false():
    """Test opponent still has beans."""
    collection, player_1, _ = create_collection()

    assert collection.opponent_has_no_beans(player_1) is False


def test_opponent_has_no_beans_true():
    """Test opponent has no beans."""
    collection, player_1, player_2 = create_collection()

    for field in collection.fields:
        if field.owner is player_2:
            field.remove_beans()

    assert collection.opponent_has_no_beans(player_1) is True


def test_can_reach_opponent_true():
    """Test reaching opponent side."""
    collection, player_1, _ = create_collection()

    collection.fields[5].beans = [1]

    assert collection.can_reach_opponent(5, player_1) is True


def test_has_valid_moves_true():
    """Test valid moves exist."""
    collection, player_1, _ = create_collection()

    assert collection.has_valid_moves(player_1) is True


def test_has_valid_moves_false():
    """Test no valid moves."""
    collection, player_1, _ = create_collection()

    for field in collection.fields:
        if field.owner is player_1:
            field.remove_beans()

    assert collection.has_valid_moves(player_1) is False


def test_can_seed_from_wrong_owner():
    """Test cannot seed opponent field."""
    collection, player_1, _ = create_collection()

    assert collection.can_seed_from(8, player_1) is False


def test_can_seed_from_empty():
    """Test cannot seed empty field."""
    collection, player_1, _ = create_collection()

    collection.fields[0].remove_beans()

    assert collection.can_seed_from(0, player_1) is False


def test_start_seeding_from():
    """Test bean distribution updates board state."""
    collection, player_1, _ = create_collection()

    start_count = collection.fields[0].bean_count()

    last_index = collection.start_seeding_from(0, player_1)

    assert isinstance(last_index, int)
    assert collection.fields[0].bean_count() < start_count


def test_start_seeding_from_invalid():
    """Test invalid seeding raises."""
    collection, player_1, _ = create_collection()

    with pytest.raises(ValueError):
        collection.start_seeding_from(8, player_1)


def test_can_harvest_from_false_own_field():
    """Test cannot harvest own field."""
    collection, player_1, _ = create_collection()

    assert collection.can_harvest_from(0, player_1) is False


def test_can_harvest_from_false_too_few():
    """Test cannot harvest with too few beans."""
    collection, player_1, player_2 = create_collection()

    collection.fields[6].beans = [1]

    assert collection.can_harvest_from(6, player_1) is False


def test_skip_rule_applies_false():
    """Test skip rule inactive."""
    collection, player_1, _ = create_collection()

    collection.fields[0].beans = [1] * 5

    assert collection.skip_rule_applies(0, player_1) is False
