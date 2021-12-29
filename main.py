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
    intro_text = ["123", "",
                  "Правила игры... Честно пока сам не ебу какие правила"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
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


class Cell:
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

    def __init__(self, filename):
        filename = "data/" + filename + '.txt'
        self.cell_size = Cell.size
        self.coords_of_ch = []
        self.active_ch = False

        with open(filename, 'r') as map_file:
            self.field_map = list(map(list, map(str.rstrip, map_file.readlines())))

        for y in range(len(self.field_map)):
            for x in range(len(self.field_map[0])):
                self.field_map[y][x] = Cell(int(self.field_map[y][x]), y * self.cell_size, x * self.cell_size)

    def render(self, screen):

        for field_y in range(len(self.field_map)):
            for field_x in range(len(self.field_map[0])):
                screen.blit(self.field_map[field_y][field_x].image, (self.field_map[field_y][field_x].x,
                                                                     self.field_map[field_y][field_x].y))
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.field_map[field_y][field_x].x, self.field_map[field_y][field_x].y, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):

        if mouse_pos[0] < len(self.field_map) * self.cell_size \
                and mouse_pos[1] <= len(self.field_map[0]) * self.cell_size:
            x = mouse_pos[0] // self.cell_size
            y = mouse_pos[1] // self.cell_size
            return x, y

        else:
            return None


class Knight1(pygame.sprite.Sprite):

    def __init__(self, field, x, y, *group,):
        super().__init__(*group)
        self.image = load_image('knight.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = field.cell_size * x + field.cell_size // 4, field.cell_size * y + field.cell_size // 4

        self.field = field
        self.field_x = x
        self.field_y = y

        self.field.coords_of_ch.append([self.field_x, self.field_y])
        self.picked = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:

            if self.field.get_cell(args[0].pos)[0] == self.field_x and self.field.get_cell(args[0].pos)[1] == self.field_y and not self.field.active_ch:
                self.picked = True
                self.field.active_ch = True

            if self.picked is True:

                if [self.field.get_cell(args[0].pos)[0], self.field.get_cell(args[0].pos)[1]] not in self.field.coords_of_ch:
                    self.field.coords_of_ch.remove([self.field_x, self.field_y])

                    new_pos_x = self.field.get_cell(args[0].pos)[0]
                    new_pos_y = self.field.get_cell(args[0].pos)[1]
                    self.rect = self.rect.move(-((self.field_x - new_pos_x) * 75), -((self.field_y - new_pos_y) * 75))
                    self.field.coords_of_ch.append([new_pos_x, new_pos_y])

                    self.field_x = args[0].pos[0] // 75
                    self.field_y = args[0].pos[1] // 75
                    self.picked = False
                    self.field.active_ch = False


clock = pygame.time.Clock()
FPS = 60
if __name__ == '__main__':

    pygame.init()

    screen_size = WIDTH, HEIGHT = 750, 750
    screen = pygame.display.set_mode(screen_size)
    start_screen()

    field = Field('generation1')
    knights = pygame.sprite.Group()
    for i in range(1, 9):
        knight = Knight1(field, 1, i, knights)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                knights.update(event)

        clock.tick(FPS)

        field.render(screen)
        knights.draw(screen)
        pygame.display.flip()
