#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
from nivel import *
from pygame.locals import *
import sys


if __name__ == '__main__':

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((1280, 720), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()


    # El bucle de eventos
    while True:

        # Sincronizar el juego a 60 fps
        tiempo_pasado = reloj.tick(60)

        # Para cada evento, hacemos
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                GeneradorNiveles.genNivel("templo2.txt", pantalla)


        pygame.display.update()

