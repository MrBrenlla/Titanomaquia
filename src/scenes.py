from turtle import Screen
import pygame
from pygame.locals import *
from gestorRecursos import *
from sprites import *
from characters import *
from gui import *
from config import *

#Constantes acceso a grupos del nivel
# FLOOR_GROUP = 0
# VASE_GROUP = 1
# PLATFORM_GROUP = 2
STATIC_GROUP = 0
INTERACTABLE_GROUP = 1
DESTRUCTABLE_GROUP = 2
ENEMY_GROUP = 3
BACKGROUND = 4
PLAYER_POS = 5
SCROLL = 6
DOORS = 7
LEVEL_PROGRESSION = 8

class Scene():
    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update")
    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo events")
    def draw(self, screen):
        raise NotImplemented("Tiene que implementar el metodo draw")


class Phase(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.screenWidth = 1280
        self.screenHeight = 640
        self.tileSize = 128

    def events(self, eventList):
        for event in eventList:
            #Comprobar si se quiere salir
            if event.type == pygame.QUIT:
                self.director.exitGame()
            if event.type == KEYDOWN and event.key == K_e:
                self.player.interact(self.screens[self.currentLevel][INTERACTABLE_GROUP], self)
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.stackScene(MenuPause(self.director))
            if event.type == self.player.invencibilityCD:
                self.player.invencibility = False
                pygame.time.set_timer(self.player.invencibilityCD, 0)

        keys = pygame.key.get_pressed()
        #Acciones posibles del player
        self.player.move(keys, K_w, K_d, K_a)
        self.player.attack(eventList)
        

    def playerLimits(self):

        levelWidth = self.levelSize[self.currentLevel][0]*128

        if self.player.rect.x < 0:
            self.player.rect.x = 0
        if self.player.rect.x > levelWidth - self.player.rect.width:
            self.player.rect.x = levelWidth - self.player.rect.width


    def clearScreen(self, screen):
        self.screens[self.currentLevel][STATIC_GROUP].clear(screen, self.screens[self.currentLevel][BACKGROUND])
        self.screens[self.currentLevel][INTERACTABLE_GROUP].clear(screen, self.screens[self.currentLevel][BACKGROUND])
        self.screens[self.currentLevel][DESTRUCTABLE_GROUP].clear(screen, self.screens[self.currentLevel][BACKGROUND])

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

        for s in self.screens[self.currentLevel][ENEMY_GROUP].sprites():
            s.draw(screen,self.scroll)

        self.player.draw(screen, self.scroll)
        self.LifeGUI.draw(screen)

    def genLevel(self, lvlName,  txt, lvl, playerPos, doorsDis):
        #leemos el txt para saber que elemetos colocar
        level = GestorRecursos.CargarNivelTxt(f"{lvlName}/{txt}")
        level = level.split("\n")
        subLevel = txt.split(".")[0]
        l = len(level)
        bgd = Background(0, -(l*self.tileSize-self.screenHeight), lvl, lvlName)
        # print(bgd.rect)
        doors = 1 + doorsDis
        # floorGroup = pygame.sprite.Group()
        # vaseGroup = pygame.sprite.Group()
        # platformGroup = pygame.sprite.Group()
        staticGroup = pygame.sprite.Group()
        interactableGroup = pygame.sprite.Group()
        destructableGroup = pygame.sprite.Group()
        enemyGroup = pygame.sprite.Group()
        levelScroll = [0, 0]
        doorArray = []
        levelProgression = 0
        guard = 0
        for i in range(l):
            for j in range(len(level[0])):
                if level[i][j] == "A":
                    floor = Floor((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight),lvlName)
                    # floorGroup.add(floor)
                    staticGroup.add(floor)
                elif level[i][j] == "B": #Vasija que contiene hidromiel
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight), 1)
                    # vaseGroup.add(vase)
                    destructableGroup.add(vase)
                elif level[i][j] == "C": #Vasija que contiene llave
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight), 2)
                    # vaseGroup.add(vase)
                    destructableGroup.add(vase)
                elif level[i][j] == "D":
                    npc = NPC((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), guard, lvlName, subLevel)
                    guard += 1
                    interactableGroup.add(npc)
                elif level[i][j] == "E":
                    platform = Platform((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight),lvlName)
                    # platformGroup.add(platform)
                    staticGroup.add(platform)
                elif level[i][j] == "F":
                    offset = 0
                    if lvlName == "Olimpo":
                        offset = self.tileSize/2
                    door = Door((j*self.tileSize), (i*self.tileSize - offset)-(l*self.tileSize-self.screenHeight), doors, lvl,lvlName, True)
                    doors += 1
                    doorArray.append(door)
                    interactableGroup.add(door)
                elif level[i][j] == "G": #Vasija que contiene nada
                    #orginal vase size is 4 times smaller than grid size
                    vase = Vase((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight), 0)
                    # vaseGroup.add(vase)
                    destructableGroup.add(vase)
                elif level[i][j] == "H":
                    key = Key((j*self.tileSize + (self.tileSize / 4)), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight))
                    interactableGroup.add(key)
                elif level[i][j] == "I":
                    pGuard = PracticeGuard((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    destructableGroup.add(pGuard)
                elif level[i][j] == "J":
                    enemy = Mermaids((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight-10), self)
                    enemyGroup.add(enemy)
                elif level[i][j] == "K":
                    medal = Medal((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    interactableGroup.add(medal)
                elif level[i][j] == "L":
                    door = Door((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), 0, lvl,lvlName, True)
                    interactableGroup.add(door)
                    doorArray.append(door)
                elif level[i][j] == "M":
                    mirror = Mirror((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    interactableGroup.add(mirror)
                elif level[i][j] == "N":
                    godObj = GodObject((j*self.tileSize + self.tileSize/4), (i*self.tileSize + self.tileSize/2)-(l*self.tileSize-self.screenHeight), lvlName)
                    interactableGroup.add(godObj)
                elif level[i][j] == "O":
                    valve = Valve((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight))
                    interactableGroup.add(valve)
                elif level[i][j] == "P":
                    door = Door((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight), doors, lvl,lvlName, False)
                    doors += 1
                    doorArray.append(door)
                    interactableGroup.add(door)
                elif level[i][j] == "Q":
                    enemy = Espiritu((j*self.tileSize), (i*self.tileSize)-(l*self.tileSize-self.screenHeight-10), self)
                    enemyGroup.add(enemy)

        return [staticGroup, interactableGroup, destructableGroup, enemyGroup, bgd, playerPos, levelScroll, doorArray, levelProgression]


class Olympus(Phase):

    def __init__(self, director, player):
        super().__init__(director)

        GestorRecursos.CargarSonido("Musica_Olimpo.wav",True)
        pygame.mixer.music.set_volume(Config.musicVolume)
        pygame.mixer.music.play()

        #Info del nivel
        self.screens = []
        self.levels = ["olimpo.txt", "templo1.txt", "templo2.txt", "templo3.txt", "temploZeus.txt"]
        self.levelSize = [[49,5],[21,9],[21,9], [16,8], [21, 9]]
        self.changeLevel = False
        self.currentLevel = 0
        self.lastLevel = 0

        self.playerName = player

        self.LifeGUI = LifeGUI("Barra de vida.png","VidaCoords.txt")
        #grupos

        for level in range(len(self.levels)):
            # print(level)
            self.screens.append(super().genLevel("Olimpo", self.levels[level], level, (300, 500), 0))

        if player == "Hera":
            self.player = Hera(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Demeter":
            self.player = Demeter(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Hestia":
            self.player = Hestia(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Zeus":
            self.player = Zeus(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Hades":
            self.player = Hades(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Poseidon":
            self.player = Poseidon(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])

        self.player.addObserver(self.LifeGUI)


    def update(self, time):
        super().updateScroll()
        super().playerLimits()
        dropItems = self.player.update(self.screens[self.currentLevel][STATIC_GROUP],self.screens[self.currentLevel][ENEMY_GROUP], self.screens[self.currentLevel][DESTRUCTABLE_GROUP])
        for item in dropItems:
            self.screens[self.currentLevel][INTERACTABLE_GROUP].add(item)
        for s in self.screens[self.currentLevel][ENEMY_GROUP]:
            s.move_enemy(self,self.screens[self.currentLevel][STATIC_GROUP])

        #condicion de muerte
        if (self.player.lifes == 0 and self.player.currentAnim == SPRITE_LET_DYING):
            #lanzar la escena de muerte
            self.director.stackScene(DeathMenu(self.director))

        #condicion de fin de nivel
        if (self.currentLevel == 4 and self.screens[self.currentLevel][LEVEL_PROGRESSION] == 1):
            if not("Zeus" in Config.availableCharacters):
                Config.availableCharacters.append("Zeus")
            #self.director.changeScene(LevelSelectionMenu(self.director))
            if Config.availableLevels == []:
                Config.availableLevels.append("TemploSubmarino")
                Config.availableLevels.append("Infierno")
                self.director.changeScene(LevelSelectionMenu(self.director))
                #self.director.changeScene(Menu(self.director))
            else:
                self.director.changeScene(LevelSelectionMenu(self.director))


class SubTemple(Phase):

    def __init__(self, director, player):
        super().__init__(director)

        GestorRecursos.CargarSonido("Musica_SubTemple.wav",True)
        pygame.mixer.music.set_volume(Config.musicVolume)
        pygame.mixer.music.play()

        #Info del nivel
        self.screens = []
        self.levels = ["templo.txt", "salaEnemigos.txt", "salaInutil.txt", "salaPuzle.txt", "salaFinal.txt"]
        self.levelSize = [[10,13],[21,5], [33, 5],[21,5], [21, 5]]
        self.changeLevel = False
        self.currentLevel = 0
        self.lastLevel = 0

        self.playerName = player

        self.LifeGUI = LifeGUI("Barra de vida.png","VidaCoords.txt")
        self.sand = Sand(0, -512)
        #grupos

        for level in range(len(self.levels)):
            # print(level)
            if level == 0:
                playerPos = (200, -520)
            elif level == 2:
                playerPos = (3900, 500)
            else:
                playerPos = (300, 500)
            self.screens.append(super().genLevel("TemploSubmarino", self.levels[level], level, playerPos, 0))
        if player == "Hera":
            self.player = Hera(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Demeter":
            self.player = Demeter(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Hestia":
            self.player = Hestia(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Zeus":
            self.player = Zeus(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Hades":
            self.player = Hades(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Poseidon":
            self.player = Poseidon(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])

        self.player.addObserver(self.LifeGUI)

        self.screens[self.currentLevel][STATIC_GROUP].add(self.sand)

    def update(self, time):
        super().updateScroll()
        super().playerLimits()
        dropItems = self.player.update(self.screens[self.currentLevel][STATIC_GROUP],self.screens[self.currentLevel][ENEMY_GROUP], self.screens[self.currentLevel][DESTRUCTABLE_GROUP])
        for item in dropItems:
            self.screens[self.currentLevel][INTERACTABLE_GROUP].add(item)
        for s in self.screens[self.currentLevel][ENEMY_GROUP]:
            s.move_enemy(self,self.screens[self.currentLevel][STATIC_GROUP])
        #lose condition
        if (self.player.lifes == 0 and self.player.currentAnim == SPRITE_LET_DYING):
            #lanzar la escena de muerte
            self.director.stackScene(DeathMenu(self.director))
        
        #sand control
        if (self.screens[1][LEVEL_PROGRESSION] == 1):
            sandPos = 0
            if (self.screens[3][LEVEL_PROGRESSION] == 1):
                sandPos = 512
            self.sand.rect.y = sandPos

        #win condition
        if (self.currentLevel == 4 and self.screens[self.currentLevel][LEVEL_PROGRESSION] == 1):
            if not("Poseidon" in Config.availableCharacters):
                Config.availableCharacters.append("Poseidon")
            Config.availableLevels.remove("TemploSubmarino")
            if Config.availableLevels == []:
                self.director.stackScene(WinMenu(self.director))
            else:
                self.director.changeScene(LevelSelectionMenu(self.director))


class Hell(Phase):

    def __init__(self, director, player):
        super().__init__(director)

        GestorRecursos.CargarSonido("Musica_Hell.wav",True)
        pygame.mixer.music.set_volume(Config.musicVolume)
        pygame.mixer.music.play()

        #Info del nivel
        self.screens = []
        
        self.levels = ["puertas.txt", "enemigos.txt", "puertas.txt", "enemigos.txt", "puertas.txt", "enemigos.txt", "enemigos.txt", "enemigos.txt", "enemigos.txt", "salaFinal.txt"]
        self.levelSize = [[26, 5], [17, 5], [26, 5], [17, 5], [26, 5], [17, 5], [17, 5], [17, 5], [17, 5], [21, 5]]
        self.changeLevel = False
        self.currentLevel = 0
        self.lastLevel = 0

        self.playerName = player

        self.LifeGUI = LifeGUI("Barra de vida.png","VidaCoords.txt")
        #grupos

        for level in range(len(self.levels)):
            # print(level)
            doorDis = 0
            if level == 2:
                doorDis = 3
            if level == 4:
                doorDis = 6
            self.screens.append(super().genLevel("Infierno", self.levels[level], level, (300, 500), doorDis))

        if player == "Hera":
            self.player = Hera(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Demeter":
            self.player = Demeter(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Hestia":
            self.player = Hestia(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Zeus":
            self.player = Zeus(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Hades":
            self.player = Hades(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])
        elif player == "Poseidon":
            self.player = Poseidon(self.screens[self.currentLevel][PLAYER_POS][0], self.screens[self.currentLevel][PLAYER_POS][1])

        self.player.addObserver(self.LifeGUI)


    def update(self, time):
        super().updateScroll()
        super().playerLimits()
        dropItems = self.player.update(self.screens[self.currentLevel][STATIC_GROUP],self.screens[self.currentLevel][ENEMY_GROUP], self.screens[self.currentLevel][DESTRUCTABLE_GROUP])
        for item in dropItems:
            self.screens[self.currentLevel][INTERACTABLE_GROUP].add(item)
        for s in self.screens[self.currentLevel][ENEMY_GROUP]:
            s.move_enemy(self,self.screens[self.currentLevel][STATIC_GROUP])

        #condicion de muerte
        if (self.player.lifes == 0 and self.player.currentAnim == SPRITE_LET_DYING):
            #lanzar la escena de muerte
            self.director.stackScene(DeathMenu(self.director))

        #condicion de fin de nivel
        if (self.currentLevel == 9 and self.screens[self.currentLevel][LEVEL_PROGRESSION] == 1):
            if not("Hades" in Config.availableCharacters):
                Config.availableCharacters.append("Hades")
            Config.availableLevels.remove("Infierno")
            if Config.availableLevels == []:
                self.director.stackScene(WinMenu(self.director))
            else:
                self.director.changeScene(LevelSelectionMenu(self.director))



class Menu(Scene):
    def __init__(self, director):
        super().__init__(director)

        GestorRecursos.CargarSonido("Main_Menu.wav",True)
        pygame.mixer.music.set_volume(Config.musicVolume)
        pygame.mixer.music.play()

        self.screens = []
        self.screens.append(InitialScreen(self))
        self.screens.append(OptionsScreen(self))
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
        phase = CharacterSelectionMenu(self.director)
        self.director.changeScene(phase)

    def changeToOptions(self):
        self.currentScreen = 1

    def showScreen(self):
        self.currentScreen = 0
    # def mostrarPantallaConfiguracion(self):
    # self.pantallaActual = ...

class MenuPause(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.screens = []
        self.screens.append(PauseScreen(self))
        self.screens.append(OptionsScreen(self))
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

    def changeToOptions(self):
        self.currentScreen = 1

    def resumeGame(self):
        self.director.exitScene()

    def showScreen(self):
        self.currentScreen = 0


class CharacterSelectionMenu(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.screens = []
        self.screens.append(SelectionScreen(self))
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


    def playGame(self, player):
        pygame.mixer.music.stop()
        phase = Olympus(self.director, player)
        self.director.changeScene(phase)

    def changeToOptions(self):
        self.currentScreen = 1

    def showScreen(self):
        self.currentScreen = 0
    # def mostrarPantallaConfiguracion(self):
    # self.pantallaActual = ...

class LevelSelectionMenu(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.screens = []
        self.screens.append(LevelSelectionScreen(self))
        self.screens.append(SelectionScreen(self))
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


    def playGame(self, player):
        pygame.mixer.music.stop()
        if self.level == "TemploSubmarino":
            phase = SubTemple(self.director, player)
        else:
            phase = Hell(self.director, player)
        self.director.changeScene(phase)

    def characterSelect(self, level):
        self.level = level
        self.currentScreen = 1

    def showScreen(self):
        self.currentScreen = 0


class DeathMenu(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.screens = []
        self.screens.append(DeathScreen(self))
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

    def changeToOptions(self):
        self.currentScreen = 1

    def retry(self):
        self.director.scenes = []
        Config.availableCharacters = ["Hera", "Hestia", "Demeter"]
        Config.availableLevels = ["TemploSubmarino", "Infierno"]
        self.director.changeScene(Menu(self.director))


    def showScreen(self):
        self.currentScreen = 0



class WinMenu(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.screens = []
        self.screens.append(WinScreen(self))
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

    def changeToOptions(self):
        self.currentScreen = 1

    def retry(self):
        self.director.scenes = []
        self.director.changeScene(Menu(self.director))


    def showScreen(self):
        self.currentScreen = 0
