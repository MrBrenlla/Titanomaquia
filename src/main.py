#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
from level import *
from pygame.locals import *
from characters import *
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

        bgd = GestorRecursos.CargarImagen("Fondo.jpg")

        # Para cada evento, hacemos
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                #futuro menu pausa
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_LEFT:
                level.clearLevel(screen, bgd)
                level.loaded = False
                level.currentLevel = (level.currentLevel - 1) % 5
            if event.type == KEYDOWN and event.key == K_RIGHT:
                level.clearLevel(screen, bgd)
                level.loaded = False
                level.currentLevel = (level.currentLevel + 1) % 5



        screen.blit(bgd, (0, 0))
        if not(level.loaded):
            level.loadLevel(screen)
            level.loaded = True

        # player = GestorRecursos.CargarImagen("sprite_0.png", -1)
        # screen.blit(player, (1280-128*3, 84))
        
        keys = pygame.key.get_pressed()
        level.update(screen, keys)

        
        pygame.display.update()

