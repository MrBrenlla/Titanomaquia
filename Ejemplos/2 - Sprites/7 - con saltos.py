# -*- coding: utf-8 -*-

# -------------------------------------------------
# Importar las librerías
# -------------------------------------------------

from email import message
from multiprocessing.connection import wait
import pygame, sys, os
from pygame.locals import *

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
ATAQUE = 5

#Posturas
SPRITE_QUIETO = 2
SPRITE_ANDANDO = 0
SPRITE_SALTANDO = 1
SPRITE_MUERTE = 4
SPRITE_MURIENDO = 3
SPRITE_ATAQUE = 5

VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.2 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura




# -------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------

# El colorkey es es color que indicara la transparencia
#  Si no se usa, no habra transparencia
#  Si se especifica -1, el color de transparencia sera el del pixel (0,0)
#  Si se especifica un color, ese sera la transparencia
def load_image(name, colorkey=None):
    fullname = os.path.join('imagenes', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise (SystemExit, message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------

class Jugador(pygame.sprite.Sprite):
    "Jugador"

    def __init__(self):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self)
        # Se carga la hoja
        self.hoja = load_image('hera_baculo.png',-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # Leemos las coordenadas de un archivo de texto
        pfile=open('imagenes/coordHera.txt','r')
        datos=pfile.read()
        pfile.close()
        datos = datos.split()
        self.numPostura = 0
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [4, 1, 4, 5, 1, 4]    
        self.coordenadasHoja = []
        for linea in range(0, 6):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        print(self.coordenadasHoja[self.numPostura])
        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # La posicion inicial del Sprite
        self.rect = pygame.Rect(0,592,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # La posicion x e y que ocupa
        self.posicionx = 0
        self.posiciony = 592
        self.rect.left = self.posicionx
        self.rect.bottom = self.posiciony
        # Velocidad en el eje y (para los saltos)
        #  En el eje x se utilizaria si hubiese algun tipo de inercia
        self.velocidady = 0

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()



    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = RETARDO_ANIMACION_JUGADOR
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
                if self.numPostura == SPRITE_ATAQUE:
                    self.numPostura = SPRITE_QUIETO
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == DERECHA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == IZQUIERDA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    

    def mover(self,teclasPulsadas, arriba, abajo, izquierda, derecha):

        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        
        if teclasPulsadas[arriba]:
            # Si estamos en el aire y han pulsado arriba, ignoramos este movimiento
            if self.numPostura == SPRITE_SALTANDO:
                if teclasPulsadas[izquierda]:
                    self.movimiento = IZQUIERDA
                elif teclasPulsadas[derecha]:
                    self.movimiento = DERECHA
                else:
                    self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        elif teclasPulsadas[izquierda]:
            self.movimiento = IZQUIERDA
        elif teclasPulsadas[derecha]:
            self.movimiento = DERECHA
        else:
            if self.movimiento != ATAQUE:
                self.movimiento = QUIETO

    def ataquePrimario(self):
        self.movimiento = ATAQUE
        self.numPostura = SPRITE_ATAQUE
        


    def update(self, tiempo):
        # Si vamos a la izquierda
        if self.movimiento == IZQUIERDA:
            # Si no estamos en el aire, la postura actual sera estar caminando
            if (not self.numPostura == SPRITE_SALTANDO):
                self.numPostura = SPRITE_ANDANDO
            # Esta mirando a la izquierda
            self.mirando = IZQUIERDA
            # Actualizamos la posicion
            self.posicionx -= VELOCIDAD_JUGADOR * tiempo
            self.rect.left = self.posicionx
        # Si vamos a la derecha
        elif self.movimiento == DERECHA:
            # Si no estamos en el aire, la postura actual sera estar caminando
            if (not self.numPostura == SPRITE_SALTANDO):
                self.numPostura = SPRITE_ANDANDO
            # Esta mirando a la derecha
            self.mirando = DERECHA
            # Actualizamos la posicion
            self.posicionx += VELOCIDAD_JUGADOR * tiempo
            self.rect.left = self.posicionx
        # Si estamos saltando
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            self.velocidady = VELOCIDAD_SALTO_JUGADOR
        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO

        # Si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO:
            # Actualizamos la posicion
            self.posiciony -= self.velocidady * tiempo
            # Si llegamos a la posicion inferior, paramos de caer y lo ponemos como quieto
            if (self.posiciony>592):
                self.numPostura = SPRITE_QUIETO
                self.posiciony = 592
                self.velovidady = 0
            # Si no, aplicamos el efecto de la gravedad
            else:
                self.velocidady -= 0.004
            # Nos ponemos en esa posicion en el eje y
            self.rect.bottom = self.posiciony

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()
        return
        



# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((1280, 720), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Poner el título de la ventana
    pygame.display.set_caption('Ejemplo de uso de Sprites')

    # Creamos los jugadores
    jugador1 = Jugador()
    jugador2 = Jugador()

    # Creamos el grupo de Sprites de jugadores
    grupoJugadores = pygame.sprite.Group( jugador1, jugador2 )


    # El bucle de eventos
    while True:

        # Hacemos que el reloj espere a un determinado fps
        tiempo_pasado = reloj.tick(60)

        # Para cada evento, hacemos
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_k:
                jugador1.ataquePrimario()

        # Miramos que teclas se han pulsado
        teclasPulsadas = pygame.key.get_pressed()

        # Si la tecla es Escape
        if teclasPulsadas[K_ESCAPE]:
            # Se sale del programa
            pygame.quit()
            sys.exit()


        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        jugador2.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d)



        # Actualizamos los jugadores actualizando el grupo
        grupoJugadores.update(tiempo_pasado)


        # Dibujar el fondo de color
        pantalla.fill((133,133,133))

        # Dibujar el grupo de Sprites
        grupoJugadores.draw(pantalla)
        
        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main()
