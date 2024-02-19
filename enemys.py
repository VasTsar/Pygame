import pygame
from sprite_class import Sprite
from main import load_image, tile_height, tile_width


class Enemy(Sprite):

    def __init__(self, pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * tile_width
        self.rect.y = pos[1] * tile_height


class Princess(Enemy):
    image = load_image("princess0.png", color_key=-1)


class Prince(Enemy):
    image = load_image("prince0.png", color_key=-1)


class Boss(Enemy):
    image = load_image("boss0.png", color_key=-1)
