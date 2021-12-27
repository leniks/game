import pygame
import os


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


class Cell:
    def __init__(self, cell_type, y, x):
        self.cell_type = cell_type
        self.size = 75
        self.y = y
        self.x = x

        if self.cell_type == 0:
            self.image = load_image('трава.jpg')
        elif self.cell_type == 1:
            self.image = load_image('камень.jpg')

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
        filename = "data/" + filename
        self.cell_size = 75

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

    def get_cell(self, mouse_pos):

        if mouse_pos[0] < len(self.field_map) * self.cell_size \
                and mouse_pos[1] <= len(self.field_map[0]) * self.cell_size:
            x = mouse_pos[0] // self.cell_size
            y = mouse_pos[1] // self.cell_size
            return x, y

        else:
            return None


class Knight(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('knight.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


if __name__ == '__main__':
    pygame.init()

    size = width, height = 750, 750
    screen = pygame.display.set_mode(size)

    field = Field('generation1')

    knights = pygame.sprite.Group()
    knight = Knight(knights)

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(field.get_cell(event.pos))


        screen.fill((0, 0, 0))
        field.render(screen)

        knights.draw(screen)

        pygame.display.flip()
