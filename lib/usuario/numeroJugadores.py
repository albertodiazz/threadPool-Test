from typing import Any
from lib import pd
from lib import c


def get_players():
    """[Funcion para saber quienes son los ljugadores]

    Returns:
        [DataFrame]: [regresamos los player]
    """
    player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
    players = player.loc[player.TipoDeUsuario == 'player']

    if len(players) > 0:
        return players
