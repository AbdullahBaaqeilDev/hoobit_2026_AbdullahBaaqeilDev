import asyncio
import pygame
import ai_system


pygame.init()
screen = pygame.display.set_mode((850, 500))
pygame.display.set_caption("AI Game State Tester")
font = pygame.font.SysFont("Consolas", 20)  # Using a monospaced font for cleaner alignment
clock = pygame.time.Clock()

async def main():
    user_input = "Please change course, we are going to crash!"
    running = True

    while running:
        # 1. Input Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Fire off the async API call
                    ai_system.ask_ai(user_input)
                
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        # 2. Draw Interface
        screen.fill((20, 20, 30))  # Slate background

        # User Input Box
        input_title = font.render("Type a prompt to the Rogue AI:", True, (150, 150, 150))
        input_surface = font.render(f"> {user_input}", True, (255, 255, 255))
        screen.blit(input_title, (40, 40))
        screen.blit(input_surface, (40, 70))

        # Horizontal Divider
        pygame.draw.line(screen, (50, 50, 70), (40, 120), (810, 120), 2)

        # Retrieve parsed AI state values
        ai_message = ai_system.ai_data.get("text", "")
        anger_val = ai_system.ai_data.get("anger", 0.0)
        progress_val = ai_system.ai_data.get("convinced_progress", 0.0)
        will_help = ai_system.ai_data.get("convinced_progress_to_help_human", False)

        # Render structured outputs
        # Color codes based on states
        anger_color = (255, 100, 100) if anger_val > 0.5 else (200, 200, 200)
        trust_color = (100, 150, 255) if progress_val > 0.5 else (200, 200, 200)
        status_color = (255, 255, 0) if ai_system.is_thinking else (100, 255, 100)

        # Output Text (UI rendering)
        status_title = font.render(f"STATUS: {'[THINKING...]' if ai_system.is_thinking else '[READY]'}", True, status_color)
        msg_surface = font.render(f"AI Message: \"{ai_message}\"", True, (255, 255, 255))
        anger_surface = font.render(f"ai_data['anger']: {anger_val} ({int(anger_val * 100)}%)", True, anger_color)
        progress_surface = font.render(f"ai_data['convinced_progress']: {progress_val} ({int(progress_val * 100)}%)", True, trust_color)
        help_surface = font.render(f"ai_data['convinced_progress_to_help_human']: {will_help}", True, (100, 255, 100) if will_help else (255, 100, 100))

        # Position elements on screen
        screen.blit(status_title, (40, 140))
        screen.blit(msg_surface, (40, 180))
        screen.blit(anger_surface, (40, 240))
        screen.blit(progress_surface, (40, 280))
        screen.blit(help_surface, (40, 320))

        # Quick Instructions at bottom
        hint_surface = font.render("Press [ENTER] to send transmission to Groq.", True, (100, 100, 120))
        screen.blit(hint_surface, (40, 430))

        pygame.display.flip()
        
        # Safe game-loop delay for Pygbag WASM compilation
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())