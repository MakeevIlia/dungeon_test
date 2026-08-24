"""What a renderer has to be able to do.

A Renderer's whole job is to take a World and show it to somebody. It is
allowed to know everything about the World. The World is not allowed to know
anything about it.

There is exactly one renderer right now (terminal). In week 4 we add a second
one that serves the same World to a web browser, and main.py will change by
about one line. That is the payoff for keeping this boundary clean.
"""

from abc import ABC, abstractmethod


class Renderer(ABC):
    """Anything that can display a World."""

    @abstractmethod
    def render(self, world) -> None:
        """Show the current state of the world."""

    def get_command(self) -> str | None:
        """Ask the human what they want to do next.

        Returns a short string like 'w' or 'quit', or None if there is no
        human to ask (a web renderer, for instance, gets commands over HTTP
        instead and just returns None here).
        """
        return None
