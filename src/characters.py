import pygame
from gestorRecursos import *
from sprites import MySprite

#Clase generica Personaje
class Character(MySprite):
    def __init__(self, spriteSheet, coords, x, y):
        MySprite.__init__(self)
        self.pos = (x, y)
        self.vel = (7, 20)
        self.velX = 0
        self.displacement = [False,False]

        self.jumping = False
        self.jumpVel = 0

        #cargamos la imagen del spritesheet
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
        
        self.rect = pygame.Rect(x, y, 44, self.anims[self.currentAnim][self.frame][3])
        self.image = self.sheet.subsurface(self.anims[self.currentAnim][self.frame])
        
        self.updateAnim()


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

    def update(self, static):
        self.updateAnim()

        if self.velX > 0:
            self.image = self.sheet.subsurface(self.anims[self.currentAnim][self.frame])
        if self.velX < 0:
            self.image = pygame.transform.flip(self.sheet.subsurface(self.anims[self.currentAnim][self.frame]), 1, 0)
        
        self.rect.x += self.velX
        self.rect.y += self.jumpVel

        collider = pygame.sprite.spritecollideany(self, static)

        if (collider != None) and (self.jumpVel>0) and (collider.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.rect.bottom =  collider.rect.y
                # Lo ponemos como quieto
                # Y estará quieto en el eje y
                self.jumpVel = 0
                self.jumping = False
        if collider == None:
            self.jumping = True
        
    def characterScroll(self, level_size, level_displacement, screenSize):

        level_size_ScrollX = (level_size[0]/10)*screenSize[0]
        level_size_ScrollY = (level_size[1]/5)*screenSize[1]
        #print("screenheight: ", screenSize[1])
        # ScrollX
        if (self.rect.x > 590 and level_displacement[0]<(level_size_ScrollX-screenSize[0]-self.rect.x) ) or (self.rect.x < 590 and level_displacement[0]>0) and level_size_ScrollX>screenSize[0]:    
            self.rect.x -= self.velX
            self.displacement[0] = True
        else:  
            self.displacement[0] = False
        
        # ScrollY
        #print("sizescrolly: ", level_size_ScrollY)
        print("self.rect.y: ", self.rect.y)
        #print("velocidad en y: ", self.jumpVel)
        if (self.rect.y < 290 and level_displacement[1]<(level_size_ScrollY-screenSize[1]-self.rect.y) ) or (self.rect.y > 290 and level_displacement[1]>0) and level_size_ScrollY>screenSize[1]:
            #self.rect.y -= self.jumpVel
            self.displacement[1] = True
        else:
            self.displacement[1] = False
        return [self.velX,self.jumpVel]


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 22, self.rect.y, self.rect.width, self.rect.height))
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 4)
        

#Clase plantilla dioses
class God(Character):
    def __init__(self, spriteSheet, coords, x, y):
        Character.__init__(self, spriteSheet, coords, x, y)
        

    def move(self, keys, up, right, left):
        self.velX = 0
        if keys[right]:
            self.velX = self.vel[0]
        if keys[left]:
            self.velX = -self.vel[0]
        if keys[up] and not(self.jumping):
            self.jumpVel = -self.vel[1]
            self.jumping = True
        #aplicamos gravedad
        self.jumpVel += 1
        #velocidad terminal
        if self.jumpVel > 15:
            self.jumpVel = 15





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
