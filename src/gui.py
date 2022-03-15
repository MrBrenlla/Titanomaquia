from math import floor
import pygame
from gestorRecursos import *
from config import *

class GUIElement():
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect

    def setPosition(self, position):
        (posX, posY) = position
        self.rect.center = position
        # self.rect.left = posX
        # self.rect.bottom = posY

    def inElementPosition(self, position):
        (posX, posY) = position

        if (posX >= self.rect.left) and (posX <= self.rect.right) and (posY <= self.rect.bottom) and (posY >= self.rect.top):
            return True
        else:
            return False

    def draw(self):
        raise NotImplemented("Tiene que implementar el metodo draw.")
    def action(self):
        raise NotImplemented("Tiene que implementar el metodo action.")


class GUIButton(GUIElement):
    def __init__(self, screen, image, position, size, chroma):

        self.image = GestorRecursos.CargarImagen(image, chroma)
        self.image = pygame.transform.scale(self.image, size)
        super().__init__(screen, self.image.get_rect())

        self.setPosition(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 4)

class PlayButton(GUIButton):
    def __init__(self, screen, image, position):
        super().__init__(screen, image, position, (220, 60), -1)

    def action(self):
        self.screen.menu.playGame()

class ContinueButton(GUIButton):
    def __init__(self, screen, image, position):
        super().__init__(screen, image, position, (220, 60), -1)

    def action(self):
        self.screen.menu.resumeGame()
        # pygame.mixer.music.stop()

class OptionsButton(GUIButton):
    def __init__(self, screen, image, position):
        super().__init__(screen, image, position, (220, 60), -1)

    def action(self):
        self.screen.menu.changeToOptions()

class BackButton(GUIButton):
    def __init__(self, screen, image, position):
        super().__init__(screen, image, position, (220, 60), -1)

    def action(self):
        self.screen.menu.showScreen()

class QuitButton(GUIButton):
    def __init__(self, screen, image, position):
        super().__init__(screen, image, position, (220, 60), -1)

    def action(self):
        self.screen.menu.exitGame()


class SelectPlayerButton(GUIButton):
    def __init__(self, screen, image, position, player):
        super().__init__(screen, image, position, (200, 200), -1)
        self.player = player

    def action(self):
        self.screen.menu.playGame(self.player)

class SelectLevelButton(GUIButton):
    def __init__(self, screen, image, position, level):
        super().__init__(screen, image, position, (400, 400), None)
        self.level = level

    def action(self):
        self.screen.menu.characterSelect(self.level)

class ChangeVolumeButton(GUIButton):
    def __init__(self, screen, image, position, type, change, text):
        super().__init__(screen, image, position, (50, 50), -1)
        self.type = type
        self.change = change
        self.textB = text
    def action(self):
        if self.type == "musica":
            Config.musicVolume += self.change
            if Config.musicVolume > 0.1: Config.musicVolume = 0.1
            if Config.musicVolume < 0: Config.musicVolume = 0
            self.textB.change(str(floor(Config.musicVolume * 100)))
            pygame.mixer.music.set_volume(Config.musicVolume)
        else:
            Config.effectsVolume += self.change
            if Config.effectsVolume > 0.1: Config.effectsVolume = 0.1
            if Config.effectsVolume < 0: Config.effectsVolume = 0
            self.textB.change(str(floor(Config.effectsVolume * 100)))

class GUIText(GUIElement):
    def __init__(self, screen, font, color, text, position):
        self.font = font
        self.color = color
        self.outline = font.render(text, True, (0, 0, 0))
        self.image = font.render(text, True, color)
        super().__init__(screen, self.image.get_rect())
        self.setPosition(position)

    def draw(self, screen):
        #draw outline
        stroke = 3
        #top left
        screen.blit(self.outline, (self.rect.x - stroke, self.rect.y - stroke))
        #top center
        screen.blit(self.outline, (self.rect.x, self.rect.y - stroke))
        screen.blit(self.outline, (self.rect.x - stroke, self.rect.y))
        #top right
        screen.blit(self.outline, (self.rect.x + stroke, self.rect.y - stroke))
        #bottom left
        screen.blit(self.outline, (self.rect.x - stroke, self.rect.y + stroke))
        #bottom center
        screen.blit(self.outline, (self.rect.x, self.rect.y + stroke))
        screen.blit(self.outline, (self.rect.x + stroke, self.rect.y))
        #bottom left
        screen.blit(self.outline, (self.rect.x + stroke, self.rect.y + stroke))
        #real text
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 4)

    def action(self):
        return

    def change(self, text):
        self.outline = self.font.render(text, True, (0, 0, 0))
        self.image = self.font.render(text, True, self.color)

class MusicVolumeText(GUIText):
    def __init__(self, screen):
        font = pygame.font.Font('Fonts/OLYMB.ttf', 70)
        super().__init__(screen, font, (255, 255, 255), str(floor(Config.musicVolume * 100)), (780, 375))
    

class SoundVolumeText(GUIText):
    def __init__(self, screen):
        font = pygame.font.Font('Fonts/OLYMB.ttf', 70)
        super().__init__(screen, font, (255, 255, 255), str(floor(Config.effectsVolume * 100)), (780, 300))




class LevelText(GUIText):
    def __init__(self, screen, level, pos):
        font = pygame.font.Font('Fonts/OLYMB.ttf', 40)
        super().__init__(screen, font, (255, 255, 255), level, pos)
        self.level = level

    def action(self):
        self.screen.menu.characterSelect(self.level)



