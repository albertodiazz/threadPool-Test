from lib import numeroJugadores
from lib import c
from lib.utilidades import resetAll as reset

def update():
    numJ = numeroJugadores.get_players()

    try:
        if len(numJ.index) < c.MIN_JUGADORES:
            c.MODO_DE_JUEGO = 'Solo'
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                ' No llego al minimo de Jugadores',
                '>>>>>>>>>>>>>>>>>>>>>>>>')
            reset.resetSesion()
        else:
            c.MODO_DE_JUEGO = 'Multijugador'
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                ' Multijugador ',
                '>>>>>>>>>>>>>>>>>>>>>>>>')
    except AttributeError:
        print('Aqui no existen los jugadores')
        reset.resetSesion()
