import pygame
from gestorRecursos import *
from sprites import *


# Movimientos
STILL = 0
LEFT = 1
RIGHT = 2
UP = 3

#Stances
SPRITE_WALKING = 0
SPRITE_JUMPING = 1
SPRITE_IDLE = 2
SPRITE_DYING = 3
SPRITE_LET_DYING = 4
SPRITE_ATTACK = 5

#Clase generica Personaje
class Character(MySprite):
    def __init__(self, spriteSheet, coords, x, y):
        MySprite.__init__(self)
        self.pos = (x, y)
        self.vel = (7, 20)
        self.velX = 0
        self.displacement = [False,False]

        self.attacking = False

        self.jumping = False
        self.jumpVel = 0

        #cargamos la imagen del spritesheet
        self.sheet = GestorRecursos.CargarImagen('Dioses/' + spriteSheet, -1)
        self.sheet = self.sheet.convert_alpha()

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas('Dioses/' + coords)
        datos = datos.split()

        #Array con el numero de frames de cada animacion
        self.animFrames = [4, 1, 4, 5, 1, 5]
        #Array con los rects de las animaciones
        self.anims = []

        cont = 0

        #Variables para identificar una animacion y controlarlas
        self.animDelay = 10
        self.delay = 10
        self.frame = 0
        self.currentAnim = SPRITE_IDLE
        self.right = True

        #recorremos el txt para crear los rects de las animaciones y guardarlas en self.anims
        for anim in range(0, len(self.animFrames)):
            self.anims.append([])
            tmp = self.anims[anim]
            for frame in range(0, self.animFrames[anim]):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        #valores iniciales

        self.rect = pygame.Rect(x, y, 44, self.anims[self.currentAnim][self.frame][3])
        self.attackRect = pygame.Rect(0, 0, 0, 0)
        self.image = self.sheet.subsurface(self.anims[self.currentAnim][self.frame])

        self.updateAnim()

    def move(self, movement):
        if (movement==UP):
            if (self.currentAnim==SPRITE_JUMPING):
                self.movement=SPRITE_IDLE
            else:
                self.movement=SPRITE_JUMPING
        else:
            self.movement=movement

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

        if (self.frame>=len(self.anims[self.currentAnim])):
            self.frame=0
        if self.right:
            self.image = self.sheet.subsurface(self.anims[self.currentAnim][self.frame])
        else:
            self.image = pygame.transform.flip(self.sheet.subsurface(self.anims[self.currentAnim][self.frame]), 1, 0)

        # self.rect.bottom = self.rect.y


    def setMeleeRange(self, width, height):
        self.attackRangeWidth = width
        self.attackRangeHeight = height

    def update(self, static):


        self.rect.x += self.velX
        self.rect.y += self.jumpVel

        self.attackRect.x += self.velX
        self.attackRect.y = self.rect.y



        if (self.jumping):
            self.currentAnim=SPRITE_JUMPING

        elif (self.velX>0 or self.velX<0) and not(self.attacking):
                self.currentAnim=SPRITE_WALKING

        elif (self.velX==0):
            self.currentAnim=SPRITE_IDLE


        if (self.attacking):
            self.currentAnim=SPRITE_ATTACK
            if self.right:
                self.attackRect.x = self.rect.x + self.rect.width
            else:
                self.attackRect.x = self.rect.x - self.attackRangeWidth
            self.attackRect.y = self.rect.y
            self.attackRect.width = self.attackRangeWidth
            self.attackRect.height = self.attackRangeHeight
            if (self.frame>=4):
                self.attacking = False
                self.attackRect = pygame.Rect(0, 0, 0, 0)

        #check collisions
        static_collider = pygame.sprite.spritecollideany(self, static)


        if (static_collider != None) and (self.jumpVel>0) and (static_collider.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.rect.bottom =  static_collider.rect.y
                # Lo ponemos como quieto
                # Y estará quieto en el eje y
                self.jumpVel = 0
                self.jumping = False
        if static_collider == None:
            self.jumping = True
        #print("self.rect.y: ", self.rect.y)


        self.updateAnim()

    def draw(self, screen, newScroll):
        screen.blit(self.image, (self.rect.x -22 - newScroll[0], self.rect.y - newScroll[1] - self.image.get_height() + self.rect.height, self.rect.width, self.rect.height))
        #pygame.draw.rect(screen, (255, 255, 255), (self.attackRect.x - newScroll[0], self.attackRect.y -newScroll[1], self.attackRect.width, self.attackRect.height), 4)
        #pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - newScroll[0], self.rect.y -newScroll[1], self.rect.width, self.rect.height), 4)


#Clase plantilla dioses
class God(Character):
    def __init__(self, spriteSheet, coords, x, y):
        Character.__init__(self, spriteSheet, coords, x, y)
        self.name=""




    def move(self, keys, up, right, left):
        self.velX = 0
        if keys[right]:
    #        Character.move(self,RIGHT)
            self.right = True
            self.velX = self.vel[0]
        if keys[left]:
            self.right = False
    #       Character.move(self,LEFT)
            self.velX = -self.vel[0]
        if keys[up] and not(self.jumping):
            son_jump = GestorRecursos.CargarSonido("Comunes/salto.wav",False)
            son_jump.set_volume(Config.effectsVolume / 10)
            son_jump.play()
    #        Character.move(self,UP)
            self.jumpVel = -self.vel[1]
            self.jumping = True
        #aplicamos gravedad
        self.jumpVel += 1
        #velocidad terminal
        if self.jumpVel > 15:
            self.jumpVel = 15

    def interact(self, interactables, level):
        interact_collider = pygame.sprite.spritecollideany(self, interactables)

        if (interact_collider != None):
            interact_collider.interact(level)


class GodMelee(God):

    def __init__(self, spriteSheet, coords, x, y):
        Character.__init__(self, spriteSheet, coords, x, y)
        self.name=""


    def attack(self, destructable, eventList):

        for event in eventList:
            if event.type == KEYDOWN and event.key == K_SPACE:
                if not self.attacking:
                    #son_attak = GestorRecursos.CargarSonido(self.name + "/ataque.wav",False)
                    son_attack = GestorRecursos.CargarSonido(type(self).__name__ + "/ataque.wav",False)
                    son_attack.set_volume(Config.effectsVolume)
                    son_attack.play()
                    self.frame = 0

                    self.attacking = True
            #Character.currentAnim=SPRITE_ATTACK

        dropItems = []
        for obj in destructable:
            hit = pygame.Rect.colliderect(self.attackRect, obj.rect)
            if hit:
                dropItems.append(obj.damage())

        return dropItems


class GodRange(God):
    def __init__(self, spriteSheet, coords, x, y):
        God.__init__(self, spriteSheet, coords, x, y)
        self.name=""
        self.coords = coords
        self.proyectiles = []


    def attack(self, destructable, eventList):

        for event in eventList:
            if event.type == KEYDOWN and event.key == K_SPACE:
                if not self.attacking:
                    son_attack = GestorRecursos.CargarSonido(type(self).__name__ + "/ataque.wav",False)
                    son_attack.set_volume(Config.effectsVolume)
                    son_attack.play()
                    self.frame = 0

                    self.attacking = True
                    proyectile = Proyectile (self.rect.x, self.rect.y, type(self).__name__)
                    self.proyectiles.append(proyectile)

        dropItems = []
        for obj in destructable:
            hit = pygame.Rect.colliderect(self.attackRect, obj.rect)
            if hit:
                dropItems.append(obj.damage())

        return dropItems

    def draw(self, screen, newScroll):
        Character.draw(self, screen, newScroll)
        for i in self.proyectiles:
            i.dropProyectile(screen)


#Clases de cada dios

class Zeus(GodRange):
    def __init__(self, x, y):
        GodRange.__init__(self, "zeus.png", "zeus.txt", x, y,)

class Hera(GodMelee):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y,)
        God.setMeleeRange(self, 55, 60)
        self.name = "Hera"


