'''from sprite_class import Sprite
from main import load_image
import pygame
from main import all_sprites, all_balconys, all_lianas, tile_width, tile_height, personage, screen, camera


class Frog(Sprite):
    """ Класс лягушки (главного героя, за которого Вы играете)"""
    image = load_image("jaba.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Frog.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * tile_width - self.image.get_width() // 2
        self.rect.y = pos[1] * tile_height - self.image.get_height() // 2
        self.pos = (self.rect.x, self.rect.y)
        self.collisions = [False] * 8

        self.abs_pos = (self.rect.x, self.rect.y)

    def update(self):
        """ Если лягушка еще в небе """
        if (not pygame.sprite.spritecollideany(self, all_balconys)
                and not pygame.sprite.spritecollideany(self, all_lianas)):
            self.rect = self.rect.move(0, 1)

        self.collisions = self.check_collision(all_balconys, screen)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in all_sprites:
            camera.apply(sprite)

    def move_in_direction(self, movement):
        x, y = self.pos
        if movement == "up" and not self.collide_from_direction('up'):
            if pygame.sprite.spritecollideany(personage, all_balconys):
                personage.rect.y -= 50
            elif pygame.sprite.spritecollideany(personage, all_lianas):
                personage.rect.y -= 55
        elif movement == "down":
            if pygame.sprite.spritecollideany(personage, all_lianas):
                personage.rect.y += 55
        elif movement == "left" and not self.collide_from_direction('left'):
            personage.rect.x -= 20
        elif movement == "right" and not self.collide_from_direction('right'):
            personage.rect.x += 20
        for sprite in all_sprites:
            camera.apply(sprite)
'''