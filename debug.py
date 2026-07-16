import pygame
def debug(info,y = 0, x = 0):
	font = pygame.font.Font(None, 20)
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info), True, "white")
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface, "black", debug_rect)
	display_surface.blit(debug_surf, debug_rect)