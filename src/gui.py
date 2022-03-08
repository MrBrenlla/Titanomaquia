import pygame
from gestorRecursos import *

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
    def __init__(self, screen, image, position):

        self.image = GestorRecursos.CargarImagen(image, -1)
        self.image = pygame.transform.scale(self.image, (200, 60))
        super().__init__(screen, self.image.get_rect())

        self.setPosition(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 4)

class PlayButton(GUIButton):
    def __init__(self, screen, image, position):
        super().__init__(screen, image, position)

    def action(self):
        self.screen.menu.playGame()

class QuitButton(GUIButton):
    def __init__(self, screen, image, position):
        super().__init__(screen, image, position)

    def action(self):
        self.screen.menu.exitGame()


class GUIText(GUIElement):
    def __init__(self, screen, font, color, text, position):
        self.image = font.render(text, True, color)
        super().__init__(screen, self.image.get_rect(), 40)
        self.setPosition(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 4)


# class PlayText(GUIText):
#     def __init__(self, screen):
#         font = pygame.font.Font('Fonts/OLYMB.ttf', 40)
#         super().__init__(screen, font, (0, 0, 0), "PLAY", (640, 302))

#     def action(self):
#         self.screen.menu.playGame()

# class QuitText(GUIText):
#     def __init__(self, screen):
#         font = pygame.font.Font('Fonts/OLYMB.ttf', 40)
#         super().__init__(screen, font, (0, 0, 0), "QUIT", (640, 402))

#     def action(self):
#         self.screen.menu.exitGame()


# class TitleText(GUIText):
#     def __init__(self, screen):
#         font = pygame.font.SysFont('supermario256', 140)
#         super().__init__(screen, font, (255, 255, 255), "TITANOMAQUIA", (50, 200))
    
#     def action(self):
#         return


    
class GUIScreen():
    def __init__(self, menu, image):
        self.menu = menu
        self.image = GestorRecursos.CargarImagen(image)
        self.image = pygame.transform.scale(self.image, (1280, 640))
        self.GUIElements = []

        #lista de elementos gui
        
    def events(self, eventList):
        
        for event in eventList:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.GUIElements:
                    if element.inElementPosition(event.pos):
                        self.elementClick = element
            if event.type == MOUSEBUTTONUP:
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
        super().__init__(menu, "Menu\\fondoMenu.png")
        playButton = PlayButton(self, "Menu\\fondo.png", (640, 310))
        optionsButton = QuitButton(self, "Menu\\fondo.png", (640, 375))
        quitButton = QuitButton(self, "Menu\\fondo.png", (640, 440))
        # playText = PlayText(self)
        # quitText = QuitText(self)
        # titleText = TitleText(self)
        
        self.GUIElements.append(playButton)
        self.GUIElements.append(optionsButton)
        self.GUIElements.append(quitButton)
        # self.GUIElements.append(playText)
        # self.GUIElements.append(quitText)
        # self.GUIElements.append(titleText)