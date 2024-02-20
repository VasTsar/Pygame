import pygame


class Sprite(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = None
        self.collision = [False] * 9

    def draw_collisions_points(self, screen):
        ''' Отрисовывает точки возможных стоклновений '''
        # pygame.draw.rect(screen, 'white', self.rect, 2)
        self.draw_point(screen, self.rect.topleft, self.collision[0])
        self.draw_point(screen, self.rect.topright, self.collision[1])
        self.draw_point(screen, self.rect.bottomleft, self.collision[2])
        self.draw_point(screen, self.rect.bottomright, self.collision[3])

        self.draw_point(screen, self.rect.midleft, self.collision[4])
        self.draw_point(screen, self.rect.midright, self.collision[5])
        self.draw_point(screen, self.rect.midtop, self.collision[6])
        self.draw_point(screen, self.rect.midbottom, self.collision[7])

        self.draw_point(screen, self.rect.center, self.collision[8])

    def draw_point(self, screen, pos, collision):
        ''' Задает нужный цвет точке в зависимости от того, сталкивается ли с чем-то объект в данный момент '''
        if not collision:
            pygame.draw.circle(screen, 'green', pos, 3)
        else:
            pygame.draw.circle(screen, 'red', pos, 3)

    def check_collision(self, sprite_group, screen):
        ''' Проверка столкновеня объекта с чем-либо'''
        self.draw_collisions_points(screen)
        points_list = [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright,
              self.rect.midleft, self.rect.midright, self.rect.midtop, self.rect.midbottom, self.rect.center]
        self.collision = [False] * 9
        for sprite_from_group in sprite_group:
            for num, i in enumerate(points_list):
                if sprite_from_group.rect.collidepoint(points_list[num]):
                    self.collision[num] = True
                    break

            '''self.collision[0] = sprite_from_group.spritecollideany(self.rect.topleft)
            self.collision[1] = sprite_from_group.spritecollideany(self.rect.topright)
            self.collision[2] = sprite_from_group.spritecollideany(self.rect.bottomleft)
            self.collision[3] = sprite_from_group.spritecollideany(self.rect.bottomright)

            self.collision[4] = sprite_from_group.spritecollideany(self.rect.midleft)
            self.collision[5] = sprite_from_group.collideany(self.rect.midright)
            self.collision[6] = sprite_from_group.collideany(self.rect.midtop)
            self.collision[7] = sprite_from_group.collideany(self.rect.midbottom)

            self.collision[8] = sprite_from_group.collideany(self.rect.center)'''

    def collide_from_direction(self, direction):
        ''' Определяет с какой стороны происходит столкновение '''
        directions_dict = {'up': [0, 1, 6],
                           'left': [0, 4],
                           'right': [1, 5],
                           'down': [2, 3, 7]}
        collides_from_direction = [self.collision[x] for x in directions_dict[direction]]
        return any(collides_from_direction)

    def get_event(self, event):
        pass