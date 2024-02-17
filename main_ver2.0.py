import os
import pygame
import sys
import argparse
from sprite_class import Sprite


parser = argparse.ArgumentParser()
parser.add_argument("map", type=str, nargs="?", default="map.map")
args = parser.parse_args()
map_file = args.map


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


pygame.init()

size = width, height = 1541, 840
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50
FPS = 50
tile_images = {
    'wall': load_image('balcony0.png'),
    'boss': load_image('boss0.png'),
    'wall_boss': load_image('balcony10.png'),
    'ground_boss': load_image('ground0.png'),
    'princess': load_image('princess0.png'),
    'prince': load_image('prince0.png')
}


# player_image = load_image('jaba.png')


class Surface(pygame.sprite.Sprite):
    """ Класс поверхности (почвы внизу экрана, по которой передвигается лягушка)"""
    image = load_image("ground0.png", color_key=-1)

    def __init__(self):
        super().__init__(all_sprites, all_balconys)
        self.image = Surface.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем платформу внизу
        self.rect.bottom = height

        self.abs_pos = (self.rect.x, self.rect.y)


class Liana(pygame.sprite.Sprite):
    """ Класс лиан, по которым лягушка может залезать на балконы с врагами"""
    image = load_image("liana0.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_lianas)
        self.image = Liana.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])

        self.abs_pos = (self.rect.x, self.rect.y)


class Balcony(pygame.sprite.Sprite):
    """ Класс балконов, по которым ходят враги (принцы и принцессы)"""
    image = load_image("balcony0.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_balconys)
        self.image = Balcony.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])

        self.abs_pos = (self.rect.x, self.rect.y)


class BossBalcony(pygame.sprite.Sprite):
    """ Класс балконов в зоне босса, по которым ходят враги (принцы и принцессы)"""
    image = load_image("balcony10.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_balconys)
        self.image = BossBalcony.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])

        self.abs_pos = (self.rect.x, self.rect.y)


class Tile(Sprite):
    def __init__(self, tile_type, pos):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])
        self.abs_pos = (self.rect.x, self.rect.y)


class Camera:
    """ Камера """

    def __init__(self):
        self.dx = 0
        self.dy = 1

    # Сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx // 2
        obj.rect.y += self.dy // 2
        return obj.rect.x, obj.rect.y

    # Позиционировать камеру на объекте target
    def update(self, target):
        self.dx = (personage.rect.x - self.dx - width / 2 - personage.abs_pos[0]) / 22

        # self.dy = (personage.rect.y - self.dy - height / 2) / 15


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


class Princess(pygame.sprite.Sprite):
    image = load_image("princess0.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_enemys)
        self.image = Princess.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Prince(pygame.sprite.Sprite):
    image = load_image("prince0.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_enemys)
        self.image = Prince.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def terminate():
    """ «Аварийное завершение» """
    pygame.quit()
    sys.exit()


def start_screen():
    """ Функция для стартового экрана (появляется прu запуске, исчезает при нажатии на клавишу клавиатуры или мыши)"""
    intro_text = ["Стартовый экран", "",
                  "здесь будет текст"]

    fon = pygame.transform.scale(load_image('start0.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
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


all_sprites = pygame.sprite.Group()
all_balconys = pygame.sprite.Group()
all_lianas = pygame.sprite.Group()
all_enemys = pygame.sprite.Group()
personage = None

# surface = Surface()

clock = pygame.time.Clock()
start_screen()
camera = Camera()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Balcony((x, y))
            elif level[y][x] == '(':
                Liana((x, y))
            elif level[y][x] == '|':
                Tile('boss', (x, y))
            elif level[y][x] == '%':
                BossBalcony((x, y))
            elif level[y][x] == '*':
                Tile('ground_boss', (x, y))
            elif level[y][x] == '!':
                Tile('princess', (x, y))
            elif level[y][x] == '?':
                Tile('prince', (x, y))
            elif level[y][x] == '@':
                new_player = Frog((x, y))
                level[y][x] = "."
    return new_player, x, y


if __name__ == '__main__':
    level_map = load_level(map_file)
    personage, max_x, max_y = generate_level(level_map)
    camera.update(personage)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if personage:
                    if event.key == pygame.K_LEFT:
                        personage.move_in_direction('left')
                    elif event.key == pygame.K_RIGHT:
                        personage.move_in_direction('right')
                    if pygame.sprite.spritecollideany(personage, all_balconys):
                        if event.key == pygame.K_SPACE:
                            personage.move_in_direction('up')
                    elif pygame.sprite.spritecollideany(personage, all_lianas):
                        if event.key == pygame.K_SPACE:
                            personage.move_in_direction('up')
                        elif event.key == pygame.K_DOWN:
                            personage.move_in_direction('down')

        screen.blit(load_image('fon0.png'), (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
