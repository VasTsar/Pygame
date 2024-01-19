import os
import pygame
import sys

pygame.init()

size = width, height = 1541, 840
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50
FPS = 50


def load_image(name, color_key=None):
    ''' Функция для загрузки спрайтов  '''
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


class Surface(pygame.sprite.Sprite):
    ''' Класс поверхности (почвы внизу экрана, по которой передвигается лягушка)'''
    image = load_image("ground0.png", color_key=-1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Surface.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем платформу внизу
        self.rect.bottom = height
        
        
class Liana(pygame.sprite.Sprite):
    ''' Класс лиан, по которым лягушка может залезать на балконы с врагами'''
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
    ''' Класс балконов, по которым ходят враги (принцы и принцессы)'''
    image = load_image("balcony0.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_balconys)
        self.image = Balcony.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Camera:
    ''' Камера '''
    # не работает
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


class Frog(pygame.sprite.Sprite):
    ''' Класс лягушки (главного героя, за которого Вы играете)'''
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
        if not pygame.sprite.collide_mask(self, all_balconys):
            self.rect = self.rect.move(0, 1)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in all_sprites:
            camera.apply(sprite)


def terminate():
    ''' «Аварийное завершение»'''
    pygame.quit()
    sys.exit()


def start_screen():
    ''' Функция для стартового экрана (появляется пр запуске, исчезает при нажатии на клавишу клавиатуры или мыши)'''
    intro_text = ["Стартовый экран", "",
                  "здесь будет текст"]

    fon = pygame.transform.scale(load_image('start0.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()
all_balconys = pygame.sprite.Group()
all_lianas = pygame.sprite.Group()
personage = None

surface = Surface()

clock = pygame.time.Clock()
start_screen()
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
                else:
                    Balcony(event.pos)
            elif event.button == 3:
                if personage is None:
                    personage = Frog(event.pos)
                else:
                    personage.rect.topleft = event.pos
        if event.type == pygame.KEYDOWN:
            if personage:
                if event.key == pygame.K_LEFT:
                    personage.rect.x -= 20
                elif event.key == pygame.K_RIGHT:
                    personage.rect.x += 20
                if pygame.sprite.spritecollideany(personage, all_lianas):
                    if event.key == pygame.K_UP:
                        personage.rect.y -= 25

    screen.blit(load_image('fon0.png'), (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
