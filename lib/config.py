
# SOCKETIO PORT
PORT = 3000
# Seteamos a produccion o seguimos en debug mode que es True
DEBUG_MODE = True
ASYNC_MODE = None
# Aqui seteamos si queremos usar el index html
INDEX_MODE = True
# Aqui es donde tenemos almacenado el index HTML
DIR_INDEX = '/mnt/d/trabajo/cocay/ramodelacion_Mide/radioGrafia_BancoCentral/Backend/lib/socketIO/frontTest/' # noqa
# Aqui seteamos el url de la carpeta data
DIR_DATA = 'data/'
SERVER_LEVEL = 'server:level'
SERVER_TIME = 'server:time'
SERVER_RESPONSE = 'server:response'
'''
..............................
        GLOBAL VARIABLES
..............................
'''
# Para saber si hay un thread del cronometro corriendo
# Nos sirve para saber cuando fue incializado en app.py
THREADS_CRONOMETRO = False
# Con esta variable sabemos cuando el cronometro esta en
# STOP/PLAY. Esta variable la solemos utilizar en subfunciones
# por ejemplo en waitMoments
CRONOMETRO = 'STOP'
# En este variable obetnemos nuestro contador de mayor a menor
TIEMPO_GLOBAL = {'minutos': 0, 'segundos': 0}
####################################
# Modo de Juego "Solo/MultiJugador"
# Esto se debe seter de forma automatica no
# es necesario cambiarlo manual
MODO_DE_JUEGO = 'Multijugador'
####################################
DATA_TO_FRONT = {
        'level': 0,
        'players': [],
        'characters': ["", "", "", "",
                       "", "", "", "",
                       "", "", ""],
        'respuestas': "",
        'respuestasCorrectas': "false",
        'respuestasFinales': []
}
'''
..............................
        SETUP JUEGO
..............................
'''
####################################
''' Tiempo'''
# Tiempos expresado en segundos si quieres 2min serian 120s
# Temporizador para seleccionar personajes
TIME_SECONDS = 30
# Temporizador para unirse al juego
JOIN_SECONDS = 3
# Segundos de momentos
MOMENTOS_SECONDS = 3
####################################
''' Niveles '''
# Cantindad maxima de jugadores. La app no tiene un limite
# de jugadores, sin embargo esta varibale es necesaria setearla,
# para el tiempo de espera en la pantalla de unirse, ya que si se
# se unes los dictados por esta variable omitimos el cronometro
MAX_JUGADORES = 3
####################################
