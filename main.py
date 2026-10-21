"""Run the dungeon.

    python main.py

This file wires the three pieces together and does nothing else:

    the World   (the rules)          game/core/
    a Renderer  (how you see it)     game/render/
    the loop    (below)

Notice how little is here. That is the point -- almost all the interesting
code lives behind those two folders, and this file just introduces them to
each other.
"""

from game.core.entity import Monster, Player
from game.core.world import World
from game.render.terminal import TerminalRenderer

# Which key means which direction. Feel free to add arrow keys or vi keys.
MOVES: dict[str, tuple[int, int]] = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0),
    ".": (0, 0),
    "a ": (-3, 0),
    "d ": (3, 0),
    "w ": (0, 3),
    "s ": (0, -3),
}


def build_world() -> tuple[World, Player]:
    """Create the level and everything in it."""
    world = World(width=40, height=15)

    player = Player(x=5, y=5)
    world.add_entity(player)

    # A couple of goblins to keep you company. They do not move yet --
    # that is your week 2 job, in game/core/entity.py.
    world.add_entity(Monster(x=20, y=7))
    world.add_entity(Monster(x=30, y=10, symbol="G", name="big goblin"))

    return world, player


def main() -> None:
    world, player = build_world()
    renderer = TerminalRenderer()

    world.log("You are in a dungeon. It is quiet.")

    while True:
        renderer.render(world)

        command = renderer.get_command()
        if command is None or command == "q":
            print("\nYou leave the dungeon. Goodbye.")
            return

        if command not in MOVES:
            world.log(f"You do not know how to '{command}'.")
            continue

        player.pending_move = MOVES[command]
        world.step()

        if not player.is_alive:
            renderer.render(world)
            print("\nYou died. Better luck next run.")
            return


if __name__ == "__main__":
    main()
