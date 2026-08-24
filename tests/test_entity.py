"""Tests for entities and movement."""

from game.core.entity import Entity, Monster, Player
from game.core.world import World


def test_moving_into_open_floor_works():
    world = World(width=10, height=6)
    entity = Entity(x=4, y=3)
    world.add_entity(entity)

    assert entity.move_by(world, 1, 0) is True
    assert (entity.x, entity.y) == (5, 3)


def test_moving_into_a_wall_is_refused():
    world = World(width=10, height=6)
    entity = Entity(x=1, y=1)
    world.add_entity(entity)

    # (1, 1) is just inside the top-left corner, so up and left are walls.
    assert entity.move_by(world, 0, -1) is False
    assert (entity.x, entity.y) == (1, 1)


def test_player_moves_when_told_to():
    world = World(width=10, height=6)
    player = Player(x=4, y=3)
    world.add_entity(player)

    player.pending_move = (0, 1)
    world.step()

    assert (player.x, player.y) == (4, 4)
    # The move is consumed, so the player does not keep sliding.
    assert player.pending_move is None


def test_stepping_the_world_does_not_crash_with_monsters_in_it():
    """Monster.act() is a stub in week 1. The game must still run."""
    world = World(width=10, height=6)
    world.add_entity(Player(x=2, y=2))
    world.add_entity(Monster(x=6, y=3))

    world.step()
    world.step()


# ---------------------------------------------------------------------------
# WEEK 2: once your monster moves, delete the @skip below and make it pass.
# ---------------------------------------------------------------------------
#
# import pytest
#
# def test_monster_eventually_moves():
#     world = World(width=10, height=6)
#     monster = Monster(x=5, y=3)
#     world.add_entity(monster)
#     start = (monster.x, monster.y)
#
#     for _ in range(20):
#         world.step()
#         if (monster.x, monster.y) != start:
#             return
#
#     pytest.fail("the monster never moved in 20 turns")
