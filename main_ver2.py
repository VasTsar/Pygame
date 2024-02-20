import pygame
import argparse
from sprite_class import Sprite
from enemys import Prince, Princess, Boss
from const import G, FPS, size, width, height, tile_width, tile_height, score
from utilities import load_image, terminate, tile_images


parser = argparse.ArgumentParser()
parser.add_argument("map", type=str, nargs="?", default="map.map")
args = parser.parse_args()
map_file = args.map


pygame.init()
screen = pygame.display.set_mode(size)


class Liana(Sprite):
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

        self.abs_pos = [self.rect.x, self.rect.y]


class Balcony(Sprite):
    """ Класс балконов, по которым ходят враги (принцы и принцессы)"""
    image = load_image("balcony00.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites, all_balconys)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos[0], tile_height * pos[1])

        self.abs_pos = [self.rect.x, self.rect.y]


class BossBalcony(Balcony):
    """ Класс балконов в зоне босса, по которым ходят враги (принцы и принцессы)"""
    image = load_image("balcony10.png", color_key=-1)


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
        self.dy = 0

    # Сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        return obj.rect.x, obj.rect.y

    # Позиционировать камеру на объекте target
    def update(self, target):
        pass
        # self.dx = (personage.rect.x - self.dx - width / 2 - personage.abs_pos[0]) / 22
        # self.dy = (personage.rect.y - self.dy - height / 2) / 15


class Frog(Sprite):
    """ Класс лягушки (главного героя, за которого Вы играете)"""
    image = load_image("jaba.png", color_key=-1)

    def __init__(self, pos, camera, score):
        super().__init__(all_sprites)
        self.image = Frog.image
        self.camera = camera
        self.score = score
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * tile_width - self.image.get_width() // 2
        self.rect.y = pos[1] * tile_height - self.image.get_height() // 2
        self.pos = (self.rect.x, self.rect.y)
        self.collisions = [False] * 8
        self.velocity_y = 0

        self.abs_pos = [self.rect.x, self.rect.y]

    def update(self):
        """ Если лягушка еще в небе """
        if (not pygame.sprite.spritecollideany(self, all_balconys)
                and not pygame.sprite.spritecollideany(self, all_lianas)):
            self.rect = self.rect.move(0, int(self.velocity_y))
            self.velocity_y = min(10, self.velocity_y + G)
        else:
            self.velocity_y = 0

        if pygame.sprite.spritecollideany(self, all_enemys) and self.collide_from_direction('down'):
            for enemy in pygame.sprite.spritecollide(self, all_enemys, dokill=True, collided=None):
                self.score += 5
                print(self.score)

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
            if pygame.sprite.spritecollideany(self, all_balconys):
                self.velocity_y = -15
                self.rect.y -= 20
                self.abs_pos[1] -= 50
                self.camera.dx = 0
            elif pygame.sprite.spritecollideany(self, all_lianas):
                self.rect.y -= 10
                self.abs_pos[1] -= 10
                self.camera.dx = 0
        elif movement == "down" and not self.collide_from_direction('down'):
            if pygame.sprite.spritecollideany(self, all_lianas):
                self.rect.y += 10
                self.abs_pos[1] += 10
                self.camera.dx = 0
        elif movement == "left" and not self.collide_from_direction('left'):
            self.rect.x -= 10
            self.abs_pos[0] -= 10
            self.camera.dx = 10
        elif movement == "right" and not self.collide_from_direction('right'):
            self.rect.x += 10
            self.abs_pos[0] += 10
            self.camera.dx = -10
        else:
            self.camera.dx = 0
        for sprite in all_sprites:
            self.camera.apply(sprite)


def start_screen():
    """ Функция для стартового экрана (появляется прu запуске, исчезает при нажатии на клавишу клавиатуры или мыши)"""
    intro_text = ["Стартовый экран", "",
                  "здесь будет текст"]

    fon = pygame.transform.scale(load_image('start0.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('blue'))
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
all_bosses = pygame.sprite.Group()
personage = None

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
                Boss((x, y), all_sprites, all_bosses)
            elif level[y][x] == '%':
                BossBalcony((x, y))
            elif level[y][x] == '*':
                Tile('ground_boss', (x, y))
            elif level[y][x] == '!':
                Princess((x, y), all_sprites, all_enemys)
            elif level[y][x] == '?':
                Prince((x, y), all_sprites, all_enemys)
            elif level[y][x] == '@':
                new_player = Frog((x, y), camera, score)
                level[y][x] = "."
    return new_player, x, y


if __name__ == '__main__':
    level_map = load_level(map_file)
    personage, max_x, max_y = generate_level(level_map)
    camera.update(personage)
    move_x_direction = None
    move_y_direction = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_x_direction = 'left'
                    # personage.move_in_direction('left')
                elif event.key == pygame.K_RIGHT:
                    move_x_direction = 'right'
                    # personage.move_in_direction('right')
                if pygame.sprite.spritecollideany(personage, all_lianas):
                    if event.key == pygame.K_SPACE:
                        move_y_direction = 'up'
                        # personage.move_in_direction('up')
                    elif event.key == pygame.K_DOWN:
                        move_y_direction = 'down'
                        # personage.move_in_direction('down')
                elif pygame.sprite.spritecollideany(personage, all_balconys):
                    if event.key == pygame.K_SPACE:
                        personage.move_in_direction('up')
                else:
                    move_y_direction = None

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    move_x_direction = None
                elif event.key == pygame.K_SPACE or event.key == pygame.K_DOWN:
                    move_y_direction = None
        if move_x_direction:
            personage.move_in_direction(move_x_direction)
        if move_y_direction:
            personage.move_in_direction(move_y_direction)

        screen.blit(load_image('fon0.png'), (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
