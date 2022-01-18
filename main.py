import pygame
import os
import sys
from random import randint, shuffle


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
    global field, knights, wizards

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            if 400 <= mouse[0] <= 800 and 150 <= mouse[1] <= 250:
                pygame.draw.rect(screen, (140, 150, 48), (400, 150, 400, 100))
                text1 = font.render('начать игру', True, (217, 188, 156))
                screen.blit(text1, (470, 170))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    generation()  # генерируем карту
                    knights = pygame.sprite.Group()
                    wizards = pygame.sprite.Group()
                    field = Field('generation1')
                    e = randint(1, 3)
                    if e == 1:
                        for i in range(1, 9):
                            knight = Knight1(field, 2, i, load_image("atttt.png"), 11, 1, knights)
                            knights.add(knight)

                        for i in range(1, 9):
                            wizard = Wizard1(field, 1, i, load_image("att.png"), 9, 1, wizards)
                            wizards.add(wizard)

                        for i in range(1, 9):
                            knight = Knight2(field, 7, i, load_image("atttt2.png"), 11, 1, knights)
                            knights.add(knight)

                        for i in range(1, 9):
                            wizard = Wizard2(field, 8, i, load_image("att2.png"), 9, 1, wizards)
                            wizards.add(wizard)

                    elif e == 2:
                        knight = Knight1(field, 2, 4, load_image("atttt.png"), 11, 1, knights)
                        knights.add(knight)
                        wizard = Wizard1(field, 1, 5, load_image("att.png"), 9, 1, wizards)
                        wizards.add(wizard)
                        knight = Knight2(field, 7, 5, load_image("atttt2.png"), 11, 1, knights)
                        knights.add(knight)
                        wizard = Wizard2(field, 8, 4, load_image("att2.png"), 9, 1, wizards)
                        wizards.add(wizard)
                    else:
                        for i in range(1, 9):
                            if i >= 5:
                                knight = Knight1(field, 2, i, load_image("atttt.png"), 11, 1, knights)
                                knights.add(knight)
                            else:
                                wizard = Wizard1(field, 2, i, load_image("att.png"), 9, 1, wizards)
                                wizards.add(wizard)

                        for i in range(1, 9):
                            if i < 5:
                                knight = Knight2(field, 8, i, load_image("atttt2.png"), 11, 1, knights)
                                knights.add(knight)
                            else:
                                wizard = Wizard2(field, 8, i, load_image("att2.png"), 9, 1, wizards)
                                wizards.add(wizard)
                    game()

            else:
                pygame.draw.rect(screen, (140, 97, 48), (400, 150, 400, 100))
                text1 = font.render('начать игру', True, (217, 188, 156))
                screen.blit(text1, (470, 170))

            if 400 <= mouse[0] <= 800 and 350 <= mouse[1] <= 450:
                pygame.draw.rect(screen, (140, 150, 48), (400, 350, 400, 100))
                text2 = font.render('правила игры', True, (217, 188, 156))
                screen.blit(text2, (470, 370))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rules()
            else:
                pygame.draw.rect(screen, (140, 97, 48), (400, 350, 400, 100))
                text2 = font.render('правила игры', True, (217, 188, 156))
                screen.blit(text2, (470, 370))

            if 400 <= mouse[0] <= 800 and 550 <= mouse[1] <= 650:
                pygame.draw.rect(screen, (140, 150, 48), (400, 550, 400, 100))
                text3 = font.render("результаты", True, (217, 188, 156))
                screen.blit(text3, (470, 570))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    results()
            else:
                pygame.draw.rect(screen, (140, 97, 48), (400, 550, 400, 100))
                text3 = font.render("результаты", True, (217, 188, 156))
                screen.blit(text3, (470, 570))

            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def rules():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    rules = ['правила', '',
             'игра предназначена для 2 игроков',
             'игроки ходят по очереди', '',
             'за один ход можно передвинуть своего юнита',
             'или атаковать им противника', '',
             'каждый тип юнитов имеет уникальные характеристики:',
             'урон, здоровье, способность наносить урон на расстоянии', '',
             'игра заканчивается, когда один игрок',
             'уничтожает все юниты другого игрока']

    text3 = font1.render("нажмите на любую кнопку, чтобы вернуться на главный экран", True, (217, 188, 156))
    dd = [[10, 730, '+'], [1140, 730, '-']]
    while True:
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, (140, 97, 48), (50, 50, 1050, 650))

        for i in range(len(rules)):
            text1 = font1.render(rules[i], True, (217, 188, 156))
            screen.blit(text1, (70, 70 + i * 30))

        screen.blit(text3, (70, 620))

        for i in range(len(dd)):
            pygame.draw.circle(screen, (140, 97, 48), (dd[i][0], dd[i][1]), 20)
            if dd[i][2] == '-':
                dd[i][0] = dd[i][0] - 2
                if abs(dd[0][0] - dd[1][0]) <= 40:
                    if dd[0][2] == '-':
                        dd[0][2] = '+'
                    else:
                        dd[0][2] = '-'
                    if dd[1][2] == '-':
                        dd[1][2] = '+'
                    else:
                        dd[1][2] = '-'
                if dd[i][0] == 10:
                    dd[i][2] = '+'
            if dd[i][2] == '+':
                dd[i][0] = dd[i][0] + 1
                if dd[i][0] == 1140:
                    dd[i][2] = '-'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()

        pygame.display.flip()
        clock.tick(150)


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
            self.passable = True
            self.image = load_image('трава.png')

        elif self.cell_type == 1:
            self.passable = False
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

        self.first_team_turn = True
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

            if x_picked - 1 >= 0 and y_picked - 1 >= 0 and self.field_map[y_picked - 1][x_picked - 1].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked - 1][x_picked - 1].x,
                                  self.field_map[y_picked - 1][x_picked - 1].y, self.cell_size, self.cell_size), 1)

            if y_picked - 1 >= 0 and self.field_map[y_picked - 1][x_picked].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked - 1][x_picked].x, self.field_map[y_picked - 1][x_picked].y,
                                  self.cell_size, self.cell_size), 1)

            if y_picked - 1 >= 0 and x_picked + 1 < len(self.field_map[0]) and \
                    self.field_map[y_picked - 1][x_picked + 1].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked - 1][x_picked + 1].x,
                                  self.field_map[y_picked - 1][x_picked + 1].y, self.cell_size, self.cell_size), 1)

            if x_picked - 1 >= 0 and self.field_map[y_picked][x_picked - 1].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked][x_picked - 1].x, self.field_map[y_picked][x_picked - 1].y,
                                  self.cell_size, self.cell_size), 1)

            if x_picked + 1 < len(self.field_map[0]) and self.field_map[y_picked][x_picked + 1].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked][x_picked + 1].x, self.field_map[y_picked][x_picked + 1].y,
                                  self.cell_size, self.cell_size), 1)

            if x_picked - 1 >= 0 and y_picked + 1 < len(self.field_map) and \
                    self.field_map[y_picked + 1][x_picked - 1].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked + 1][x_picked - 1].x,
                                  self.field_map[y_picked + 1][x_picked - 1].y, self.cell_size, self.cell_size), 1)

            if y_picked + 1 < len(self.field_map) and self.field_map[y_picked + 1][x_picked].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked + 1][x_picked].x, self.field_map[y_picked + 1][x_picked].y,
                                  self.cell_size, self.cell_size), 1)

            if y_picked + 1 < len(self.field_map) and x_picked + 1 < len(self.field_map[0]) and \
                    self.field_map[y_picked + 1][x_picked + 1].passable:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[y_picked + 1][x_picked + 1].x,
                                  self.field_map[y_picked + 1][x_picked + 1].y, self.cell_size, self.cell_size), 1)

            pygame.draw.rect(screen, pygame.Color('white'),
                             (self.field_map[y_picked][x_picked].x,
                              self.field_map[y_picked][x_picked].y, self.cell_size, self.cell_size), 1)

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

    def __init__(self, field, x, y, sheet, columns, rows, *group, ):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.is_animating = False
        self.image = self.frames[self.cur_frame % 9]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            field.cell_size * x + field.cell_size // 4, field.cell_size * y + field.cell_size // 4

        self.field = field
        self.field_x = x
        self.field_y = y

        self.field.team1[self] = (self.field_x, self.field_y)
        self.picked = False

        self.health = 10
        self.damage = 4
        self.alive = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for z in range(columns):
                frame_location = (self.rect.w * z, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (50, 50)))

    def attackanimate(self):
        self.is_animating = True

    def update(self, *args):
        self.image = self.frames[self.cur_frame]
        if self.is_animating:
            self.cur_frame += 1
            self.cur_frame %= 11
            if self.cur_frame == 0:
                self.is_animating = False

        if args and args[0].type == pygame.MOUSEBUTTONDOWN:

            if field.get_cell(args[0].pos):
                mouse_pos_x = self.field.get_cell(args[0].pos)[0]
                mouse_pos_y = self.field.get_cell(args[0].pos)[1]

                if mouse_pos_x == self.field_x and mouse_pos_y == self.field_y and not self.field.active_ch \
                        and not self.field.attacked and self.alive and self.field.first_team_turn:
                    self.picked = True
                    self.field.active_ch = True
                    self.field.active_ch_x = mouse_pos_x
                    self.field.active_ch_y = mouse_pos_y

                if self.picked and (mouse_pos_x, mouse_pos_y) != (self.field_x, self.field_y):

                    if (mouse_pos_x, mouse_pos_y) not in self.field.team1.values() and (mouse_pos_x, mouse_pos_y) \
                            not in self.field.team2.values() and field.field_map[mouse_pos_y][mouse_pos_x].passable:

                        if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                            self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                       -((self.field_y - mouse_pos_y) * Cell.size))
                            self.field.team1[self] = (mouse_pos_x, mouse_pos_y)

                            self.field_x = mouse_pos_x
                            self.field_y = mouse_pos_y
                            self.picked = False
                            self.field.active_ch = False

                            self.field.first_team_turn = not self.field.first_team_turn

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
                            self.attackanimate()
                            attacked_ch.health -= self.damage
                            if attacked_ch.health <= 0:
                                attacked_ch.image = pygame.transform.flip(attacked_ch.image, False, True)
                                attacked_ch.alive = False
                                self.field.team2[attacked_ch] = None

                            self.picked = False
                            self.field.active_ch = False
                            self.field.attacked = True

                            self.field.first_team_turn = not self.field.first_team_turn