class GUIScreen():
    def __init__(self, menu, image, colorKey):
        self.menu = menu
        self.image = GestorRecursos.CargarImagen(image, colorKey)
        self.image = pygame.transform.scale(self.image, (1280, 640))
        self.GUIElements = []

        #lista de elementos gui

    def events(self, eventList):

        for event in eventList:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.elementClick = None
                for element in self.GUIElements:
                    if element.inElementPosition(event.pos):
                        self.elementClick = element
            if event.type == MOUSEBUTTONUP and event.button == 1:
                for element in self.GUIElements:
                    if element.inElementPosition(event.pos):
                        if (element == self.elementClick):
                            element.action()

    def draw(self, screen):
        # Dibujamos primero la imagen de fondo
        screen.blit(self.image, (0, 0))
        # pygame.draw.line(screen, (255, 255, 255), (640, 0), (640, 640))
        # Después los botones
        for element in self.GUIElements:
            element.draw(screen)


class InitialScreen(GUIScreen):
    def __init__(self, menu):
        super().__init__(menu, "Menu/fondoMenuES.png", None)
        playButton = PlayButton(self, "Menu/fondo.png", (640, 310))
        optionsButton = OptionsButton(self, "Menu/fondo.png", (640, 375))
        quitButton = QuitButton(self, "Menu/fondo.png", (640, 440))
        

        self.GUIElements.append(playButton)
        self.GUIElements.append(optionsButton)
        self.GUIElements.append(quitButton)



class PauseScreen(GUIScreen):
    def __init__(self, menu):
        super().__init__(menu, "Menu/fondoMenuPausa4.png", None)
        continueButton = ContinueButton(self, "Menu/fondo.png", (135, 275))
        optionsButton = OptionsButton(self, "Menu/fondo.png", (135, 340))
        quitButton = QuitButton(self, "Menu/fondo.png", (135, 405))


        self.GUIElements.append(continueButton)
        self.GUIElements.append(optionsButton)
        self.GUIElements.append(quitButton)


class OptionsScreen(GUIScreen):
    def __init__(self, menu):
        super().__init__(menu, "Menu/menuOpciones.png", None)
        #adjust volume
        #playButton = PlayButton(self, "Menu/fondo.png", (640, 310))
        #optionsButton = QuitButton(self, "Menu/fondo.png", (640, 375))
        backButton = BackButton(self, "Menu/fondo.png", (640, 440))
        musicVolumeText = MusicVolumeText(self)
        musicVoumeUpButton = ChangeVolumeButton(self, "Menu/fondo.png", (850, 375), "musica", 0.01, musicVolumeText)
        musicVoumeDownButton = ChangeVolumeButton(self, "Menu/fondo.png", (700, 375), "musica", -0.01, musicVolumeText)
        soundVolumeText = SoundVolumeText(self)
        effectVoumeUpButton = ChangeVolumeButton(self, "Menu/fondo.png", (850, 300), "efectos", 0.01, soundVolumeText)
        effectVoumeDownButton = ChangeVolumeButton(self, "Menu/fondo.png", (700, 300), "efectos", -0.01, soundVolumeText)

        self.GUIElements.append(backButton)
        self.GUIElements.append(musicVolumeText)
        self.GUIElements.append(musicVoumeUpButton)
        self.GUIElements.append(musicVoumeDownButton)
        self.GUIElements.append(soundVolumeText)
        self.GUIElements.append(effectVoumeUpButton)
        self.GUIElements.append(effectVoumeDownButton)


class SelectionScreen(GUIScreen):
    def __init__(self, menu):
        super().__init__(menu, "Menu/menuSeleccionPersonaje.png", None)

        for i in range(len(Config.availableCharacters)):
            #creamos un boton para cada personaje
            if i < 3:
                selection = SelectPlayerButton(self, f"Menu/{Config.availableCharacters[i]}Menu.png", (364+276*i, 300), Config.availableCharacters[i])
                self.GUIElements.append(selection)
            else:
                selection = SelectPlayerButton(self, f"Menu/{Config.availableCharacters[i]}Menu.png", (364+276*(i-3), 540), Config.availableCharacters[i])
                self.GUIElements.append(selection)


class LevelSelectionScreen(GUIScreen):
    def __init__(self, menu):
        super().__init__(menu, "Menu/menuSeleccionNivel.png", None)

        if len(Config.availableLevels) == 1:
            text = LevelText(self, Config.availableLevels[0], (640, 400))
            selection = SelectLevelButton(self, f"Menu/{Config.availableLevels[0]}Menu.png", (640, 420), Config.availableLevels[0])
            self.GUIElements.append(selection)
            self.GUIElements.append(text)
        else:
            text = LevelText(self, Config.availableLevels[0], (640-228, 400))
            selection = SelectLevelButton(self, f"Menu/{Config.availableLevels[0]}Menu.png", (640-228, 420), Config.availableLevels[0])
            self.GUIElements.append(selection)
            self.GUIElements.append(text)
            text = LevelText(self, Config.availableLevels[1], (640+228, 400))
            selection = SelectLevelButton(self, f"Menu/{Config.availableLevels[1]}Menu.png", (640+228, 420), Config.availableLevels[1])
            self.GUIElements.append(selection)
            self.GUIElements.append(text)