import pygame
import asyncio


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Spacecraft Puzzle")

from game_manager import GameManager
from debug import debug

async def main():
    running = True
    clock = pygame.time.Clock()
    game = GameManager()

    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_x, start_y = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                end_x, end_y = event.pos
                print(f"{start_x}, {start_y}, {end_x - start_x}, {end_y - start_y}")
            
            game.handle_events(event)
        game.update()
        game.draw(screen)

        debug(f"{pygame.mouse.get_pos()}")

        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
