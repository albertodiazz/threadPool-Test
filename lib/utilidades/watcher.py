from lib import config as c # noqa
import time
import json 
from lib import emit


def run():
    # TODO
    # [] Terminar la implementacion de esto en todo el programa
    # [x] Correrlo en Thread como lo estabas haciendo antes cuando alguien se conecte 
    '''Cada que cambie alguna variable emitimos un mensaje'''
    print('Iniciando WATCHER')
    primerEstado = list(c.DATA_TO_FRONT.values())
    while(True):
        list1 = list(c.DATA_TO_FRONT.values())
        for i in range(len(list1)):
            if list1[i] != primerEstado[i]:
                print('<<<<<<<<<<<<<<')
                print('<<<<<<<<<<<<<<')
                print('<<<WATCHER<<<')
                primerEstado = list(c.DATA_TO_FRONT.values())
                emit(c.SERVER_LEVEL,
                     json.dumps(c.DATA_TO_FRONT, indent=4),
                     broadcast=True)
                print('<<<<<<<<<<<<<<')
                print('<<<<<<<<<<<<<<')
                print('<<<<<<<<<<<<<<')
        time.sleep(0.5)
    return
