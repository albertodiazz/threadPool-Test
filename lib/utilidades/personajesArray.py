from lib import pd
from lib import c


def get():
    personT = pd.read_csv(c.DIR_DATA+"Personajes.csv", index_col=0)
    result = personT.Jugador_ID.replace('Nada', '').values.tolist()
    return result
