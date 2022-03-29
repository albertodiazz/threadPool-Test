from lib import json
from lib import c

'''
Aqui manejamos todos los mensajes relacions con el json to_front
hay que recordar que es el json que compartimos con front
'''


def add_level_reto_automatic(_type_='nivel'):
    """[Agregamos de manera automatica un +1 al level en el json]

    Args:
        _type_ (str, optional): [podemos acceder a 'nivel' o 'reto'].
                                Defaults to 'nivel'.

    Returns:
        [type]: [description]
    """
    open_json = open(c.DIR_DATA+"to_front.json")
    levels = json.load(open_json)
    count_levels = None

    count_levels = int(levels['General'][_type_]) + 1
    levels['General'][_type_] = count_levels

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(levels, f)
        f.close()

    open_json.close()
    return {'response': 'Ok add ' + _type_}


def add_confirmaciones_automatic(nivel_name, mode='Momentos'):
    """[Esta funcion debebemos ocuparla para
        todos los niveles que necesiten confirmaciones
        por parte de todos los jugadores. Lo que hace es agregar
        de forma automatica al json los jugadores que le han dado
        ha cofirmar]
    ..................................................
    IMPORTANTE si agregas un nivel nuevo recuerda en seguir
    la estructura del json ['nivel_name']['confirmacion']
    ..................................................
    Args:
        nivel_name ([string]): [nombre del nivel en el json]
        mode ([string]): [nombre del root json para acceder a los atributos]
    """
    # Necesitamos saber de quien viene la confirmacion?
    # Considero que no ya que no aparece un mensaje especial por jugador
    open_json = open(c.DIR_DATA+"to_front.json")
    confirmaciones = json.load(open_json)
    count_confir = 0
    print(mode, nivel_name)
    count_confir = int(confirmaciones[mode][nivel_name]['confirmacion']) + 1 # noqa
    confirmaciones[mode][nivel_name]['confirmacion'] = count_confir

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(confirmaciones, f)
        f.close()
    open_json.close()


def add_respuestas(nivel_name, respuestas, mode='Momentos'):
    """[Funcion donde recivimos respuestas y la alamcenamos
    en un array, para despues ser guardadas en un JSON]

    Args:
        nivel_name ([type]): [description]
        respuestas ([type]): [description]
        mode (str, optional): [asi accedemos al JSON dentro debe
                                contener los atributos:
                                respuestas].
                                Defaults to 'Momentos'.
                                'Retos'
    """
    open_json = open(c.DIR_DATA+"to_front.json")
    confirmaciones = json.load(open_json)

    lista = confirmaciones[mode][nivel_name]['respuestas']
    if type(lista) == list:
        lista.append(respuestas)
        confirmaciones[mode][nivel_name]['respuestas'] = lista
    else:
        confirmaciones[mode][nivel_name]['respuestas'] = [respuestas]  # noqa

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(confirmaciones, f)
        f.close()

    open_json.close()


def only_save(data):
    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(data, f)
        f.close()
    return 'salvado'


def reset_confirmaciones(nivel_name, mode='Momentos'):
    open_json = open(c.DIR_DATA+"to_front.json")
    confirmaciones = json.load(open_json)
    confirmaciones[mode][nivel_name]['confirmacion'] = 0

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(confirmaciones, f)
        f.close()

    open_json.close()


def reset_respuestas(nivel_name, mode='Momentos'):
    open_json = open(c.DIR_DATA+"to_front.json")
    confirmaciones = json.load(open_json)
    confirmaciones[mode][nivel_name]['respuestas'] = ''

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(confirmaciones, f)
        f.close()

    open_json.close()


def reset():
    open_reset = open(c.DIR_DATA+"to_front_RESET.json")
    to_front = json.load(open_reset)

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(to_front, f)
        f.close()
    open_reset.close()
