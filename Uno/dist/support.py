import pygame

def blit_text(text, color, pos, font):
    display_surface = pygame.display.get_surface()
    overlay_txt = font.render(text, False, color)
    overlay_txt_rect = overlay_txt.get_rect(center= (pos))
    display_surface.blit(overlay_txt, overlay_txt_rect)

def blit_text_shadow(text, color, pos, font, back_color='black'):
    blit_text(text, back_color, [pos[0] + 1, pos[1] + 1], font)
    blit_text(text, back_color, [pos[0] - 1, pos[1] - 1], font)
    blit_text(text, color, pos, font)