class Knight2(pygame.sprite.Sprite):

    def __init__(self, field, x, y, sheet, columns, rows, *group, ):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.is_animating = False
        self.image = self.frames[self.cur_frame % 9]
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            field.cell_size * x + field.cell_size // 4, field.cell_size * y + field.cell_size // 4

        self.field = field
        self.field_x = x
        self.field_y = y

        self.field.team2[self] = (self.field_x, self.field_y)
        self.picked = False

        self.health = 10
        self.damage = 4
        self.alive = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for z in range(columns):
                frame_location = (self.rect.w * z, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (50, 50)))

    def attackanimate(self):
        self.is_animating = True

    def update(self, *args):
        self.image = self.frames[self.cur_frame]
        if self.is_animating:
            self.cur_frame += 1
            self.cur_frame %= 11
            if self.cur_frame == 0:
                self.is_animating = False

        if args and args[0].type == pygame.MOUSEBUTTONDOWN:

            if field.get_cell(args[0].pos):
                mouse_pos_x = self.field.get_cell(args[0].pos)[0]
                mouse_pos_y = self.field.get_cell(args[0].pos)[1]

                if mouse_pos_x == self.field_x and mouse_pos_y == self.field_y and not self.field.active_ch \
                        and not self.field.attacked and self.alive and not self.field.first_team_turn:
                    self.picked = True
                    self.field.active_ch = True
                    self.field.active_ch_x = mouse_pos_x
                    self.field.active_ch_y = mouse_pos_y

                if self.picked and (mouse_pos_x, mouse_pos_y) != (self.field_x, self.field_y):

                    if (mouse_pos_x, mouse_pos_y) not in self.field.team2.values() and (mouse_pos_x, mouse_pos_y) \
                            not in self.field.team1.values() and field.field_map[mouse_pos_y][mouse_pos_x].passable:

                        if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                            self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                       -((self.field_y - mouse_pos_y) * Cell.size))
                            self.field.team2[self] = (mouse_pos_x, mouse_pos_y)

                            self.field_x = mouse_pos_x
                            self.field_y = mouse_pos_y
                            self.picked = False
                            self.field.active_ch = False

                            self.field.first_team_turn = not self.field.first_team_turn

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
                            self.attackanimate()
                            attacked_ch.health -= self.damage
                            if attacked_ch.health <= 0:
                                attacked_ch.image = pygame.transform.flip(attacked_ch.image, False, True)
                                attacked_ch.alive = False
                                self.field.team1[attacked_ch] = None

                            self.picked = False
                            self.field.active_ch = False
                            self.field.attacked = True

                            self.field.first_team_turn = not self.field.first_team_turn


