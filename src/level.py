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
    interactable_group = pygame.sprite.Group()
    screenWidth = 1280
    screenHeight = 720
    screenScroll = [0,0]
    bgScroll = 0
    tileSize = 128
    loaded = False
    currentLevel = 0
    

    def __init__(self, screen, bgd):
        self.levels = ["olimpo.txt", "templo1.txt", "templo2.txt", "templo3.txt", "temploZeus.txt"]
        self.level_size = [[49,5],[21,9],[21,9]]
        self.level_displacement = [0, 0]
        self.screen = screen
        self.bgd = bgd
        

    def loadLevel(self):
        self.genLevel(self.levels[self.currentLevel])
    
    def clearLevel(self):
        self.floor_group.clear(self.screen, self.bgd)
        self.vase_group.clear(self.screen, self.bgd)
        self.platform_group.clear(self.screen, self.bgd)
        self.interactable_group.clear(self.screen, self.bgd)
        self.floor_group.empty()
        self.vase_group.empty()
        self.platform_group.empty()
        self.interactable_group.empty()
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
                elif level[i][j] == "P":
                    self.player = Hera((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.players = pygame.sprite.Group(self.player)
                elif level[i][j] == "E":
                    platform = Platform((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.platform_group.add(platform)
                    self.static_group.add(platform)
                elif level[i][j] == "C" or level[i][j] == "G":
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight))
                    self.vase_group.add(vase)
                    self.interactable_group.add(vase)
                elif level[i][j] == "F":
                    door = Door((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.interactable_group.add(door)
                elif level[i][j] == "B":
                    wall = Wall((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.interactable_group.add(wall)
                elif level[i][j] == "I":
                    ceil = Ceiling((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), 1)
                    self.static_group.add(ceil)
                elif level[i][j] == "J":
                    ceil = Ceiling((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), 2)
                    self.static_group.add(ceil)
                elif level[i][j] == "K":
                    ceil = Ceiling((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), 3)
                    self.static_group.add(ceil)

    def drawScenary(self,screen):

        self.floor_group.draw(screen)
        self.vase_group.draw(screen)
        self.platform_group.draw(screen)
        self.player.draw(screen)

    def update(self, screen, keys):


        self.player.move(keys, K_w, K_d, K_a)
        self.player.interact(keys, K_e, self.interactable_group, self)
        self.player.update(self.static_group)
        
        self.screenScroll = self.player.characterScroll(self.level_size[self.currentLevel], self.level_displacement,[self.screenWidth,self.screenHeight])

        if self.player.displacement[0] or self.player.displacement[1]:
            self.levelDisplacement()
        
        self.static_group.draw(screen)
        self.interactable_group.draw(screen)
        self.player.draw(screen)

    def levelDisplacement(self):
        self.level_displacement[0] += self.screenScroll[0]
        self.level_displacement[1] -= self.screenScroll[1]
        for s in self.static_group.sprites():
            s.displacementSprite(self.screenScroll)
        for s in self.interactable_group.sprites():
            s.displacementSprite(self.screenScroll)


        
                    
        