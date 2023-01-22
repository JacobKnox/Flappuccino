import pygame
import colorsys
from PIL import Image

class Background:
    file = 'data/gfx/bg.png'
    pil_sprite = Image.open(file)
    uncolored_sprite = pygame.image.load(file)
    
    def __init__(self):
        self.sprite = pygame.image.load(self.file)
        self.position = 0
        
    def set_sprite(self, tint: float) -> None:  
        copy = self.uncolored_sprite.copy()
        color = colorsys.hsv_to_rgb(tint,1,1)
        copy.fill((color[0]*255, color[1]*255, color[2]*255), special_flags=pygame.BLEND_ADD)
        self.sprite = copy
        
    def resize(self, new_size: tuple[float, float]) -> None:
        self.pil_sprite = self.pil_sprite.resize(new_size)
        mode = self.pil_sprite.mode
        size = self.pil_sprite.size
        data = self.pil_sprite.tobytes()
        self.sprite = pygame.image.fromstring(data, size, mode)
        self.uncolored_sprite = pygame.image.fromstring(data, size, mode)