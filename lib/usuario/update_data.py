from lib import pd
from lib import c


def update_info_jugador():
    """[
        Funcion donde actualizamos el csv info_sesion con el csv de Personajes
        Info_Csv es nuestra data main por eso necesito tener centralizada la
        informacion en ese documento.
    ]

    Returns:
        [DataFrame]: [Data actualizada de info_sesion.csv]
    """
    players = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
    personajes = pd.read_csv(c.DIR_DATA+'Personajes.csv', index_col=0)

    playersA = players.index.to_list()
    personajesB = personajes.loc[personajes.Jugador_ID != 'Nada'].Jugador_ID.to_list() # noqa
    sumAll = playersA + personajesB

    find_ID = [n for n in sumAll if sumAll.count(n) > 1]
    _ID_Finds = list(set(find_ID))
    df = pd.DataFrame([])
    for i in range(len(_ID_Finds)):
        df = df.append(personajes.loc[personajes.Jugador_ID == _ID_Finds[i]])
    df = df.drop('Disponible', axis=1)
    df = df.reset_index().set_index('Jugador_ID')
    update_ = df.rename(columns={'ID': 'SeleccionID',
                                 'Confirmacion': 'StatusConfirmacion'})

    players.StatusConfirmacion = players.StatusConfirmacion.astype(str)
    for i in range(len(update_)):
        players.at[update_.index[i],
                   'StatusConfirmacion'] = update_.StatusConfirmacion[i]
        players.at[update_.index[i],
                   'SeleccionID'] = update_.SeleccionID[i]

    players.to_csv(c.DIR_DATA+'info_sesion.csv')
    return players
