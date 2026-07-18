import pygame
import asyncio


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Spacecraft Puzzle")

from game_manager import GameManager


async def main():
    running = True
    clock = pygame.time.Clock()
    game = GameManager()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game.handle_events(event)
        game.update()
        game.draw(screen)

        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())
