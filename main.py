import pygame as pg
import random
from settings import *
from sprites import *

class Game():
    def __init__(self):
        #initialize game
        pg.init()
        pg.mixer.init()

        self.running = True

    def new(self):
        #makes a new Game
        self.playing = True
        self.cameraPos = 0

        self.allSprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.pipes = pg.sprite.Group()

        self.player = Player()
        self.allSprites.add(self.player)

        for i in range(5):
            pipeTopHeight = random.randrange(40, screenSize[1] - pipeGapSize - 40)
            pipeBotHeight = screenSize[1] - pipeTopHeight - pipeGapSize
            pipeTop = Pipe(Pipe.pipeX, pipeTopHeight,'top')
            pipeBot = Pipe(Pipe.pipeX, pipeBotHeight,'bot')

            self.allSprites.add(pipeTop, pipeBot)
            self.pipes.add(pipeTop, pipeBot)

            Pipe.pipeX += spaceBetweenPipePairs

        for i in range(int(screenSize[0] / 32) + 1):
            plat = Platform(Platform.platformX, screenSize[1] - 32)
            self.allSprites.add(plat)
            self.platforms.add(plat)

            Platform.platformX += plat.rect.width

        waitForPlayerInput()

    def run(self):
        #Runs the game permanently until self.running not is equal to True
        while self.playing:
            #Declaring the Delay
            clock.tick(FPS)
            self.events()
            self.update()
            self.render()

    def update(self):
        #Updates all Sprites
        self.allSprites.update()

        self.cameraPos += -cameraSpeed

        if pg.sprite.spritecollide(self.player, self.platforms, False):
            self.playing = False

        if pg.sprite.spritecollide(self.player, self.pipes, False):
            self.playing = False

        for p in self.pipes:
            p.rect.x = p.defaultX + self.cameraPos
            if p.rect.right < 0:
                p.kill()
                pipeTopHeight = random.randrange(40, screenSize[1] - pipeGapSize - 40)
                pipeBotHeight = screenSize[1] - pipeTopHeight - pipeGapSize
                pipeTop = Pipe(Pipe.pipeX, pipeTopHeight,'top')
                pipeBot = Pipe(Pipe.pipeX, pipeBotHeight,'bot')

                self.allSprites.add(pipeTop, pipeBot)
                self.pipes.add(pipeTop, pipeBot)

                Pipe.pipeX += spaceBetweenPipePairs

        for pl in self.platforms:
            pl.rect.x = pl.defaultX + self.cameraPos
            if pl.rect.right < 0:
                pl.kill()
                plat = Platform(Platform.platformX, screenSize[1] - 32)
                self.allSprites.add(plat)
                self.platforms.add(plat)

                Platform.platformX += plat.rect.width

        self.player.score = - int((self.cameraPos - firstPipePair - pipeWidth / 2 + screenSize[0] / 2) / (pipeGapSize + pipeWidth))

    def events(self):
        #Tracks all events and reacts on 'em'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.showPauseScreen()
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def render(self):
        #Render all sprites
        surface.fill(darkaqua)
        self.allSprites.draw(surface)
        drawText('Score: ' + str(self.player.score), white, screenSize[0] / 2, 10,'topmid')
        pg.display.update()

    def showGOScreen(self):
        #Show Game Over Screen
        Pipe.pipeX = firstPipePair
        Platform.platformX = 0

    def showStartScreen(self):
        #Show Start Screen
        pass

    def showPauseScreen(self):
        #Show Pause Screen
        self.playing = False
        self.running = False

game = Game()
game.showStartScreen()
while game.running:
    game.new()
    game.run()
    game.showGOScreen()

pg.quit()
