import pygame
from gestorRecursos import *
#objetos del nivel
from sprites import *

class Level():
    floor_group = pygame.sprite.Group()
    vase_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    screenWidth = 1280
    screenHeight = 720
    tileSize = 128
    loaded = False

    def __init__(self):
        self.levels = ["olimpo.txt", "templo1.txt", "templo2.txt", "templo3.txt", "temploZeus.txt"]
        self.currentLevel = 0
        

    def loadLevel(self, screen):
        
        if not(self.loaded):
            self.genLevel(self.levels[self.currentLevel])
            self.loaded = True
        self.floor_group.draw(screen)
        self.vase_group.draw(screen)
        self.platform_group.draw(screen)
    
    def clearLevel(self, screen, bgd):
        self.floor_group.clear(screen, bgd)
        self.vase_group.clear(screen, bgd)
        self.platform_group.clear(screen, bgd)
        self.floor_group.empty()
        self.vase_group.empty()
        self.platform_group.empty()

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
                elif level[i][j] == "E":
                    platform = Platform((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.platform_group.add(platform)
                elif level[i][j] == "C" or level[i][j] == "G":
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight))
                    self.vase_group.add(vase)



 

    
                    
        