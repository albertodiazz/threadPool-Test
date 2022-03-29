from lib import pd
from lib import c


def delete(_ID_):
    player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)

    try:
        player = player.drop(_ID_)
        player.to_csv(c.DIR_DATA+'info_sesion.csv')
    except KeyError:
        print('El usuario no existe:')
        pass