class Wizard1(pygame.sprite.Sprite):
    """
    field - поле, на котором создаются воины
    image - картинка мага
    rect.x, rect.y - координаты модельки воина в пикселях
    field_x, field_y - координаты мага в номерах клеток
    picked - выбран ли юнит
    health - количество здоровья
    mouse_pos_x, mouse_pos_y - позиция мыши при ходе в номерах клеток
    """

    def __init__(self, field, x, y, sheet, columns, rows, *group, ):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 8
        self.is_animating = False
        self.image = self.frames[self.cur_frame % 9]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            field.cell_size * x + field.cell_size // 4, field.cell_size * y + field.cell_size // 8

        self.field = field
        self.field_x = x
        self.field_y = y

        self.field.team1[self] = (self.field_x, self.field_y)
        self.picked = False

        self.health = 10
        self.damage = 3
        self.alive = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for z in range(columns):
                frame_location = (self.rect.w * z, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (50, 50)))

    def attackanimate(self):
        self.is_animating = True

    def update(self, *args):
        self.image = self.frames[self.cur_frame]
        if self.is_animating:
            self.cur_frame += 1
            self.cur_frame %= 9
            if self.cur_frame == 8:
                self.is_animating = False

        if args and args[0].type == pygame.MOUSEBUTTONDOWN:

            if field.get_cell(args[0].pos):
                mouse_pos_x = self.field.get_cell(args[0].pos)[0]
                mouse_pos_y = self.field.get_cell(args[0].pos)[1]

                if mouse_pos_x == self.field_x and mouse_pos_y == self.field_y and not self.field.active_ch \
                        and not self.field.attacked and self.alive and self.field.first_team_turn:
                    self.picked = True
                    self.field.active_ch = True
                    self.field.active_ch_x = mouse_pos_x
                    self.field.active_ch_y = mouse_pos_y

                if self.picked and (mouse_pos_x, mouse_pos_y) != (self.field_x, self.field_y):

                    if (mouse_pos_x, mouse_pos_y) not in self.field.team1.values() and (mouse_pos_x, mouse_pos_y) \
                            not in self.field.team2.values() and field.field_map[mouse_pos_y][mouse_pos_x].passable:

                        if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                            self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                       -((self.field_y - mouse_pos_y) * Cell.size))
                            self.field.team1[self] = (mouse_pos_x, mouse_pos_y)

                            self.field_x = mouse_pos_x
                            self.field_y = mouse_pos_y
                            self.picked = False
                            self.field.active_ch = False

                            self.field.first_team_turn = not self.field.first_team_turn

                    elif (mouse_pos_x, mouse_pos_y) not in self.field.team1.values() and (mouse_pos_x, mouse_pos_y) \
                            in self.field.team2.values():

                        if abs(self.field_x - mouse_pos_x) <= 3 and abs(self.field_y - mouse_pos_y) <= 3:
                            attack_x = mouse_pos_x
                            attack_y = mouse_pos_y

                            attacked_ch = None

                            for key, val in self.field.team2.items():
                                if val == (attack_x, attack_y):
                                    attacked_ch = key
                                    break

                            self.attackanimate()

                            attacked_ch.health -= self.damage
                            if attacked_ch.health <= 0:
                                attacked_ch.image = pygame.transform.flip(attacked_ch.image, False, True)
                                attacked_ch.alive = False
                                self.field.team2[attacked_ch] = None

                            self.picked = False
                            self.field.active_ch = False
                            self.field.attacked = True

                            self.field.first_team_turn = not self.field.first_team_turn


