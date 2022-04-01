import re
from lib import c


def obstaculos_nivel(nivel):
    '''[Aqui es donde cambiamos los niveles en base al orden 
        de los obstaculos]

    Args: 
        [nivel] ([str]) : [En que nivel de la app estamos] 
    '''
    # TODO
    # [x] Aqui es donde condicionamos el avanze a los obstaculos
    # [] Esta bugeado lo mejor es hacer la pruba en ocasiones me llega
    #    mandar de golpe al nivel 10
    # [] Si te da tiemnpo generar una unit Test usando la funcion de
    #    generar los obstaculos random y esto

    # Cada uno de estos numeros corresponde al nivel en relacion a la tabla
    # hecha por Misael en Notion
    relacion = [None, 4, 5, 6, 7, 8, 9]
    # Esto lo hago por que debemos en si mi cambio de niveles sigue siendo
    # secuencial y no aleatrio cada uno esta linkeado a un valor de lectura
    # del array de obstaculos
    if len(c.DATA_TO_FRONT['posicionObstaculos']) > 0:
        niveles = {
            'nivel'+str(relacion[int(c.DATA_TO_FRONT['posicionObstaculos'][0])]): 0,
            'nivel'+str(relacion[int(c.DATA_TO_FRONT['posicionObstaculos'][1])]): 1,
            'nivel'+str(relacion[int(c.DATA_TO_FRONT['posicionObstaculos'][2])]): 2,
            'nivel'+str(relacion[int(c.DATA_TO_FRONT['posicionObstaculos'][3])]): 3
        }
        if int(c.DATA_TO_FRONT['posicionObstaculos'][0]) != 1:
            try:
                nivel = "nivel"+str(nivel+1)
                # print('Niveles: {}'.format(niveles))
                return relacion[int(c.DATA_TO_FRONT['posicionObstaculos'][niveles[nivel]])]
            except KeyError:
                # Llegamos al final del array y en base a la tabla de Misa el siguiente nivel
                # que va despues de los obstaculose es el 10 de lo lograron 
                # (Es el nivel de resultado fianal)
                # FIXME se refiere que estamos en el nivel3 y necesitamos saber lo que va
                # antes del nivel3 no de lo que va antes de obstaculos
                if nivel == 'nivel2':
                    return 2
                else:
                    return 10
        else:
            try:
                print("************")
                nivelA = "nivel"+str(nivel+1)
                # print('Niveles: {}'.format(niveles))
                return relacion[int(c.DATA_TO_FRONT['posicionObstaculos'][niveles[nivelA]])]
            except KeyError as error:
                try:
                    nivel = "nivel"+str(nivel)
                    # print('Niveles: {}'.format(niveles))
                    return relacion[int(c.DATA_TO_FRONT['posicionObstaculos'][niveles[nivel]])]
                except:
                    # Llegamos al final del array y en base a la tabla de Misa el siguiente nivel
                    # que va despues de los obstaculose es el 10 de lo lograron 
                    # (Es el nivel de resultado fianal)
                    # FIXME se refiere que estamos en el nivel3 y necesitamos saber lo que va
                    # antes del nivel3 no de lo que va antes de obstaculos
                    if nivel == 'nivel2':
                        return 2
                    else:
                        return 10


def reto_nivel_check(levelFromFront):
    """[Obtenemos la posicion anterior o posterior del nivel]

    Args:
        levelFromFront ([string]): [Es el nivel donde estamos
                                    la nomenglatura es: 
                                    'nivel8']

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
    if int(filterString[1]) >= 3 and int(filterString[1]) < 10:
        # print(obstaculos_nivel(posiciones['adelante']))
        posiciones = {
            'atras': obstaculos_nivel(nivelAtras),
            'adelante': obstaculos_nivel(nivelAdelante)
        }
    else:
        posiciones = {
            'atras': nivelAtras,
            'adelante': nivelAdelante 
        }
    return posiciones
