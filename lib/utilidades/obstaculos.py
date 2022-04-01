from lib import config as c 
import random


def run():
    '''Funcion donde seleccionamos de forma aleatoria los 4
    onbstaculos de 6 que contiene la actividad'''
    obstaculos = [1, 2, 3, 4, 5, 6]
    for i in range(2):
        r = random.randint(0, len(obstaculos))
        obstaculos.pop(r-1)
    c.DATA_TO_FRONT['posicionObstaculos'] = obstaculos

