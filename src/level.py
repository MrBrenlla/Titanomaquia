import pygame
from gestorRecursos import *
#objetos del nivel
from sprites import *
from characters import *

class Level():
    floor_group = pygame.sprite.Group()
    vase_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    static_group = pygame.sprite.Group()
    screenWidth = 1280
    screenHeight = 720
    tileSize = 128
    loaded = False
    

    def __init__(self):
        self.levels = ["olimpo.txt", "templo1.txt", "templo2.txt", "templo3.txt", "temploZeus.txt"]
        self.currentLevel = 0
        self.player = Hera(100, 592)
        self.players = pygame.sprite.Group(self.player)

    def loadLevel(self, screen):
        self.genLevel(self.levels[self.currentLevel])
    
    def clearLevel(self, screen, bgd):
        self.floor_group.clear(screen, bgd)
        self.vase_group.clear(screen, bgd)
        self.platform_group.clear(screen, bgd)
        self.floor_group.empty()
        self.vase_group.empty()
        self.platform_group.empty()
        self.static_group.empty()

    def genLevel(self, txt):
        #leemos el txt para saber que elemetos colocar
        level = GestorRecursos.CargarNivelTxt(txt)
        level = level.split("\n")
        l = len(level)
        
        
        for i in range(l):
            for j in range(len(level[0])):
                if level[i][j] == "A":
                    floor = Floor((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.floor_group.add(floor)
                    self.static_group.add(floor)
                elif level[i][j] == "E":
                    platform = Platform((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.platform_group.add(platform)
                    self.static_group.add(platform)
                elif level[i][j] == "C" or level[i][j] == "G":
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight))
                    self.vase_group.add(vase)

    def update(self, screen, keys):
        self.floor_group.draw(screen)
        self.vase_group.draw(screen)
        for s in self.platform_group.sprites():
            s.draw(screen)

        self.player.move(keys, K_w, K_d, K_a)
        self.player.update(self.static_group)
        self.player.draw(screen)
        
        

        



 

    
                    
        