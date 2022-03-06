import pygame
import random
from gestorRecursos import *

#Clase platilla mysprite
class MySprite(pygame.sprite.Sprite):
    pass
    

class Background(MySprite):
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Exterior.png')
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
    def __init__(self, x, y, level, lastLevel):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('door.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
        self.lastLevel = lastLevel
        
    def interact(self, level):
        level.clearLevel()
        level.lastLevel = self.lastLevel
        level.currentLevel = self.level
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