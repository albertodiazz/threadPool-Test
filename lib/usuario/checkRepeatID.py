class no_hay_repetidos(Exception):
    pass


def safeID(ID, data):
    """[Funcion para verificar ID repetidos]

    Args:
        ID ([string]): [ID jugador]
        data ([dataFrame]): [Data de personajes.csv]

    Raises:
        no_hay_repetidos: [description]

    Returns:
        [data, numJugadoresFix]: [
            1.-([dataFrame]) = Data arreglada sin el repetido
            2.-([int]) = numero de jugadores restado de los eliminados
        ]
    """
    if len(data[data.index.duplicated()]) > 0:
        data = data[~data.index.duplicated(keep='first')]
        numJugadoresFix = len(data.index)
        return data, numJugadoresFix
    else:
        raise no_hay_repetidos('No hay repetidos')
