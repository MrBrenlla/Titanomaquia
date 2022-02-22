from re import M
from telnetlib import NOP
import pygame
from gestorRecursos import *
from sprites import MySprite

#Clase generica Personaje
class Character(MySprite):
    def __init__(self):
        MySprite.__init__(self)
        self.pos = (0, 0)
        self.vel = (3, 3)

#Clase plantilla dioses
class God(Character):
    def __init__(self, spriteSheet, coords, x, y):
        Character.__init__(self)
        self.pos = (x, y)
        self.sheet = GestorRecursos.CargarImagen(spriteSheet, -1)
        self.sheet = self.sheet.convert_alpha()

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(coords)
        datos = datos.split()

        #Array con el numero de frames de cada animacion
        self.animFrames = [4, 1, 4, 5, 1, 4]
        #Array con los rects de las animaciones
        self.anims = []
        
        cont = 0
        
        #Variables para identificar una animacion y controlarlas
        self.animDelay = 10
        self.delay = 10
        self.frame = 0
        self.currentAnim = 0
        
        #recorremos el txt para crear los rects de las animaciones y guardarlas en self.anims
        for anim in range(0, len(self.animFrames)):
            self.anims.append([])
            tmp = self.anims[anim]
            for frame in range(0, self.animFrames[anim]):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        #valores iniciales
        self.rect = pygame.Rect(x, y, self.anims[self.currentAnim][self.frame][2], self.anims[self.currentAnim][self.frame][3])
        self.image = self.sheet.subsurface(self.anims[self.currentAnim][self.frame])
        
        self.updateAnim()



    def move(self, keys, right, left):
        if keys[right]:
            self.rect.x += self.vel[0]
        if keys[left]:
            self.rect.x -= self.vel[0]
    
    def updateAnim(self):
        self.delay -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.delay < 0):
            self.delay = self.animDelay
            # Si ha pasado, actualizamos la postura
            self.frame += 1
            if self.frame >= len(self.anims[self.currentAnim]):
                self.frame = 0
            if self.frame < 0:
                self.frame = len(self.anims[self.frame])-1
            self.image = self.sheet.subsurface(self.anims[self.currentAnim][self.frame])

    def update(self):
        self.updateAnim()
        self.rect.top = self.pos[1] - self.anims[self.currentAnim][self.frame][3]
        Character.update(self)

#Clases de cada dios
class Zeus(God):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y)

class Hera(God):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y)
 

class Hestia(God):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y)

class Poseidon(God):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y)

class Hades(God):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y)

class Demeter(God):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y)


#Clases personajes no jugables
class NoPlayer(Character):
    def __init__(self):
        MySprite.__init__(self)

class NPC(NoPlayer):
    def __init__(self):
        MySprite.__init__(self)


class Enemy(NoPlayer):
    def __init__(self):
        MySprite.__init__(self)

#Clases bosses y enemigos

class Chronos(Enemy):
    pass

class Cerberus(Enemy):
    pass

class Telchines(Enemy):
    pass

class Mermaids(Enemy):
    pass
