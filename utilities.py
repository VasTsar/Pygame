import pygame
import sys
import os


def load_image(name, color_key=None):
    """ Функция для загрузки спрайтов """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    """ «Аварийное завершение» """
    pygame.quit()
    sys.exit()


tile_images = {
    'wall': load_image('balcony00.png'),
    'boss': load_image('boss0.png'),
    'wall_boss': load_image('balcony10.png'),
    'ground_boss': load_image('ground0.png'),
    'princess': load_image('princess0.png'),
    'prince': load_image('prince0.png')
}


'''
class Surface(Sprite):
    """ Пусть пока тут полежит"""
    image = load_image("ground0.png", color_key=-1)

    def __init__(self):
        super().__init__(all_sprites, all_balconys)
        self.image = Surface.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем платформу внизу
        self.rect.bottom = height

        self.abs_pos = [self.rect.x, self.rect.y]
'''