import pygame
from gestorRecursos import *

#objetos del nivel
class Floor(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('SueloOlimpo.png')
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Plataforma.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Vase(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Jarron.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level():
    floor_group = pygame.sprite.Group()
    vase_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    screenWidth = 1280
    screenHeight = 720
    tileSize = 128

    def __init__(self) -> None:
        self.levels = ["olimpo.txt", "templo1.txt", "templo2.txt", "templo3.txt", "temploZeus.txt"]
        self.currentLevel = 0
        

    def loadLevel(self, screen):
        self.genLevel(self.levels[self.currentLevel])
        self.floor_group.draw(screen)
        self.vase_group.draw(screen)
        self.platform_group.draw(screen)
    
    def clearLevel(self, screen):
        self.floor_group.clear(screen, screen)
        self.vase_group.clear(screen, screen)
        self.platform_group.clear(screen, screen)
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
                if level[i][j] == "E":
                    platform = Platform((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    self.platform_group.add(platform)
                if level[i][j] == "C" or level[i][j] == "G":
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight))
                    self.vase_group.add(vase)



 

    
                    
        