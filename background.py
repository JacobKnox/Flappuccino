import pygame
import colorsys


class Background:
    sprite = pygame.image.load('data/gfx/bg.png').convert_alpha()
    uncolored_sprite = pygame.image.load(
        'data/gfx/bg.png').convert_alpha()

    def __init__(self):
        self.position = 0

    def set_sprite(self, tint: float) -> None:
        copy = self.uncolored_sprite.copy()
        color = colorsys.hsv_to_rgb(tint, 1, 1)
        copy.fill((color[0]*255, color[1]*255, color[2]*255),
                  special_flags=pygame.BLEND_ADD)
        self.sprite = copy
