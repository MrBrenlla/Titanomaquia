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
    screen = pygame.display.set_mode((1280, 640), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    clock = pygame.time.Clock()

    #Variables globales juego
    fps = 60
    level = Level(screen)
    true_scroll = [0,0]
    

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
            if event.type == KEYDOWN and event.key == K_LEFT:
                level.clearLevel()
                level.loaded = False
                level.currentLevel = (level.currentLevel - 1) % 5
            if event.type == KEYDOWN and event.key == K_RIGHT:
                level.clearLevel()
                level.loaded = False
                level.currentLevel = (level.currentLevel + 1) % 5



        if not(level.loaded):
            level.loadLevel()
            level.loaded = True
        player = level.player

        if( (((player.rect.x-true_scroll[0]-640)/10)>=0 or true_scroll[0]>0) and ((true_scroll[0]<(level.level_size[level.currentLevel][0]*128-1280-4)) or ((player.rect.x-true_scroll[0]-640)/10)<=0 )):
            true_scroll[0] += (player.rect.x-true_scroll[0]-640)/10

        if ( ((true_scroll[1]>(level.level_size[level.currentLevel][1]*(-128)+640+4)) or (((player.rect.y-true_scroll[1]-200)/10)>=0)) and (((player.rect.y-true_scroll[1]-200)/10)<=0 or true_scroll[1]<0) ):
            true_scroll[1] += (player.rect.y-true_scroll[1]-200)/10   
        
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        if scroll[0] < 0: scroll[0] = 0
        if scroll[1] > 0: scroll[1] = 0

        # print("scroll: ",scroll)
        # player = GestorRecursos.CargarImagen("sprite_0.png", -1)
        # screen.blit(player, (1280-128*3, 84))
        keys = pygame.key.get_pressed()
        level.update(screen, keys, scroll)
        #TODO: hacer que el mapa solo se desplace en determinados momentos
        
        pygame.display.update()

