import pygame
from pygame.locals import *


class Director():

    def __init__(self):
        #Inicializamos la pantalla
        self.screen = pygame.display.set_mode((1280, 640), 0, 32)
        pygame.display.set_caption("Titanomaquia")
        #Pila de escenas
        self.scenes = []
        # Flag para salir de la escena
        self.exitScn = False
        self.fps = 60
        # Reloj para sincronizacion
        self.clock = pygame.time.Clock()

    def gameLoop(self, scene):
        self.exitScn = False

        #Eliminamos eventos producidos previos al bucle
        pygame.event.clear()

        while not self.exitScn:
            #Sincronizamos por tiempo
            time = self.clock.tick(self.fps)

            scene.events(pygame.event.get())
            scene.update(time)
            scene.draw(self.screen)
            pygame.display.flip()

    def execute(self):
        while(len(self.scenes) > 0):
            #Ejecutamos el bucle hasta que termina la escena de la pila
            print(self.scenes)
            self.gameLoop(self.scenes[len(self.scenes)-1])

    def exitScene(self):
        #Indicamos que queremos salir de escena
        self.exitScn = True

        #Eliminamos de la pila
        if (len(self.scenes) > 0):
            self.scenes.pop()
        
    def exitGame(self):
        #Vaciamos la lista de escenas pendientes
        self.scenes = []
        self.exitScn = True

    def changeScene(self, scene):
        #Salimos de la escena actual y anhadimos la nueva
        self.exitScene()
        self.scenes.append(scene)

    def stackScene(self, scene):
        #Apilamos la ecena por encima de la actual
        self.exitScn = True
        self.scenes.append(scene)