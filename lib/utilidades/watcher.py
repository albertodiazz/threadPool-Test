from lib import config as c # noqa
import asyncio
import time
import json 
from lib import emit
from lib import webSocketMessage 


def run():
    # TODO
    # [x] Terminar la implementacion de esto en todo el programa
    # [x] Correrlo en Thread como lo estabas haciendo antes cuando alguien se conecte 
    # [] Los array no se estan comparando en tiempo real y el problema esta cuando
    # alguien abandona o se une. Si no lo logras solucionar relativamente rapido mejor
    # pasate a otra cosa y esos array emitelos como estabana antes
    # [] Una prueba que puedes haver es separar todo por tipos
    # [] O en ultimas crear una variable que se actualize 
    '''Cada que cambie alguna variable emitimos un mensaje'''
    print('\n Iniciando WATCHER \n')
    primerEstado = list(c.DATA_TO_FRONT.values())
    while(True):
        list1 = list(c.DATA_TO_FRONT.values())
        for i in range(len(list1)):
            if list1[i] != primerEstado[i]:
                print('<<<<<<<<<<<<<<')
                print('<<<<<<<<<<<<<<')
                print('<<<WATCHER<<<')
                primerEstado = list(c.DATA_TO_FRONT.values())
                asyncio.run(webSocketMessage.sendMessage(msg='CambioDeNivel'))
                emit(c.SERVER_LEVEL,
                     json.dumps(c.DATA_TO_FRONT, indent=4),
                     broadcast=True)
                print('<<<<<<<<<<<<<<')
                print('<<<<<<<<<<<<<<')
                print('<<<<<<<<<<<<<<')
        time.sleep(0.5)
    return
