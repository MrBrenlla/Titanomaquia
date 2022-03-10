import pygame
from pygame.locals import *
from gestorRecursos import *
from sprites import *
from characters import *
from gui import *

#Constantes acceso a grupos del nivel
# FLOOR_GROUP = 0
# VASE_GROUP = 1
# PLATFORM_GROUP = 2
STATIC_GROUP = 0
INTERACTABLE_GROUP = 1
DESTRUCTABLE_GROUP = 2
BACKGROUND = 3
PLAYER_POS = 4
SCROLL = 5
DOORS = 6
LEVEL_PROGRESSION = 7

class Scene():
    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update")
    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo events")
    def draw(self, screen):
        raise NotImplemented("Tiene que implementar el metodo draw")


class Olympus(Scene):

    def __init__(self, director):
        super().__init__(director)
        self.screenWidth = 1280
        self.screenHeight = 640
        self.tileSize = 128

        #Grupos de sprites del nivel
        # self.floorGroup = pygame.sprite.Group()
        # self.vaseGroup = pygame.sprite.Group()
        # self.platformGroup = pygame.sprite.Group()
        # self.staticGroup = pygame.sprite.Group()
        # self.interactableGroup = pygame.sprite.Group()

        #Info del nivel
        self.screens = []
        self.levels = ["olimpo.txt", "templo1.txt", "templo2.txt", "templo3.txt", "temploZeus.txt"]
        self.levelSize = [[49,5],[21,9],[21,9], [16,8], [21, 9]]
        self.changeLevel = False
        self.currentLevel = 0
        self.lastLevel = 0



        #grupos

        for level in range(len(self.levels)):
            # print(level)
            self.screens.append(self.genLevel(self.levels[level], level))

        self.player = Hera(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])


    def events(self, eventList):
        for event in eventList:
            #Comprobar si se quiere salir
            if event.type == pygame.QUIT:
                self.director.exitGame()
            if event.type == KEYDOWN and event.key == K_e:
                self.player.interact(self.screens[self.currentLevel][INTERACTABLE_GROUP], self)
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.stackScene(MenuPause(self.director))


        keys = pygame.key.get_pressed()
        #Acciones posibles del player
        self.player.move(keys, K_w, K_d, K_a)
        dropItems = self.player.attack(self.screens[self.currentLevel][DESTRUCTABLE_GROUP], eventList)
        for item in dropItems:
            self.screens[self.currentLevel][INTERACTABLE_GROUP].add(item)


    def updateScroll(self):
        #Usamos true scroll para hacer los calculos exactos del scroll
        #El scroll es propio de cada pantalla para mantener los valores anteriores al cambiar entre ellas
        trueScroll = self.screens[self.currentLevel][SCROLL]

        if( (((self.player.rect.x-trueScroll[0]-640)/10)>=0 or trueScroll[0]>0) and ((trueScroll[0]<(self.levelSize[self.currentLevel][0]*128-1280-4)) or ((self.player.rect.x-trueScroll[0]-640)/10)<=0 )):
            self.screens[self.currentLevel][SCROLL][0] += (self.player.rect.x-trueScroll[0]-640)/10

        if ( ((trueScroll[1]>(self.levelSize[self.currentLevel][1]*(-128)+640+4)) or (((self.player.rect.y-trueScroll[1]-200)/10)>=0)) and (((self.player.rect.y-trueScroll[1]-200)/10)<=0 or trueScroll[1]<0) ):
            self.screens[self.currentLevel][SCROLL][1] += (self.player.rect.y-trueScroll[1]-200)/10

        #Copiamos los valores de true scroll y los convertimos a int para mayor fluidez
        self.scroll = self.screens[self.currentLevel][SCROLL].copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
        #Comprobamos que la camara no se salga de los limites del mapa
        if self.scroll[0] < 0: self.scroll[0] = 0
        if self.scroll[1] > 0: self.scroll[1] = 0

    def playerLimits(self):

        levelWidth = self.levelSize[self.currentLevel][0]*128

        if self.player.rect.x < 0:
            self.player.rect.x = 0
        if self.player.rect.x > levelWidth - self.player.rect.width:
            self.player.rect.x = levelWidth - self.player.rect.width

    def update(self, time):
        self.updateScroll()
        self.playerLimits()
        self.player.update(self.screens[self.currentLevel][STATIC_GROUP])



    def clearScreen(self, screen):
        self.screens[self.currentLevel][STATIC_GROUP].clear(screen, self.screens[self.currentLevel][BACKGROUND])
        self.screens[self.currentLevel][INTERACTABLE_GROUP].clear(screen, self.screens[self.currentLevel][BACKGROUND])
        self.screens[self.currentLevel][DESTRUCTABLE_GROUP].clear(screen, self.screens[self.currentLevel][BACKGROUND])

    def draw(self, screen):

        if self.changeLevel:
            self.clearScreen(screen)

            self.changeLevel = False

        screen.blit(self.screens[self.currentLevel][BACKGROUND].image, (self.screens[self.currentLevel][BACKGROUND].rect.x-self.scroll[0],self.screens[self.currentLevel][BACKGROUND].rect.y-self.scroll[1]))

        for s in self.screens[self.currentLevel][STATIC_GROUP].sprites():
            screen.blit(s.image,(s.rect.x-self.scroll[0],s.rect.y-self.scroll[1]))

        for s in self.screens[self.currentLevel][INTERACTABLE_GROUP].sprites():
            screen.blit(s.image,(s.rect.x-self.scroll[0],s.rect.y-self.scroll[1]))

        for s in self.screens[self.currentLevel][DESTRUCTABLE_GROUP].sprites():
            screen.blit(s.image,(s.rect.x-self.scroll[0],s.rect.y-self.scroll[1]))

        self.player.draw(screen, self.scroll)


    def genLevel(self, txt, lvl):
        #leemos el txt para saber que elemetos colocar
        level = GestorRecursos.CargarNivelTxt("Olimpo/" + txt)
        level = level.split("\n")
        sound = GestorRecursos.CargarSonido("Musica_Olimpo.mp3",True)
        l = len(level)
        bgd = Background(0, -(l*self.tileSize-self.screenHeight), lvl)
        # print(bgd.rect)
        doors = 1
        # floorGroup = pygame.sprite.Group()
        # vaseGroup = pygame.sprite.Group()
        # platformGroup = pygame.sprite.Group()
        staticGroup = pygame.sprite.Group()
        interactableGroup = pygame.sprite.Group()
        destructableGroup = pygame.sprite.Group()
        playerPos = (300, 500)
        levelScroll = [0, 0]
        doorArray = []
        levelProgression = 0
        guard = 0
        for i in range(l):
            for j in range(len(level[0])):
                if level[i][j] == "A":
                    floor = Floor((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    # floorGroup.add(floor)
                    staticGroup.add(floor)
                elif level[i][j] == "E":
                    platform = Platform((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    # platformGroup.add(platform)
                    staticGroup.add(platform)
                elif level[i][j] == "C": #Vasija que contiene llave
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight), 2)
                    # vaseGroup.add(vase)
                    destructableGroup.add(vase)
                elif level[i][j] == "G": #Vasija que contiene nada
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight), 0)
                    # vaseGroup.add(vase)
                    destructableGroup.add(vase)
                elif level[i][j] == "B": #Vasija que contiene hidromiel
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight), 1)
                    # vaseGroup.add(vase)
                    destructableGroup.add(vase)
                elif level[i][j] == "F":
                    door = Door((j*self.tileSize), (i*self.tileSize - self.tileSize/2)-(l*self.tileSize-self.screenHeight), doors, lvl)
                    doors += 1
                    doorArray.append(door)
                    interactableGroup.add(door)
                elif level[i][j] == "L":
                    door = Door((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), 0, lvl)
                    interactableGroup.add(door)
                    doorArray.append(door)
                elif level[i][j] == "B":
                    wall = Wall((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    interactableGroup.add(wall)
                elif level[i][j] == "H":
                    key = Key((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight))
                    interactableGroup.add(key)
                elif level[i][j] == "D":
                    npc = NPC((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), guard)
                    guard += 1
                    interactableGroup.add(npc)

        return [staticGroup, interactableGroup, destructableGroup, bgd, playerPos, levelScroll, doorArray, levelProgression]



class Menu(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.screens = []
        self.screens.append(InitialScreen(self))
        #self.screens.append(OptionsScreen(self))
        self.showScreen()

    def update(self, *args):
        return

    def events(self, eventList):
        for event in eventList:
            #Comprobar si se quiere salir
            if event.type == pygame.QUIT:
                self.director.exitGame()

        self.screens[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screens[self.currentScreen].draw(screen)


    def exitGame(self):
        self.director.exitGame()

    def playGame(self):
        phase = Olympus(self.director)
        self.director.stackScene(phase)

    def showScreen(self):
        self.currentScreen = 0
    # def mostrarPantallaConfiguracion(self):
    # self.pantallaActual = ...

class MenuPause(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.screens = []
        self.screens.append(PauseScreen(self))
        self.showScreen()

    def update(self, *args):
        return

    def events(self, eventList):
        for event in eventList:
            #Comprobar si se quiere salir
            if event.type == pygame.QUIT:
                self.director.exitGame()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.resumeGame()

        self.screens[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screens[self.currentScreen].draw(screen)


    def exitGame(self):
        self.director.exitGame()

    def resumeGame(self):
        self.director.exitScene()

    def showScreen(self):
        self.currentScreen = 0
