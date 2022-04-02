from lib import eventosJuego
from lib import obstaculos 
from lib import c 


def cambioNivelesObstaculos():
    for i in range(500):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        obstaculos.run()
        print(c.DATA_TO_FRONT['posicionObstaculos'])
        nivelStart = {
            'obstaculo1': 4,
            'obstaculo2': 5,
            'obstaculo3': 6,
            'obstaculo4': 7,
            'obstaculo5': 8,
            'obstaculo6': 9
        }
        nivelS = {
            'nivel4': 1,
            'nivel5': 2,
            'nivel6': 3,
            'nivel7': 4,
            'nivel8': 5,
            'nivel9': 6,
            'nivel10': 10
        }

        for levels in range(len(c.DATA_TO_FRONT['posicionObstaculos'])):
            getObstaculos = 'obstaculo'+ str(c.DATA_TO_FRONT['posicionObstaculos'][levels])
            posicion = eventosJuego.reto_nivel_check('nivel'+str(nivelStart[getObstaculos]))
            # print('Obs: {} Obs: {}'.format(getObstaculos, nivelS['nivel'+str(posicion['adelante'])]))
 

if __name__ == '__main__':
    cambioNivelesObstaculos()
