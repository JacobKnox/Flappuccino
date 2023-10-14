import pygame
from pygame.image import load


class Button:
    sprite = load('data/gfx/button.png').convert_alpha()

    def __init__(self, index: int, indicator: str = "data/gfx/null_indicator.png") -> None:
        self.price = 5
        self.level = 1
        self.index = index
        self.type_indicator_sprite = load(indicator).convert_alpha()
        self.position = pygame.Vector2()
        self.position.xy = 220 + (self.index*125), 393

    def set_price(self, new_price: int) -> None:
        self.price = new_price
