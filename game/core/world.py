"""The world: a grid of tiles, plus the things standing on it.

This module is PURE LOGIC. It never prints anything and never talks to the
network. That is not an accident -- it is the single most important design
decision in this codebase. Because the rules of the game know nothing about
how they are displayed, we can show the same game in a terminal (week 1),
in a web browser (week 4), and to a robot player (week 12) without changing
a single line in this folder.

If you ever find yourself wanting to write print() in game/core/, stop.
That belongs in game/render/.
"""

WALL = "#"
FLOOR = "."


class World:
    """A dungeon level: the tile grid and every entity standing on it."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # A 2D grid, indexed as tiles[y][x]. Y FIRST. This trips up everyone
        # at least once -- think "which row, then which column".
        self.tiles: list[list[str]] = [
            [FLOOR for _ in range(width)] for _ in range(height)
        ]
        self.entities: list = []
        self.messages: list[str] = []
        self._build_starter_room()

    # ---------------------------------------------------------------- setup

    def _build_starter_room(self) -> None:
        """Wall off the outer edge, leaving open floor inside.

        WEEK 3 replaces this with real procedural generation: random rooms
        joined by corridors. For now, one big boring box.
        """
        for x in range(self.width):
            self.tiles[0][x] = WALL
            self.tiles[self.height - 1][x] = WALL
        for y in range(self.height):
            self.tiles[y][0] = WALL
            self.tiles[y][self.width - 1] = WALL

    def add_entity(self, entity) -> None:
        self.entities.append(entity)

    # ------------------------------------------------------------- querying

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x: int, y: int) -> bool:
        if not self.in_bounds(x, y):
            return True
        return self.tiles[y][x] == WALL

    def entity_at(self, x: int, y: int):
        """Return the entity standing at (x, y), or None if the square is empty."""
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        return None

    def is_walkable(self, x: int, y: int) -> bool:
        """True if something could step onto this square right now."""
        return not self.is_wall(x, y) and self.entity_at(x, y) is None

    def log(self, message: str) -> None:
        """Record something worth telling the player about."""
        self.messages.append(message)

    # ---------------------------------------------------------------- turns

    def step(self) -> None:
        """Advance the world by one turn: every entity gets to act, in order.

        Note what happens here: we call .act() on every entity without
        checking what kind of entity it is. A Player reads your keyboard, a
        Monster decides for itself -- and this loop does not care. That is
        polymorphism, and it is why you can add new kinds of creature later
        without ever editing this method.
        """
        for entity in list(self.entities):
            entity.act(self)
