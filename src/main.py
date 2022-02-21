#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
from level import *
from pygame.locals import *
import sys


if __name__ == '__main__':

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    screen = pygame.display.set_mode((1280, 720), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    clock = pygame.time.Clock()

    #Variables globales juego
    fps = 60

    level = Level()


    # El bucle de eventos
    while True:

        # Sincronizar el juego a 60 fps
        time = clock.tick(fps)

        # Para cada evento, hacemos
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                #futuro menu pausa
                pygame.quit()
                sys.exit()
        

        bgd = GestorRecursos.CargarImagen("Fondo.jpg")
        screen.blit(bgd, (0, 0))
        level.currentLevel = 2
        level.clearLevel(screen)
        level.loadLevel(screen)

        player = GestorRecursos.CargarImagen("sprite_0.png", -1)
        screen.blit(player, (1280-128*3, 84))
        player = GestorRecursos.CargarImagen("sprite_hera.png", -1)
        screen.blit(player, (800, 464))

        
        pygame.display.update()

