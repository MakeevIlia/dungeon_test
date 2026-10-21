"""Everything that occupies a square and does something on its turn.

The class hierarchy here is the backbone of the whole project:

    Entity              <- knows where it is and how to draw itself
      |- Player         <- acts on your keypresses
      |- Monster        <- decides for itself  (YOU BUILD THIS, week 2)

Add your own subclasses below. Anything that inherits from Entity is
automatically picked up by World.step() -- you never have to register it.
"""
import random

class Entity:
    """Something standing on a square of the dungeon."""

    def __init__(self, x: int, y: int, symbol: str = "?", name: str = "thing") -> None:
        self.x = x
        self.y = y
        self.symbol = symbol
        self.name = name
        self.hp = 10

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def act(self, world) -> None:
        """Take one turn. The base entity is inert -- it just stands there.

        Subclasses override this. Because World.step() calls .act() on
        everything without knowing the type, overriding this method is the
        ONLY thing you need to do to give a creature a personality.
        """
        return None

    # ------------------------------------------------------------- movement

    def move_by(self, world, dx: int, dy: int) -> bool:
        """Try to step by (dx, dy). Returns True if the move happened.

        Blocked by walls and by other entities. Returning a bool rather than
        just moving is deliberate: the caller often wants to know whether the
        move succeeded so it can do something else instead (like attack).
        """
        new_x = self.x + dx
        new_y = self.y + dy
        if world.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r} at ({self.x}, {self.y})>"


class Player(Entity):
    """You. Moves when told to by whatever is driving the game."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, symbol="@", name="you")
        self.hp = 20
        # Set from outside before each turn: (dx, dy), or None to stand still.
        self.pending_move: tuple[int, int] | None = None

    def act(self, world) -> None:
        if self.pending_move is None:
            return
        dx, dy = self.pending_move
        self.pending_move = None
        if not self.move_by(world, dx, dy):
            world.log("You bump into something solid.")


class Monster(Entity):
    """A creature that decides for itself what to do.

    ============================ WEEK 2: YOUR TURN ============================

    Right now this monster stands perfectly still, because act() below does
    nothing. The game runs fine -- it is just boring.

    Your job: make it move. Start with a random step in one of the four
    directions. You will want:

        import random
        dx, dy = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.move_by(world, dx, dy)

    Then, once that works, make it more interesting. Some ideas:
      - only move every other turn, so it feels sluggish
      - move toward the player if it is close enough to notice you
      - log a message when it bumps into a wall

    In WEEK 6 you will replace whatever you write here with real pathfinding,
    so do not over-engineer it. Get something moving.
    ==========================================================================
    """

    def __init__(self, x: int, y: int, symbol: str = "g", name: str = "goblin") -> None:
        super().__init__(x, y, symbol=symbol, name=name)
        self.hp = 5
        self.vision_area = 5
        self.damage = 3
        self.stunned_turns = 0


    def act(self, world) -> None:
        if not(self.stunned_turns):
            for i in world.entities:
                if i.name == "you":
                    player = i 

            enemy_possible_moves = [[-1, 0], [0, 0], [1, 0], [0, 1], [0, -1]]

            dx, dy = random.choice(enemy_possible_moves)

            distance = abs(player.x - self.x) + abs(player.y - self.y)
            print(distance)
            if distance < self.vision_area and distance != 1:
                print(self.name, "sees you, RUN AWAY!")
                dx = 0
                if player.x - self.x > 0:
                    dx = 1
                elif player.x - self.x < 0:
                    dx = -1

                dy = 0 
                if player.y - self.y > 0:
                    dy = 1
                elif player.y - self.y < 0:
                    dy = -1

            elif distance == 1:
                player.hp -= self.damage
                self.stunned_turns = 3
            self.move_by(world, dx, dy)

        else:
            self.stunned_turns -= 1

        