class Wizard2(pygame.sprite.Sprite):

    def __init__(self, field, x, y, sheet, columns, rows, *group, ):
        super().__init__(*group)
        self.alive = True
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 8
        self.image = self.frames[self.cur_frame % 9]
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            field.cell_size * x + field.cell_size // 4, field.cell_size * y + field.cell_size // 8

        self.field = field
        self.field_x = x
        self.field_y = y

        self.field.team2[self] = (self.field_x, self.field_y)
        self.picked = False
        self.is_animating = False
        self.health = 10
        self.damage = 3

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for z in range(columns):
                frame_location = (self.rect.w * z, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (50, 50)))

    def attackanimate(self):
        self.is_animating = True

    def update(self, *args):
        self.image = self.frames[self.cur_frame]

        if self.is_animating:
            self.cur_frame += 1
            self.cur_frame %= 9
            if self.cur_frame == 8:
                self.is_animating = False

        if args and args[0].type == pygame.MOUSEBUTTONDOWN:

            if field.get_cell(args[0].pos):
                mouse_pos_x = self.field.get_cell(args[0].pos)[0]
                mouse_pos_y = self.field.get_cell(args[0].pos)[1]

                if mouse_pos_x == self.field_x and mouse_pos_y == self.field_y and not self.field.active_ch \
                        and not self.field.attacked and self.alive and not self.field.first_team_turn:
                    self.picked = True
                    self.field.active_ch = True
                    self.field.active_ch_x = mouse_pos_x
                    self.field.active_ch_y = mouse_pos_y

                if self.picked and (mouse_pos_x, mouse_pos_y) != (self.field_x, self.field_y):

                    if (mouse_pos_x, mouse_pos_y) not in self.field.team2.values() and (mouse_pos_x, mouse_pos_y) \
                            not in self.field.team1.values() and field.field_map[mouse_pos_y][mouse_pos_x].passable:

                        if abs(self.field_x - mouse_pos_x) <= 1 and abs(self.field_y - mouse_pos_y) <= 1:
                            self.rect = self.rect.move(-((self.field_x - mouse_pos_x) * Cell.size),
                                                       -((self.field_y - mouse_pos_y) * Cell.size))
                            self.field.team2[self] = (mouse_pos_x, mouse_pos_y)

                            self.field_x = mouse_pos_x
                            self.field_y = mouse_pos_y
                            self.picked = False
                            self.field.active_ch = False

                            self.field.first_team_turn = not self.field.first_team_turn

                    elif (mouse_pos_x, mouse_pos_y) not in self.field.team2.values() and (mouse_pos_x, mouse_pos_y) \
                            in self.field.team1.values():
                        attack_x = mouse_pos_x
                        attack_y = mouse_pos_y

                        if abs(self.field_x - mouse_pos_x) <= 3 and abs(self.field_y - mouse_pos_y) <= 3:
                            attacked_ch = None

                            for key, val in self.field.team1.items():
                                if val == (attack_x, attack_y):
                                    attacked_ch = key
                                    break
                            self.attackanimate()
                            attacked_ch.health -= self.damage
                            if attacked_ch.health <= 0:
                                attacked_ch.image = pygame.transform.flip(attacked_ch.image, False, True)
                                attacked_ch.alive = False
                                self.field.team1[attacked_ch] = None

                            self.picked = False
                            self.field.active_ch = False
                            self.field.attacked = True

                            self.field.first_team_turn = not self.field.first_team_turn


