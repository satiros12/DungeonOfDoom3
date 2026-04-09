"""Main entry point for Escape the Dungeon of Doom."""

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)


def main() -> None:
    """Run the game."""
    from src.core.game import Game
    from src.scenes.menu_scene import MenuScene

    logging.info("Starting Escape the Dungeon of Doom...")

    game = Game()
    menu = MenuScene(game)
    game.change_scene(menu)
    game.run()


if __name__ == "__main__":
    main()
