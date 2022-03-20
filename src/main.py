#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
from director import *
from scenes import *



if __name__ == '__main__':

    # Inicializar pygame
    pygame.init()

    #Inicializar modulo de Sonidos
    pygame.mixer.pre_init(44100, 16, 1, 4096)
    pygame.mixer.init()

    #Creamos el director
    director = Director()

    #Creamos la primera escena
    scene = SubTemple(director,"Poseidon")#Menu(director)


    director.stackScene(scene)

    director.execute()

    pygame.quit()
