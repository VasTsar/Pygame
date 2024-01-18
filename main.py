import os
import pygame

pygame.init()

size = width, height = 800, 400
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
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


class Platform(pygame.sprite.Sprite):
    image = load_image("ground0.png", color_key=-1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Platform.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем платформу внизу
        self.rect.bottom = height
        
        
class Liana(pygame.sprite.Sprite):
    image = load_image("liana0.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_lianas)
        self.image = Liana.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Balcony(pygame.sprite.Sprite):
    image = load_image("balcony0.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_platforms)
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        self.image.fill('grey')
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Frog(pygame.sprite.Sprite):
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
        # если еще в небе
        if not pygame.sprite.collide_mask(self, platform):
            self.rect = self.rect.move(0, 1)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in sprite_group:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()
all_platforms = pygame.sprite.Group()
all_lianas = pygame.sprite.Group()
personage = None

platform = Platform()

clock = pygame.time.Clock()

camera = Camera()
camera.update(personage)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    Liana(event.pos)
                '''else:
                    Platform(event.pos)'''
            elif event.button == 3:
                if personage is None:
                    personage = Frog(event.pos)
                else:
                    personage.rect.topleft = event.pos
        if event.type == pygame.KEYDOWN:
            if personage:
                if event.key == pygame.K_LEFT:
                    personage.rect.x -= 10
                elif event.key == pygame.K_RIGHT:
                    personage.rect.x += 10
                if pygame.sprite.spritecollideany(personage, all_lianas):
                    if event.key == pygame.K_UP:
                        personage.rect.y -= 10
                    elif event.key == pygame.K_DOWN:
                        personage.rect.y += 10

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()



'''while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    Liana(event.pos)
                else:
                    Platform(event.pos)
            elif event.button == 3:
                if personage is None:
                    personage = Liana(event.pos)
                else:
                    personage.rect.topleft = event.pos
        if event.type == pygame.KEYDOWN:
            if personage:
                if event.key == pygame.K_LEFT:
                    personage.rect.x -= 10
                elif event.key == pygame.K_RIGHT:
                    personage.rect.x += 10
                if pygame.sprite.spritecollideany(personage, all_lianas):
                    if event.key == pygame.K_UP:
                        personage.rect.y -= 10
                    elif event.key == pygame.K_DOWN:
                        personage.rect.y += 10'''
