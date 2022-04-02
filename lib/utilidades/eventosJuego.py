import re
from lib import c


def obstaculos_nivel(nivel,
                     nivelPrevio,
                     nivelFinal):
    '''[Aqui es donde cambiamos los niveles en base al orden 
        de los obstaculos]

    Args: 
        [nivel] ([str]) : [En que nivel de la app estamos] 
        [nivelPrevio] ([str]) : [Nivel anterior para comenzar los obstaculos] 
        [nivelFinal] ([str]) : [Nivel posterior para comenzar los obstaculos] 
    '''

    if len(c.DATA_TO_FRONT['posicionObstaculos']) > 0:
        obstaculos = [
            'obstaculo'+str(int(c.DATA_TO_FRONT['posicionObstaculos'][0])),
            'obstaculo'+str(int(c.DATA_TO_FRONT['posicionObstaculos'][1])),
            'obstaculo'+str(int(c.DATA_TO_FRONT['posicionObstaculos'][2])),
            'obstaculo'+str(int(c.DATA_TO_FRONT['posicionObstaculos'][3]))
        ]
        # Cada uno de estos numeros corresponde al nivel en relacion a la tabla
        # hecha por Misael en Notion

        # Obstaculo = Nivel
        nivelStart = {
            'obstaculo1': 4,
            'obstaculo2': 5,
            'obstaculo3': 6,
            'obstaculo4': 7,
            'obstaculo5': 8,
            'obstaculo6': 9
        }
        # Nivel = Obstaculo
        nivelS = {
            'nivel4': 1,
            'nivel5': 2,
            'nivel6': 3,
            'nivel7': 4,
            'nivel8': 5,
            'nivel9': 6,
            'nivel10': 10
        }
        getIndexActual = obstaculos.index('obstaculo'+str(nivelS[str(nivel)]))
        c.DATA_TO_FRONT['posicionRuta'] = getIndexActual + 1
        try:
            Atras = obstaculos[getIndexActual-1] if getIndexActual != 0 else nivelPrevio 
            Adelante = obstaculos[getIndexActual+1]
            # print('{} -- Obstaculo{} -- Atras: {} -- Adelante: {}'.format(nivel, nivelS[str(nivel)], Atras, Adelante))
            return {'atras':Atras, 'adelante': Adelante}
        except IndexError:
            Atras = obstaculos[getIndexActual-1]
            Adelante = nivelFinal
            # print('{} -- Obstaculo{} -- Atras: {} -- Adelante: {}'.format(nivel, nivelS[str(nivel)], Atras, Adelante))
            return {'atras':Atras, 'adelante': Adelante}


def reto_nivel_check(levelFromFront, 
                     nivelPrevio=3,
                     nivelFinal=10):
    """[Obtenemos la posicion anterior o posterior del nivel]

    Args:
        levelFromFront ([string]): [Es el nivel donde estamos
                                    la nomenglatura es: 
                                    'nivel8']
        [nivelPrevio] ([str]) : [Nivel anterior para comenzar los obstaculos] 
        [nivelFinal] ([str]) : [Nivel posterior para comenzar los obstaculos] 

    Returns:
        [dict]: ['atras', 'adelante']
    """
    enQueNivelEstamos = levelFromFront
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    filterString = temp.match(enQueNivelEstamos).groups()

    nivelAdelante = int(filterString[1]) + 1

    if int(filterString[1]) > 0:
        nivelAtras = int(filterString[1]) - 1
    else:
        nivelAtras = 0
    
    # posiciones = {
    #     'atras': nivelAtras,
    #     'adelante': nivelAdelante
    # }
    # print('nivel'+str(filterString[1]))
    if int(filterString[1]) >= nivelPrevio and int(filterString[1]) < nivelFinal:
        posicionObstaculos = obstaculos_nivel('nivel'+str(filterString[1]),
                                             nivelPrevio,
                                             nivelFinal)
        # print(obstaculos_nivel(posiciones['adelante']))
        posiciones = {
            'atras': posicionObstaculos['atras'],
            'adelante': posicionObstaculos['adelante'] 
        }
    else:
        posiciones = {
            'atras': nivelAtras,
            'adelante': nivelAdelante 
        }
    return posiciones
