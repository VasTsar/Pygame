from main import *


class Frog(pygame.sprite.Sprite):
    """ Класс лягушки (главного героя, за которого Вы играете)"""
    image = load_image("jaba.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Frog.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        """ Если лягушка еще в небе """
        if not pygame.sprite.spritecollideany(self, all_balconys):
            self.rect = self.rect.move(0, 1)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in all_sprites:
            camera.apply(sprite)