import pygame
from gestorRecursos import *


class Suelo(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargamos la imagen
        self.imagen = GestorRecursos.CargarImagen('SueloOlimpo.png')
        # El rectangulo donde estara la imagen
        self.rect = self.imagen.get_rect()

    def dibuja(self, pantalla, posicion):
        self.rect.left = posicion[0]
        self.rect.top = posicion[1]
        pantalla.blit(self.imagen, self.rect)

class Plataforma(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self,rectangulo):
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.posicion = (self.rect.left, self.rect.bottom)
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen("Plataforma.png")

    def dibuja(self, pantalla, posicion):
        self.rect.left = posicion[0]
        self.rect.top = posicion[1]
        pantalla.blit(self.image, self.rect)

class Jarron(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    # Primero invocamos al constructor de la clase padre
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargamos la imagen
        self.imagen = GestorRecursos.CargarImagen('Jarron.png')
        # El rectangulo donde estara la imagen
        self.rect = self.imagen.get_rect()

    def dibuja(self, pantalla, posicion):
        self.rect.left = posicion[0]
        self.rect.top = posicion[1]
        pantalla.blit(self.imagen, self.rect)

#Generador automatico de niveles a partir de txt
class GeneradorNiveles(object):
    "Generador de niveles con un txt"
    
    @classmethod
    def genNivel(self, txt, pantalla):
        #leemos el txt para saber que elemetos colocar
        nivel = GestorRecursos.CargarNivelTxt(txt)
        sueloOlimpo = Suelo()
        plataforma = Plataforma(pygame.Rect(0, 0, 128, 128))
        jarron = Jarron()
        
        nivel = nivel.split("\n")
        l = len(nivel)
        for i in range(l):
            for j in range(len(nivel[0])):
                if nivel[i][j] == "A":
                    sueloOlimpo.dibuja(pantalla, ((j*128), (i*128)-(l*128-720)))
                if nivel[i][j] == "E":
                    plataforma.dibuja(pantalla, ((j*128), (i*128)-(l*128-720)))
                if nivel[i][j] == "C" or nivel[i][j] == "G":
                    jarron.dibuja(pantalla, ((j*128), (i*128)-(l*128-720)))
                    
        