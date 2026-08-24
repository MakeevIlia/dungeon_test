"""Draws the dungeon as text in your terminal.

This is the week 1 renderer. It is deliberately simple, and it is the only
file in the project allowed to call print().
"""

from game.render.base import Renderer


class TerminalRenderer(Renderer):
    """Prints the world as a block of characters."""

    def render(self, world) -> None:
        # Build a character grid, then stamp the entities on top of it.
        # We copy the tiles first so we never accidentally modify the world
        # while drawing it -- a renderer must not change the game.
        grid = [list(row) for row in world.tiles]

        for entity in world.entities:
            if world.in_bounds(entity.x, entity.y) and entity.is_alive:
                grid[entity.y][entity.x] = entity.symbol

        print("\n" * 2)
        for row in grid:
            print("".join(row))

        player = next((e for e in world.entities if e.symbol == "@"), None)
        if player is not None:
            print(f"\nHP: {player.hp}")

        # Show anything that happened since we last drew, then clear it.
        for message in world.messages:
            print(message)
        world.messages.clear()

        print("\nmove: w a s d   |   wait: .   |   quit: q")

    def get_command(self) -> str | None:
        try:
            return input("> ").strip().lower()
        except EOFError:
            # Input ran out (piped input, or Ctrl-D). Treat it as quitting.
            return "q"


# ---------------------------------------------------------------------------
# WEEK 1 EXERCISE
#
# The dungeon currently looks like a plain box of # and . characters.
# Make it yours:
#
#   1. Open game/core/world.py and change WALL to a different character.
#      Try "█" or "▓" or "%". Run the game again and see it change.
#   2. Change the size of the map in main.py.
#   3. Harder, optional: colour the walls. Terminals understand special
#      escape codes -- "\033[90m" starts grey text and "\033[0m" ends it.
#      So "\033[90m#\033[0m" prints a grey #.
#
# Then commit and push. That is week 1 done.
# ---------------------------------------------------------------------------
