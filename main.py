import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    else:
        image = image.convert_alpha()

    return image


def start_screen():
    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    pygame.draw.rect(screen, (140, 97, 48), (300, 150, 400, 100))
    pygame.draw.rect(screen, (140, 97, 48), (300, 350, 400, 100))
    pygame.draw.rect(screen, (140, 97, 48), (300, 550, 400, 100))

    text1 = font.render('начать игру', True, (217, 188, 156))
    text2 = font.render('продолжить игру', True, (217, 188, 156))
    text3 = font.render("результаты", True, (217, 188, 156))

    screen.blit(text1, (370, 170))
    screen.blit(text2, (320, 370))
    screen.blit(text3, (370, 570))

    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            if 300 <= mouse[0] <= 700 and 150 <= mouse[1] <= 250:
                pygame.draw.rect(screen, (140, 150, 48), (300, 150, 400, 100))
                text1 = font.render('начать игру', True, (217, 188, 156))
                screen.blit(text1, (370, 170))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            else:
                pygame.draw.rect(screen, (140, 97, 48), (300, 150, 400, 100))
                text1 = font.render('начать игру', True, (217, 188, 156))
                screen.blit(text1, (370, 170))

            if 300 <= mouse[0] <= 700 and 350 <= mouse[1] <= 450:
                pygame.draw.rect(screen, (140, 150, 48), (300, 350, 400, 100))
                text2 = font.render('продолжить игру', True, (217, 188, 156))
                screen.blit(text2, (320, 370))
            else:
                pygame.draw.rect(screen, (140, 97, 48), (300, 350, 400, 100))
                text2 = font.render('продолжить игру', True, (217, 188, 156))
                screen.blit(text2, (320, 370))

            if 300 <= mouse[0] <= 700 and 550 <= mouse[1] <= 650:
                pygame.draw.rect(screen, (140, 150, 48), (300, 550, 400, 100))
                text3 = font.render("результаты", True, (217, 188, 156))
                screen.blit(text3, (370, 570))
            else:
                pygame.draw.rect(screen, (140, 97, 48), (300, 550, 400, 100))
                text3 = font.render("результаты", True, (217, 188, 156))
                screen.blit(text3, (370, 570))

            if event.type == pygame.QUIT:
                pygame.terminate()
        pygame.display.flip()
        clock.tick(FPS)


class Cell:
    """
    size - размер клетки в пикселях
    cell_type - тип клетки целочисленный
    y, x - координаты клетки в пикселях
    image - картинка клетки (поверхность)
    """

    size = 75

    def __init__(self, cell_type, y, x):
        self.cell_type = cell_type
        self.size = Cell.size
        self.y = y
        self.x = x

        if self.cell_type == 0:
            self.image = load_image('трава.png')
        elif self.cell_type == 1:
            self.image = load_image('камень.png')

        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def __str__(self):
        if self.cell_type == 0:
            return 'grass'

        elif self.cell_type == 1:
            return 'stone'

    def __repr__(self):
        if self.cell_type == 0:
            return 'grass'

        elif self.cell_type == 1:
            return 'stone'


