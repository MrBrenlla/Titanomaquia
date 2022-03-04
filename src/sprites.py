import pygame
import random
from gestorRecursos import *

#Clase platilla mysprite
class MySprite(pygame.sprite.Sprite):
    def displacementSprite(self,vel):
        self.rect.x -= vel[0]
        self.rect.y -= vel[1]
    

class Floor(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('SueloOlimpo.png')
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('door.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def interact(self, level):
        level.clearLevel()
        level.currentLevel = random.randrange(0, 3)
        print(level.currentLevel)
        level.loaded = False
class Wall(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Wall.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ceiling(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y, type):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen(f'techo{type}.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Plataforma.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = 24


class Vase(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Jarron.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self, level):
        self.kill()