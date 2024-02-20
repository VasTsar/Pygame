import pygame
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

'''
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
'''