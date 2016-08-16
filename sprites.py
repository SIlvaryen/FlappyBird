import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load(os.path.join(imgFolder, 'Birdy.png'))
        pg.transform.scale(self.image, (32,32))
        self.rect = self.image.get_rect()

        self.rect.centerx = screenSize[0] / 4
        self.rect.centery = screenSize[1] / 2

        self.vely = 0
        self.accy = 0

        self.score = 0

    def update(self):
        self.accy = gravity

        self.vely += self.accy
        self.rect.y += int(self.vely)

    def jump(self):
        self.vely = -jumpPower

class Platform(pg.sprite.Sprite):
    platformX = 0
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(os.path.join(imgFolder, 'gras_block.png'))
        pg.transform.scale(self.image, (32,32))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.defaultX = self.rect.x
        self.defaultY = self.rect.y

class Pipe(pg.sprite.Sprite):
    pipeX = firstPipePair
    def __init__(self, x, height, pos):
        super().__init__()
        self.image = pg.Surface((pipeWidth, height))
        self.image.fill(green)
        self.rect = self.image.get_rect()

        self.rect.x = x
        if pos == 'top':
            self.rect.y = 0
        elif pos == 'bot':
            self.rect.y = screenSize[1] - self.rect.height
        else:
            print('Not correct!!!')

        self.defaultX = self.rect.x
        self.defaultY = self.rect.y
