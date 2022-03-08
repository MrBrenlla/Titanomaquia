#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
from director import *
from scenes import *



if __name__ == '__main__':

    # Inicializar pygame
    pygame.init()

    #Creamos el director
    director = Director()
    
    #Creamos la primera escena
    scene = Menu(director)


    director.stackScene(scene)

    director.execute()

    pygame.quit()