def generation():
    # os.system(r'nul>data/generation1.txt')  # очищаем файл
    with open('data/generation1.txt', 'w') as file:
        ans = []
        for i in range(10):
            w = randint(1, 5)
            r = []
            for j in range(w):
                r.append('1')
            for j in range(10 - w):
                r.append('0')
            shuffle(r)
            if 1 <= i <= 8:
                r[2] = '0'
                r[7] = '0'
                r[1] = '0'
                r[8] = '0'
            r = ''.join(r)
            ans.append(r)
        for i in ans:
            file.write(i + '\n')
    return None


def results(result=None):
    if result:
        f = open('data/results.txt', 'a')
        f.write(result + '\n')
        f.close()

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    text = ['результаты последних игр:']
    pygame.draw.rect(screen, (140, 97, 48), (50, 50, 1050, 650))

    text3 = font1.render("нажмите на любую кнопку, чтобы вернуться на главный экран", True, (217, 188, 156))

    with open('data/results.txt', 'r', encoding='utf-8') as f:
        r = [i.strip() for i in f.readlines()][1:]
    if len(r) == 0:
        text.append('нет записанных результатов')
    else:
        if len(r) >= 7:
            r = r[:7]
        text.extend(r[::-1])

    for i in range(len(text)):
        if text[i] == 'first':
            text1 = font1.render('победа первого игрока', True, (34, 89, 46))
        elif text[i] == 'second':
            text1 = font1.render('победа второго игрока', True, (127, 45, 45))
        else:
            text1 = font1.render(text[i], True, (217, 188, 156))
        screen.blit(text1, (70, 70 + i * 30))

    screen.blit(text3, (70, 620))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def game():
    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    running = True
    while running:
        wizards.update()
        knights.update()

        mouse = pygame.mouse.get_pos()

        a, b = len([i for i in field.team1 if i.alive]), len([i for i in field.team2 if i.alive])

        pygame.draw.rect(screen, (140, 97, 48), (780, 40, 350, 80))
        pygame.draw.rect(screen, (140, 97, 48), (780, 140, 350, 180))
        pygame.draw.rect(screen, (140, 97, 48), (780, 280, 350, 180))
        if field.first_team_turn:
            text1 = font1.render(f'ход первого игрока', True, (34, 89, 46))
        else:
            text1 = font1.render(f'ход второго игрока', True, (127, 45, 45))

        text3 = font1.render("у первого игрока", True, (217, 188, 156))
        text6 = font1.render(f"осталось юнитов: {a}", True, (217, 188, 156))

        text4 = font1.render("у второго игрока", True, (217, 188, 156))
        text7 = font1.render(f"осталось юнитов: {b}", True, (217, 188, 156))

        screen.blit(text1, (790, 60))
        screen.blit(text3, (790, 150))
        screen.blit(text4, (790, 350))
        screen.blit(text6, (790, 200))
        screen.blit(text7, (790, 400))

        for event in pygame.event.get():
            if 780 <= mouse[0] <= 1130 and 640 <= mouse[1] <= 720:
                pygame.draw.rect(screen, (140, 150, 48), (780, 640, 350, 80))
                text5 = font1.render("нажмите, чтобы выйти", True, (217, 188, 156))
                screen.blit(text5, (790, 650))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_screen()
            else:
                pygame.draw.rect(screen, (140, 97, 48), (780, 640, 350, 80))
                text5 = font1.render("нажмите, чтобы выйти", True, (217, 188, 156))
                screen.blit(text5, (790, 650))

            if 780 <= mouse[0] <= 1130 and 540 <= mouse[1] <= 620:
                pygame.draw.rect(screen, (140, 150, 48), (780, 540, 350, 80))
                text5 = font1.render("отменить выбор", True, (217, 188, 156))
                screen.blit(text5, (790, 550))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass  # print(knight.picked)
            else:
                pygame.draw.rect(screen, (140, 97, 48), (780, 540, 350, 80))
                text5 = font1.render("отменить выбор", True, (217, 188, 156))
                screen.blit(text5, (790, 550))

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 780 <= mouse[0] <= 1130 and 540 <= mouse[1] <= 620:

                    for elem in field.team1:
                        elem.picked = False

                    for elem in field.team2:
                        elem.picked = False

                    field.active_ch = False

                else:
                    knights.update(event)
                    wizards.update(event)
                    field.attacked = False

                    sec_win = True
                    for elem in field.team1:
                        if elem.alive:
                            sec_win = False

                    if sec_win:
                        results('second')

                    first_win = True
                    for elem in field.team2:
                        if elem.alive:
                            first_win = False

                    if first_win:
                        results('first')

        clock.tick(FPS)
        field.render(screen, field.active_ch, field.active_ch_x, field.active_ch_y)

        for elem, coords in field.team1.items():
            try:
                pygame.draw.rect(screen, (0, 255, 0),
                                 (coords[0] * Cell.size + Cell.size // 8,
                                  (coords[1] + 1) * Cell.size - Cell.size // 8, 5 * elem.health, 5))
            except TypeError:
                pass

        for elem, coords in field.team2.items():
            try:
                pygame.draw.rect(screen, (0, 255, 0),
                                 (coords[0] * Cell.size + Cell.size // 8,
                                  (coords[1] + 1) * Cell.size - Cell.size // 8, 5 * elem.health, 5))
            except TypeError:
                pass

        knights.draw(screen)
        wizards.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    clock = pygame.time.Clock()
    FPS = 15

    pygame.init()
    pygame.display.set_caption('Game')
    screen_size = WIDTH, HEIGHT = 1150, 750
    screen = pygame.display.set_mode(screen_size)
    picture = load_image('trash.png')
    pygame.display.set_icon(picture)
    font = pygame.font.Font('data/21063.otf', 36)
    font1 = pygame.font.Font('data/21063.otf', 24)
    field = Field('generation1')

    start_screen()
    
