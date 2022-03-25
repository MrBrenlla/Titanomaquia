from operator import sub
import pygame
from gestorRecursos import *
from config import *

STATIC_GROUP = 0
INTERACTABLE_GROUP = 1
DESTRUCTABLE_GROUP = 2
ENEMY_GROUP = 3
BACKGROUND = 4
PLAYER_POS = 5
SCROLL = 6
DOORS = 7
LEVEL_PROGRESSION = 8

#Clase plantilla mysprite
class MySprite(pygame.sprite.Sprite):
    pass


class Background(MySprite):
    def __init__(self, x, y, bgd, level):
        MySprite.__init__(self)
        # Cargamos la imagen
        if bgd == 0:
            fondo = f"{level}/fondo1.png"
        else:
            fondo = f"{level}/fondo2.png"
        self.image = GestorRecursos.CargarImagen(fondo)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Floor(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y,lvlName):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen(f'{lvlName}/Suelo.png', - 1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Dialog(MySprite):
    def __init__(self, x, y, dialog, lvlName, subLevel):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen(f'{lvlName}/{subLevel}/Texto{dialog}.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self, level):
        pass

class Key(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Olimpo/Llave.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self, level):
        GestorRecursos.CargarSonido("Comunes/coger_llaves.wav",False).play()
        level.screens[level.currentLevel][DOORS][level.screens[level.currentLevel][LEVEL_PROGRESSION]].openDoor()
        level.screens[level.currentLevel][LEVEL_PROGRESSION] += 1
        self.kill()

class Door(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y, level, lastLevel, lvlName, closed):
        MySprite.__init__(self)
        # Cargamos la imagen
        if closed:
            self.image = GestorRecursos.CargarImagen(f'{lvlName}/PortaPechada.png', -1)
        else: 
            self.image = GestorRecursos.CargarImagen('ObjetosComunes/door.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
        self.lastLevel = lastLevel
        self.closed = closed

    def openDoor(self):
        self.image = GestorRecursos.CargarImagen('ObjetosComunes/door.png', -1)
        self.closed = False

    def interact(self, level):
        if not self.closed:
            print(self.lastLevel)
            level.changeLevel = True
            level.currentLevel = level.lastLevel if self.level == 0 else self.level
            level.lastLevel = self.lastLevel
            #Posicionar al jugador segun la posicion correcta en el nivel y actualizar la del nivel anterior
            level.screens[level.lastLevel][PLAYER_POS] = (self.rect.x, self.rect.y)
            level.player.rect.x = level.screens[level.currentLevel][PLAYER_POS][0]
            level.player.rect.y = level.screens[level.currentLevel][PLAYER_POS][1]


class Platform(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y,lvlName):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen(f'{lvlName}/Plataforma.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = 24


class Vase(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y, item):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Olimpo/Jarron.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.item = item

    def damage(self):
        vase_sound = GestorRecursos.CargarSonido("Comunes/vasija_rompiendose.wav",False)
        vase_sound.set_volume(Config.effectsVolume / 10)
        vase_sound.play()
        self.kill()
        if self.item == 1:
            return Mead(self.rect.x, self.rect.y)
        if self.item == 2:
            return Key(self.rect.x, self.rect.y)
        return []


class PracticeGuard(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('Olimpo/practiceGuard.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def damage(self):
        hitSound = GestorRecursos.CargarSonido("Comunes/vasija_rompiendose.wav",False)
        hitSound.set_volume(Config.effectsVolume / 10)
        hitSound.play()
        return []


class Mead(MySprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self, x, y):
        MySprite.__init__(self)
        # Cargamos la imagen
        self.image = GestorRecursos.CargarImagen('ObjetosComunes/HidromielOlimpo.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self, level):
        vase_sound = GestorRecursos.CargarSonido("Comunes/beber_hidromiel.wav",False)
        vase_sound.set_volume(Config.effectsVolume)
        vase_sound.play()
        self.kill()



class Proyectile(MySprite):
    def __init__(self,x,y,right, nameGod):
        MySprite.__init__(self)
        self.image = GestorRecursos.CargarImagen('Proyectil/proyectil' + nameGod + '.png', -1)
        self.vel = 10
        if not right:
            self.vel = -10
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.damage = 10
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.orginalPos = x
        self.rect.width = 48
        self.rect.height = 48
        

    def moveProyectile(self):
        self.rect.x += self.vel

        if abs(self.rect.x - self.orginalPos) > 700:
            self.kill()


    def checkCollision(self,enemies, destructable):
        dropItems = []
        for obj in destructable:
            hit = pygame.Rect.colliderect(self.rect, obj.rect)
            if hit:
                dropItems.append(obj.damage())
                self.kill()
        for enemy in enemies:
            hit = pygame.Rect.colliderect(self.rect, enemy.rect)
            if hit:
                enemy.damage()
                self.kill()


        

        return dropItems


class Sand(MySprite):
    def __init__(self, x, y):
        MySprite.__init__(self)
        self.image = GestorRecursos.CargarImagen('TemploSubmarino/arena.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Medal(MySprite):
    def __init__(self, x, y):
        MySprite.__init__(self)
        self.image = GestorRecursos.CargarImagen('Olimpo/Medallon.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self, level):
        pass 

class Mirror(MySprite):
    def __init__(self, x, y):
        MySprite.__init__(self)
        self.image = GestorRecursos.CargarImagen('Olimpo/Espello.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self, level):
        pass 



class GodObject(MySprite):
    def __init__(self, x, y, lvlName):
        MySprite.__init__(self)
        self.image = GestorRecursos.CargarImagen(f'{lvlName}/godObj.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self, level):
        level.screens[level.currentLevel][LEVEL_PROGRESSION] += 1
        self.kill() 

class Valve(MySprite):
    def __init__(self, x, y):
        MySprite.__init__(self)
        self.image = GestorRecursos.CargarImagen('TemploSubmarino/Valvula.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False

    def interact(self, level):
        if not self.active:        
            level.screens[level.currentLevel][DOORS][level.screens[level.currentLevel][LEVEL_PROGRESSION]].openDoor()
            level.screens[level.currentLevel][LEVEL_PROGRESSION] += 1
            self.active = True