class Hestia(GodRange):
    def __init__(self, x, y):
        GodRange.__init__(self, "hera.png", "hera.txt", x, y,)


class Poseidon(GodRange):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y,)

class Hades(GodMelee):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y,)

class Demeter(GodMelee):
    def __init__(self, x, y):
        God.__init__(self, "hera.png", "hera.txt", x, y,)


#Clases personajes no jugables
class NoPlayer(Character):
    def __init__(self):
        MySprite.__init__(self)

class NPC(NoPlayer):
    def __init__(self, x, y, guard):
        MySprite.__init__(self)
        self.image = GestorRecursos.CargarImagen('NPC/guardia2.png', -1)
        # El rectangulo donde estara la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.guard = guard


    def interact(self, level):
        if (level.screens[level.currentLevel][LEVEL_PROGRESSION] == self.guard) and ((not level.screens[self.guard][DOORS][-1].closed) or self.guard == 0):
            level.screens[level.currentLevel][STATIC_GROUP].add(Dialog(self.rect.x - 60, self.rect.y - 256))

            level.screens[level.currentLevel][DOORS][level.screens[level.currentLevel][LEVEL_PROGRESSION]].openDoor()
            level.screens[level.currentLevel][LEVEL_PROGRESSION] += 1


class Enemy(Character):
    def __init__(self, spriteSheet, coords, x, y):
        MySprite.__init__(self)
        self.pos = (x, y)
        self.vel = (5, 17)
        self.velX = 0
        self.displacement = [False,False]

        self.attacking = False

        self.jumping = False
        self.jumpVel = 0

        #cargamos la imagen del spritesheet
        self.sheet = GestorRecursos.CargarImagen('Dioses/' + spriteSheet, -1)
        self.sheet = self.sheet.convert_alpha()

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas('Dioses/' + coords)
        datos = datos.split()

        #Array con el numero de frames de cada animacion
        self.animFrames = [4, 1, 4, 5, 1, 5]
        #Array con los rects de las animaciones
        self.anims = []



#Clases bosses y enemigos

class Chronos(Enemy):
    pass

class Cerberus(Enemy):
    pass

class Telchines(Enemy):
    pass

class Mermaids(Enemy):
    pass