class Field:
    """
    cell_size - размер клетки целочисленный
    team1 - словарь с юнитами и их координатами для первой команды
    team2 - словарь с юнитами и их координатами для второй команды

    active_ch - наличие активного персонажа на карте
    attacked - была ли произведена атака
    (для предотвращения множественных выборов юнитов из-за того, что после каждого клика по полю проверяются все юниты)

    active_ch_x, active_ch_y - координаты в номерах клеток поля
    field_map - список из объектов cell, создающийся по ранее сгенерированному текстовому файлу
    """

    def __init__(self, filename):
        filename = "data/" + filename + '.txt'
        self.cell_size = Cell.size

        self.team1 = {}
        self.team2 = {}

        self.active_ch = False
        self.attacked = False
        self.active_ch_x = 0
        self.active_ch_y = 0

        with open(filename, 'r') as map_file:
            self.field_map = list(map(list, map(str.rstrip, map_file.readlines())))

        for y in range(len(self.field_map)):
            for x in range(len(self.field_map[0])):
                self.field_map[y][x] = Cell(int(self.field_map[y][x]), y * self.cell_size, x * self.cell_size)

    """
    screen - экран для отображения
    picked - переменная, проверяющая, выбран ли юнит
    x_picked, y_picked - координаты выбранного юнита в номерах клеток поля
    """

    def render(self, screen, picked, x_picked=0, y_picked=0):

        for field_y in range(len(self.field_map)):
            for field_x in range(len(self.field_map[0])):
                screen.blit(self.field_map[field_y][field_x].image, (self.field_map[field_y][field_x].x,
                                                                     self.field_map[field_y][field_x].y))
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (self.field_map[field_y][field_x].x, self.field_map[field_y][field_x].y,
                                  self.cell_size, self.cell_size), 1)

        if picked:

            if x_picked - 1 >= 0 and y_picked - 1 >= 0:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked - 1][x_picked - 1].x,
                                  self.field_map[y_picked - 1][x_picked - 1].y, self.cell_size, self.cell_size), 1)

            if y_picked - 1 >= 0:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked - 1][x_picked].x, self.field_map[y_picked - 1][x_picked].y,
                                  self.cell_size, self.cell_size), 1)

            if y_picked - 1 >= 0 and x_picked + 1 < len(self.field_map[0]):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked - 1][x_picked + 1].x,
                                  self.field_map[y_picked - 1][x_picked + 1].y, self.cell_size, self.cell_size), 1)

            if x_picked - 1 >= 0:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked][x_picked - 1].x, self.field_map[y_picked][x_picked - 1].y,
                                  self.cell_size, self.cell_size), 1)

            if x_picked + 1 < len(self.field_map[0]):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked][x_picked + 1].x, self.field_map[y_picked][x_picked + 1].y,
                                  self.cell_size, self.cell_size), 1)

            if x_picked - 1 >= 0 and y_picked + 1 < len(self.field_map):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked + 1][x_picked - 1].x,
                                  self.field_map[y_picked + 1][x_picked - 1].y, self.cell_size, self.cell_size), 1)

            if y_picked + 1 < len(self.field_map):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked + 1][x_picked].x, self.field_map[y_picked + 1][x_picked].y,
                                  self.cell_size, self.cell_size), 1)

            if y_picked + 1 < len(self.field_map) and x_picked + 1 < len(self.field_map[0]):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked + 1][x_picked + 1].x,
                                  self.field_map[y_picked + 1][x_picked + 1].y, self.cell_size, self.cell_size), 1)

    """
    возвращает позицию мыши в номерах клеток поля
    """

    def get_cell(self, mouse_pos):

        if mouse_pos[0] < len(self.field_map) * self.cell_size \
                and mouse_pos[1] <= len(self.field_map[0]) * self.cell_size:
            x = mouse_pos[0] // self.cell_size
            y = mouse_pos[1] // self.cell_size
            return x, y

        else:
            return None


class Knight1(pygame.sprite.Sprite):
    """
    field - поле, на котором создаются воины
    image - картинка воина
    rect.x, rect.y - координаты модельки воина в пикселях
    field_x, field_y - координаты воина в номерах клеток
    picked - выбран ли юнит
    health - количество здоровья
    mouse_pos_x, mouse_pos_y - позиция мыши при ходе в номерах клеток
    """

    def __init__(self, field, x, y, *group, ):
        super().__init__(*group)
        self.image = load_image('knight.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            field.cell_size * x + field.cell_size // 4, field.cell_size * y + field.cell_size // 4

        self.field = field
        self.field_x = x
        self.field_y = y

        self.field.team1[self] = (self.field_x, self.field_y)
        self.picked = False

        self.health = 10
        self.alive = True

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:

            mouse_pos_x = self.field.get_cell(args[0].pos)[0]
            mouse_pos_y = self.field.get_cell(args[0].pos)[1]

            if mouse_pos_x == self.field_x and mouse_pos_y == self.field_y \
                    and not self.field.active_ch and not self.field.attacked and self.alive:
                self.picked = True
                self.field.active_ch = True
                self.field.active_ch_x = mouse_pos_x
                self.field.active_ch_y = mouse_pos_y

            if self.picked and (mouse_pos_x, mouse_pos_y) != (self.field_x, self.field_y):

                if (mouse_pos_x, mouse_pos_y) not in self.field.team1.values() and (mouse_pos_x, mouse_pos_y) \
                        not in self.field.team2.values():

                    if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                        self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                   -((self.field_y - mouse_pos_y) * Cell.size))
                        self.field.team1[self] = (mouse_pos_x, mouse_pos_y)

                        self.field_x = mouse_pos_x
                        self.field_y = mouse_pos_y
                        self.picked = False
                        self.field.active_ch = False

                elif (mouse_pos_x, mouse_pos_y) not in self.field.team1.values() and (mouse_pos_x, mouse_pos_y) \
                        in self.field.team2.values():

                    if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                        attack_x = mouse_pos_x
                        attack_y = mouse_pos_y

                        attacked_ch = None

                        for key, val in self.field.team2.items():
                            if val == (attack_x, attack_y):
                                attacked_ch = key
                                break

                        if attacked_ch.alive:
                            attacked_ch.health -= 4
                            if attacked_ch.health <= 0:
                                attacked_ch.image = pygame.transform.flip(attacked_ch.image, False, True)
                                attacked_ch.alive = False

                            self.picked = False
                            self.field.active_ch = False
                            self.field.attacked = True

                        else:
                            self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                       -((self.field_y - mouse_pos_y) * Cell.size))
                            self.field.team1[self] = (mouse_pos_x, mouse_pos_y)

                            self.field_x = mouse_pos_x
                            self.field_y = mouse_pos_y
                            self.picked = False
                            self.field.active_ch = False


