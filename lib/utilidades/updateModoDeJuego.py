from lib import numeroJugadores
from lib import c
from lib.utilidades import resetAll as reset

def update():
    numJ = numeroJugadores.get_players()

    try:
        if len(numJ.index) < 2:
            c.MODO_DE_JUEGO = 'Solo'
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                ' Solo ',
                '>>>>>>>>>>>>>>>>>>>>>>>>')
        else:
            c.MODO_DE_JUEGO = 'Multijugador'
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                ' Multijugador ',
                '>>>>>>>>>>>>>>>>>>>>>>>>')
    except AttributeError:
        print('Aqui no existen los jugadores')
        reset.resetSesion()