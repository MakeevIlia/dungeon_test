"""Tests for the world grid.

These already pass. Run them with:

    pytest

Green output means your environment works. If you break something later in
the semester, these will tell you before your classmate's bot does.
"""

from game.core.entity import Entity
from game.core.world import FLOOR, WALL, World


def test_world_has_the_size_we_asked_for():
    world = World(width=10, height=6)
    assert world.width == 10
    assert world.height == 6
    assert len(world.tiles) == 6
    assert len(world.tiles[0]) == 10


def test_edges_are_walls_and_the_middle_is_not():
    world = World(width=10, height=6)
    assert world.tiles[0][0] == WALL
    assert world.tiles[5][9] == WALL
    assert world.tiles[3][4] == FLOOR


def test_outside_the_map_counts_as_wall():
    world = World(width=10, height=6)
    assert world.is_wall(-1, 3)
    assert world.is_wall(100, 3)
    assert not world.in_bounds(10, 6)


def test_a_square_with_someone_on_it_is_not_walkable():
    world = World(width=10, height=6)
    world.add_entity(Entity(x=4, y=3))
    assert not world.is_walkable(4, 3)
    assert world.is_walkable(5, 3)


def test_entity_at_finds_the_right_one():
    world = World(width=10, height=6)
    goblin = Entity(x=4, y=3, name="goblin")
    world.add_entity(goblin)
    assert world.entity_at(4, 3) is goblin
    assert world.entity_at(1, 1) is None
