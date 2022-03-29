from lib import Players
from lib import pd
from lib import np
from lib import c
from lib.usuario import checkRepeatID


def create_player(ID):
    """ Funcion para crear personajes
    ...............
    - No hay un limite de personajes
    - safeID ([def]) = arreglamos ID repetidos
    ...............
    Args:
        ID ([string]): [Id del Jugador en sesion]

    Returns:
        [allData ([dataFrame]), numJugadores ([int])]: [
            .......................................
            -allData = dataFrame,
            -numJugadores = numero de jugadores
            .......................................
            ]
    """
    players = []
    allData = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
    players.append(Players.Jugadores())
    players[len(players)-1].newPlayer(ID)
    allData = allData.append([players[len(players)-1].Datos])
    numJugadores = len(allData.index)
    try:
        allData, numFix = checkRepeatID.safeID(ID, allData)
        numJugadores = numFix
        allData.to_csv(c.DIR_DATA+'info_sesion.csv')
        return allData, numJugadores
    except checkRepeatID.no_hay_repetidos:
        print('Todo bien')
        allData.to_csv(c.DIR_DATA+'info_sesion.csv')
        return allData, numJugadores


def seleccionDePersonaje(ID, ID_Person, data, confirmacion=False):
    """Funcion para seleccion personaje

    Args:
        ID ([string]): [ID del Jugador]
        ID_Person ([int]): [ID del personaje ha elegir]
        data ([dataFrame]): [Tabla de datos de Usuarios]
        confirmacion (bool, optional): [
            1.- Solo debe ser enviada una vez].
                                                Defaults to False.

    Returns:
        [type]: [description]
    """
    personT = pd.read_csv(c.DIR_DATA+"Personajes.csv", index_col=0)
    getSi = personT.loc[personT.Disponible == 'Si'].index
    estaDisponible = np.any(np.array(getSi == ID_Person))
    habiaElegido = personT.loc[personT.Jugador_ID == ID].index
    confirmados = personT.loc[personT['Confirmacion'] == 'Confirmado']
    confirResultado = np.any(np.array(confirmados.Jugador_ID == ID))
    if confirResultado:
        return {'response': 'Ya no puedes elegir, haz confirmado un personaje'}
    else:
        if len(data.index[data.index == ID]) > 0:
            if confirmacion:
                if len(habiaElegido) > 0:
                    if personT.loc[personT.Jugador_ID == ID].index[0] == ID_Person: # noqa
                        personT.at[ID_Person, 'Confirmacion'] = 'Confirmado'
                        personT.to_csv(c.DIR_DATA + "Personajes.csv")
                        print({'reponse': 'Confirmado'})
                    else:
                        return {'response': 'Este personaje no es tuyo'}
                else:
                    return {'response': 'Elige primero el personaje'}
            elif estaDisponible:
                if len(habiaElegido) > 0:
                    select = personT.loc[personT.Jugador_ID == ID].index[0]
                    personT.at[select, 'Jugador_ID'] = 'Nada'
                    personT.at[select, 'Disponible'] = 'Si'
                # Ojo aqui no pongo condicional solo utilizo
                # la logica de ejecucion de Python
                personT.at[ID_Person, 'Jugador_ID'] = ID
                personT.at[ID_Person, 'Disponible'] = 'No'
                personT.to_csv(c.DIR_DATA+"Personajes.csv")
                # Aqui marcamos la verificacion una vez que nos confirme
                return {'response': 'Se modifico la tabla de Personajes'}
            else:
                print(estaDisponible)
                return {'response': 'No disponible'}
        else:
            return {'response': 'No existe el ID del Jugador'}