class Knight2(pygame.sprite.Sprite):

    def __init__(self, field, x, y, *group, ):
        super().__init__(*group)
        self.image = pygame.transform.flip(load_image('knight.png', -1), True, False)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            field.cell_size * x + field.cell_size // 4, field.cell_size * y + field.cell_size // 4

        self.field = field
        self.field_x = x
        self.field_y = y

        self.field.team2[self] = (self.field_x, self.field_y)
        self.picked = False

        self.health = 10
        self.alive = True

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:

            mouse_pos_x = self.field.get_cell(args[0].pos)[0]
            mouse_pos_y = self.field.get_cell(args[0].pos)[1]

            if mouse_pos_x == self.field_x and mouse_pos_y == self.field_y \
                    and not self.field.active_ch and not self.field.attacked and self.alive:
                self.picked = True
                self.field.active_ch = True
                self.field.active_ch_x = mouse_pos_x
                self.field.active_ch_y = mouse_pos_y

            if self.picked and (mouse_pos_x, mouse_pos_y) != (self.field_x, self.field_y):

                if (mouse_pos_x, mouse_pos_y) not in self.field.team2.values() and (mouse_pos_x, mouse_pos_y) \
                        not in self.field.team1.values():

                    if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                        self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                   -((self.field_y - mouse_pos_y) * Cell.size))
                        self.field.team2[self] = (mouse_pos_x, mouse_pos_y)

                        self.field_x = mouse_pos_x
                        self.field_y = mouse_pos_y
                        self.picked = False
                        self.field.active_ch = False

                elif (mouse_pos_x, mouse_pos_y) not in self.field.team2.values() and (mouse_pos_x, mouse_pos_y) \
                        in self.field.team1.values():
                    attack_x = mouse_pos_x
                    attack_y = mouse_pos_y

                    if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                        attacked_ch = None

                        for key, val in self.field.team1.items():
                            if val == (attack_x, attack_y):
                                attacked_ch = key
                                break

                        if attacked_ch.alive:
                            attacked_ch.health -= 4
                            if attacked_ch.health <= 0:
                                attacked_ch.image = pygame.transform.flip(attacked_ch.image, False, True)
                                attacked_ch.alive = False

                            self.picked = False
                            self.field.active_ch = False
                            self.field.attacked = True

                        else:
                            self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                       -((self.field_y - mouse_pos_y) * Cell.size))
                            self.field.team1[self] = (mouse_pos_x, mouse_pos_y)

                            self.field_x = mouse_pos_x
                            self.field_y = mouse_pos_y
                            self.picked = False
                            self.field.active_ch = False


clock = pygame.time.Clock()
FPS = 60
pygame.init()
pygame.display.set_caption('Game')
screen_size = WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode(screen_size)
picture = load_image('trash.png')
pygame.display.set_icon(picture)
font = pygame.font.Font('data/21063.otf', 36)


if __name__ == '__main__':
    start_screen()
    field = Field('generation1')
    knights = pygame.sprite.Group()
    for i in range(1, 9):
        knight = Knight1(field, 2, i, knights)
    for i in range(1, 9):
        knight = Knight2(field, 7, i, knights)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                knights.update(event)
                field.attacked = False

                sec_win = True
                for elem in field.team1:
                    if elem.alive:
                        sec_win = False

                if sec_win:
                    print('победила вторая команда')
                    running = False

                first_win = True
                for elem in field.team2:
                    if elem.alive:
                        first_win = False

                if first_win:
                    print('победила первая команда')
                    running = False

        clock.tick(FPS)

        screen.fill(pygame.Color('black'))
        field.render(screen, field.active_ch, field.active_ch_x, field.active_ch_y)
        knights.draw(screen)
        pygame.display.flip()
