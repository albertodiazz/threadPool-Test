from lib import pd
from lib import c
'''
    Con estas funciones cambiamos los status de player a user o viceversa.
'''


def change_to_player(_ID_):
    # Aqui cambiamos el tipo de usuario a player
    player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)

    try:
        if player.loc[_ID_].TipoDeUsuario == 'user':
            player.at[_ID_, 'TipoDeUsuario'] = 'player'
            player.to_csv(c.DIR_DATA+'info_sesion.csv')

            return {'response': 'Se cambio a player'}
        else:
            return {'response': 'Ya es un player'}
    except KeyError:
        print('El usuario no existe:')
        pass


def change_to_user(_ID_):
    player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)

    try:
        if player.loc[_ID_].TipoDeUsuario == 'player':
            player.at[_ID_, 'TipoDeUsuario'] = 'user'
            player.to_csv(c.DIR_DATA+'info_sesion.csv')
            return {'response': 'Se cambio a user'}
        else:
            return {'response': 'Ya es un user'}
    except KeyError:
        print('El usuario no existe:')
        pass
