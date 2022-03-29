import time
from lib.usuario import numeroJugadores
from lib import c
from lib import updateModoDeJuego


def convert(seconds):
    """[Funcion para convertir segundos a formato 00:00]

    Args:
        seconds ([int]): [esperamos el time_in_seconds de cronometro]

    Returns:
        [array]: [regresamos dos strings]
    """
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d" % (minutes), "%02d" % (seconds)


def comparacionTiempos(tiempo, minutos_meta, segundos_meta, emit=None):
    """[Funcion en donde restamos los valores del tiempo meta]
        .......................
        IMPORTANTE aqui usamos la variable global
        esta funcion nos regresa los minutos y segundos restantes
        eso se lo tenemos que compartir a front
        .......................
    Args:
        tiempo ([dict]): [minutos y segundos de la funcion cronometro]
        minutos_meta ([string]): [esperamos string de la funcion convert]
        segundos_meta ([string]): [esperamos string de la funcion convert]
        emit ([socketIO]): [Eso hay que agragarlo cundo lo setemos a socket io]
    """
    global tiempoGlobal
    minutos = "%02d" % (tiempo['minutos'])
    segundos = "%02d" % (tiempo['segundos'])
    if int(segundos_meta) != 0:
        # GLOBAL
        c.TIEMPO_GLOBAL['minutos'] = "%02d" % (int(minutos_meta)-(int(minutos))) # noqa
        c.TIEMPO_GLOBAL['segundos'] = "%02d" % (int(segundos_meta)-int(segundos)) # noqa
        print(c.TIEMPO_GLOBAL)
    elif int(segundos_meta) == 0:
        # GLOBAL
        c.TIEMPO_GLOBAL['minutos'] = "%02d" % (int(minutos_meta)-(int(minutos))) # noqa
        c.TIEMPO_GLOBAL['segundos'] = "%02d" % (int(59)-int(segundos))
        print(c.TIEMPO_GLOBAL)


def temporizador(time_in_seconds, _queue_):
    """[Funcion de temporizador]
        ................................
        Funciona para restar el tiempo, sera utilizada como temporizador en
        un juego multijugador. Donde al terminar el tiempo se ejecutara una
        accion en el juego.
        ................................
    Args:
        time_in_seconds ([int]): [hay que meter los minutos en conversion a
                                    segundos tipo 120 para 2 minutos]
    Returns:
        [array]: [regresamos dos strings]
    """
    # GLOBAL
    ########################################
    c.CRONOMETRO = 'PLAY'
    ########################################
    minutos_meta, segundos_meta = convert(time_in_seconds)
    count = 0
    tiempo = {'minutos': 0, 'segundos': -1}
    seguro = 0
    while True:
        tiempo['segundos'] += 1
        if tiempo['segundos'] > 59:
            tiempo['segundos'] = 0
            tiempo['minutos'] += 1
        elif int(segundos_meta) > seguro:
            if count > int(segundos_meta):
                segundos_meta = 59
                tiempo['segundos'] = 0
                tiempo['minutos'] += 1
                seguro = 129128098
        comparacionTiempos(tiempo, minutos_meta, segundos_meta)
        # print("%02d:%02d" % (tiempo['minutos'], tiempo['segundos']))
        time.sleep(1)
        count += 1
        if count > time_in_seconds or c.CRONOMETRO == 'STOP':
            '''Se acabo el tiempo'''
            # GLOBAL
            ########################################
            c.TIEMPO_GLOBAL = {'minutos': 0, 'segundos': 0}
            c.THREADS_CRONOMETRO = False
            c.CRONOMETRO = 'STOP'
            #######################################
            updateModoDeJuego.update()
            # numJ = numeroJugadores.get_players()

            # if len(numJ.index) < 2:
            #     c.MODO_DE_JUEGO = 'Solo'
            # else:
            #     c.MODO_DE_JUEGO = 'Multijugador'
            return
