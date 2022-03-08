import pygame
from gestorRecursos import *

STATIC_GROUP = 0
INTERACTABLE_GROUP = 1
DESTRUCTABLE_GROUP = 2
BACKGROUND = 3
PLAYER_POS = 4
SCROLL = 5
DOORS = 6
LEVEL_PROGRESSION = 7

#Clase platilla mysprite
class MySprite(pygame.sprite.Sprite):
    pass


class Background(MySprite):
    def __init__(self, x, y, bgd):
        MySprite.__init__(self)
        # Cargamos la imagen
        if bgd == 0:
            fondo = "Olimpo\\Exterior.png"
        else:
            fondo = "Olimpo\\Templo.png"
        self.image = GestorRecursos.CargarImagen(fondo)
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
        self.image = GestorRecursos.CargarImagen('Olimpo\\SueloOlimpo.png')
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Key(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y, level):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Olimpo\\Llave.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        level.locked = True

    def interact(self, level):
        level.screens[level.currentLevel][DOORS][level.screens[level.currentLevel][LEVEL_PROGRESSION]].openDoor()
        level.screens[level.currentLevel][LEVEL_PROGRESSION] += 1
        self.kill()

class Door(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y, level, lastLevel):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('ObjetosComunes\\PortaPechada.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
        self.lastLevel = lastLevel
        self.closed = True

    def openDoor(self):
        self.image = GestorRecursos.CargarImagen('ObjetosComunes\\door.png', -1)
        self.closed = False

    def interact(self, level):
        if not self.closed:
            level.changeLevel = True
            level.currentLevel = self.level
            level.lastLevel = self.lastLevel

    
        
class Wall(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Olimpo\\Wall.png', -1)
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
        self.image = GestorRecursos.CargarImagen(f'Olimpo\\techo{type}.png', -1)
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
        self.image = GestorRecursos.CargarImagen('Olimpo\\Plataforma.png', -1)
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
        self.image = GestorRecursos.CargarImagen('Olimpo\\Jarron.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def damage(self):
        self.kill()
