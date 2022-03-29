
import threading
import flask
from lib import SocketIO, disconnect, emit
from lib import Flask
from lib import copy_current_request_context
from lib import c
from lib import json
from lib import queue
from lib import pd
from lib import funcionesJugador
from lib import cronometro
from lib import update_data
from lib import resetAll as reset
from lib import changeTipo
from lib import deletUser
from lib import waitMoments
from lib import handle_json
from lib import updateModoDeJuego
from lib import personajesArray
from lib import CORS

app = Flask(__name__, template_folder=c.DIR_INDEX)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=c.ASYNC_MODE)
CORS(app)

work_queue = queue.Queue()


class SocketIOEventos(Exception):
    pass


# Con esta condicion lo que hacemos es setear el modo, si quieres cambiarlo
# ve al archivo de config.py y pon el INDEX_MODE = False
if c.INDEX_MODE:
    print(c.INDEX_MODE)
    from flask import render_template

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html', async_mode=socketio.async_mode)
else:
    @app.route('/')
    def index():
        return '<p>Hellow World desde Flask </p>'


@socketio.on('connect')
def connect(evento):
    # Aqui no importa si son dos o mas jugadores
    try:
        # Comprobamos conexiones de clientes
        app.logger.info('connect: ',
                        'Alguien se conecto al servidor: ',
                        flask.request.sid)
        # Creamos jugador por sesion con el atributo user
        # en unirse se lo cambiamos a player
        funcionesJugador.create_player(flask.request.sid)
        emit(c.SERVER_LEVEL,
             json.dumps(c.DATA_TO_FRONT, indent=4),
             broadcast=True)
    except TypeError:
        app.logger.info('No hay conexion con el servidor')
        return


@socketio.on('disconnect')
def on_disconnect():
    try:
        deletUser.delete(flask.request.sid)
        print('\n', '<<<<<<<< Alguien se deconecto >>>>>>>')
        print(flask.request.sid)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            c.DATA_TO_FRONT['players'].remove(flask.request.sid)
        except ValueError:
            # No existe en la lista
            pass
        try:
            c.DATA_TO_FRONT['characters'].remove(flask.request.sid)
        except ValueError:
            # No existe en la lista
            pass
        emit(c.SERVER_LEVEL,
             json.dumps(c.DATA_TO_FRONT, indent=4),
             broadcast=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    except TypeError:
        app.logger.info('No hay conexion con el servidor')
        disconnect()
        return


@socketio.on('/user/start')
def userStart(jsonMsg):
    """[Solo funciona para cambiar el video]"""
    # Una vez recibamos el ID de quien sea empezamos la applicacion
    # Aqui no importa si son dos o mas jugadores
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Aqui ejecutamos la funcion
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            c.DATA_TO_FRONT['level'] = 1
            emit(c.SERVER_LEVEL,
                 json.dumps(c.DATA_TO_FRONT, indent=4),
                 broadcast=True)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            app.logger.info({'userStart': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userStart': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/user/unirme')
def userUnirme(jsonMsg):
    """[Aqui es donde creamos el Jugador]"""
    # Aqui es donde manejamos los usuarios que se unan al juego
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Aqui ejecutamos la funcion
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            c.DATA_TO_FRONT['players'].append(msg['ID'])
            emit(c.SERVER_LEVEL,
                 json.dumps(c.DATA_TO_FRONT, indent=4),
                 broadcast=True)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            changeTipo.change_to_player(msg['ID'])
            ##########################################
            '''IMPORTANTE aqui revizamos el modo de juego
               una vez acabado el temporizador'''
            ##########################################
            # GLOBAL
            if c.THREADS_CRONOMETRO:
                print('<<<<<<<< Cronometo is running >>>>>>>>>')
            else:
                print('<<<<<<<< Cronometo START >>>>>>>>>')
                _cronometro_ = threading.Thread(target=cronometro.temporizador,
                                                args=(c.JOIN_SECONDS,
                                                      work_queue))
                _cronometro_.start()
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                _waitMoments_ = threading.Thread(target=copy_current_request_context(waitMoments.wait_join_players)) # noqa
                _waitMoments_.start()

                # GLOBAL
                c.THREADS_CRONOMETRO = _waitMoments_.is_alive()
            app.logger.info({'userUnirme': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userUnirme': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/player/seleccion')
def userSeleccion(jsonMsg):

    _cronometro_ = threading.Thread(target=cronometro.temporizador,
                                    args=(c.TIME_SECONDS,
                                          work_queue))
    if c.THREADS_CRONOMETRO:
        # Revizamos que no este corriendo el Thread
        print('<<<<<<<<<<<<<<<<< ',
              'Cronometro is running', ' >>>>>>>>>')
    else:
        _cronometro_.start()
        c.THREADS_CRONOMETRO = _cronometro_.is_alive()
        _waitMoments_ = threading.Thread(target=copy_current_request_context(waitMoments.wait_confirmacion_characters)) # noqa
        _waitMoments_.start()
        print('<<<<<<<<<<<<<<<<< ', 'Start Cronometro: ',
              c.THREADS_CRONOMETRO, ' >>>>>>>>>>>>>')
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            if len(msg['seleccion']) >= 2:
                ''' Aqui ejecutamos la funcion '''
                players = pd.read_csv(c.DIR_DATA+'info_sesion.csv',
                                      index_col=0)
                seleccion = int(msg['seleccion'][0])

                if msg['seleccion'][1].strip() == 'True':
                    # No han mandado confirmacion
                    funcionesJugador.seleccionDePersonaje(msg['ID'],
                                                          seleccion,
                                                          players,
                                                          True)
                else:
                    funcionesJugador.seleccionDePersonaje(msg['ID'],
                                                          seleccion,
                                                          players)
                # Actualizamos la data main de info_sesion.csv
                update_data.update_info_jugador()
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                c.DATA_TO_FRONT['characters'] = personajesArray.get()
                emit(c.SERVER_LEVEL,
                     json.dumps(c.DATA_TO_FRONT, indent=4),
                     broadcast=True)
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                app.logger.info({'userSeleccion': {'ID': msg['ID']}})
            else:
                raise SocketIOEventos({
                    msg['ID']: 'Faltan atributos'
                })
        else:
            raise SocketIOEventos({
                'userSeleccion': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/actividades')
def momentos_retos_confirmaciones(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['type']) >= 0:
            # No nos importa cuantas veces lo llamen aqui ponemos
            # un append para el json y en back lo revizamos todo el tiempo
            # revizando que corresponda con el numero de
            # participantes por sesion
            handle_json.add_confirmaciones_automatic(nivel_name=msg['name'],
                                                     mode=msg['type'])
            try:
                # Con msg['respuesta'] levantamos la excepcion
                print(msg['respuesta'])
                handle_json.add_respuestas(nivel_name=msg['name'],
                                           respuestas=msg['respuesta'],
                                           mode=msg['type'])
            except KeyError:
                '''El valor ['respueta'] no esta presente en el JSON'''
                pass

            if c.THREADS_CRONOMETRO:
                # Revizamos que no este corriendo el Thread
                print('<<<<<<<<<<<<<<<<< ',
                      'Wait Event is running', ' >>>>>>>>>')
            else:
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                _waitMoments_ = threading.Thread(target=copy_current_request_context(waitMoments.wait_momentos_retos), # noqa
                                                 args=(msg['name'],
                                                       msg['type']))
                _waitMoments_.start()
                # GLOBAL
                c.THREADS_CRONOMETRO = _waitMoments_.is_alive()

        else:
            raise SocketIOEventos({
                'Response': 'no enviaste nada'
                })
    except TypeError:
        return


@socketio.on('/nivel/cambiar')
def adelante_atras(jsonMsg):
    try:
        msg = json.loads(jsonMsg)

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',
            'Estamos en nivel cambiar',
            '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',
            c.THREADS_CRONOMETRO,
            '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',
            msg)

        # NOTA [Importante, hay que cambiar el nivel4 por otro
        # en el caso que se mueva el orde]
        if len(msg['type']) >= 0 and msg['name'] != 'nivel4':
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            handle_json.add_confirmaciones_automatic(nivel_name=msg['name'], # noqa
                                                     mode=msg['type'])

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            if c.THREADS_CRONOMETRO:
                # Revizamos que no este corriendo el Thread
                print('<<<<<<<<<<<<<<<<< ',
                      'Wait Event is running', ' >>>>>>>>>')
            else:
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                # [Aqui hacemos la logica de comparacion de respuestas
                # y logica de preguntas iguales y asi]
                _waitMoments_ = threading.Thread(target=copy_current_request_context(waitMoments.wait_momentos_retos), # noqa
                                                 args=(msg['name'],
                                                       msg['type'],
                                                       msg['cambioNivel']))
                _waitMoments_.start()
                # GLOBAL
                c.THREADS_CRONOMETRO = _waitMoments_.is_alive()
        else:
            # BUG [el pop up no aparece cuando contestan diferente]
            # [Estamos en un momento especial, el nivel4, que tiene como
            # atributo poder ir de adelante atras]
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>',
                  'Estamos en un momento especial de la App',
                  '<<<<<<<<<<<<<<<<<<<<<<<<<<<<',
                  msg)
            handle_json.add_confirmaciones_automatic(nivel_name=msg['name'],
                                                     mode=msg['type'])
            try:
                # Con msg['respuesta'] levantamos la excepcion
                print(msg['respuesta'])
                handle_json.add_respuestas(nivel_name=msg['name'],
                                           respuestas=msg['respuesta'],
                                           mode=msg['type'])
            except KeyError:
                '''El valor ['respueta'] no esta presente en el JSON'''
                pass

            if c.THREADS_CRONOMETRO:
                # Revizamos que no este corriendo el Thread
                print('<<<<<<<<<<<<<<<<< ',
                      'Wait Event is running', ' >>>>>>>>>')
            else:
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                _waitMoments_ = threading.Thread(target=copy_current_request_context(waitMoments.wait_momentos_retos), # noqa
                                                 args=(msg['name'],
                                                       msg['type'],
                                                       msg['cambioNivel']))
                _waitMoments_.start()
                # GLOBAL
                c.THREADS_CRONOMETRO = _waitMoments_.is_alive()

    except TypeError:
        return
    return


@socketio.on('/sesion/exit')
def nivel_final(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['type']) >= 0:
            ''' Aqui ejecutamos la funcion '''
            _cronometro_ = threading.Thread(target=cronometro.temporizador,
                                            args=(c.TIME_SECONDS,
                                                  work_queue))
            handle_json.add_confirmaciones_automatic(nivel_name=msg['name'],
                                                     mode=msg['type'])
            # GLOBAL
            if c.THREADS_CRONOMETRO:
                # Revizamos que no este corriendo el Thread
                print('<<<<<<<<<<<<<<<<< ',
                      'Cronometro is running', ' >>>>>>>>>')
            else:
                _cronometro_.start()
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                _waitMoments_ = threading.Thread(target=copy_current_request_context(waitMoments.wait_exit_sesion), # noqa
                                                 args=(msg['name'],
                                                       msg['type'],))
                # GLOBAL
                c.THREADS_CRONOMETRO = _cronometro_.is_alive()
                _waitMoments_.start()
                print('<<<<<<<<<<<<<<<<< ',
                      'Start Cronometro / Wait Moments: ',
                      c.THREADS_CRONOMETRO, ' >>>>>>>>>>>>>')
        else:
            raise SocketIOEventos({
                'userSeleccion': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/popup')
def popUp_confirmacion(jsonMsg):
    # print(flask.request.sid)
    try:
        msg = json.loads(jsonMsg)
        if len(msg['type']) >= 0:
            ''' Aqui ejecutamos la funcion '''

            handle_json.add_confirmaciones_automatic(nivel_name=msg['name'],
                                                     mode=msg['type'])
            # GLOBAL
            if c.THREADS_CRONOMETRO:
                # Revizamos que no este corriendo el Thread
                print('<<<<<<<<<<<<<<<<< ',
                      'Wait Moments is running', ' >>>>>>>>>')
            else:
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                _waitMoments_ = threading.Thread(target=copy_current_request_context(waitMoments.wait_popup), # noqa
                                                 args=(msg['name'],
                                                       msg['type'],))
                # GLOBAL
                _waitMoments_.start()
                c.THREADS_CRONOMETRO = _waitMoments_.is_alive()
                print('<<<<<<<<<<<<<<<<< ',
                      'Wait Moments: ',
                      c.THREADS_CRONOMETRO, ' >>>>>>>>>>>>>')
        else:
            raise SocketIOEventos({
                'userSeleccion': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/player/changeStatus')
def change_player_to_user(jsonMsg):
    """[Funcion en donde cambiamos al player to user
        esto significa que pasara de ser un jugador a un
        usuario nada mas]
    """
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Estas dos funiciones estan de sobra ya que no andamos
            # seteando el array en base a nuestra base de datos, sin
            # embarhgo la dejo en caso de utilizarla en un futuro,
            # ya que todo se esta actualizando a nivel base de datos
            changeTipo.change_to_user(msg['ID'])
            updateModoDeJuego.update()
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            try:
                c.DATA_TO_FRONT['players'].remove(msg['ID'])
            except ValueError:
                # No existe en la lista
                pass
            try:
                c.DATA_TO_FRONT['characters'].remove(msg['ID'])
            except ValueError:
                # No existe en la lista
                pass
            emit(c.SERVER_LEVEL,
                 json.dumps(c.DATA_TO_FRONT, indent=4),
                 broadcast=True)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            app.logger.info({'userUnirme': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userUnirme': 'no recivimos el ID del participante'
                })
    except TypeError:
        return

    return


@socketio.on('/sesion/resetAll')
def resetAll(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            reset.resetSesion()
            emit(c.SERVER_LEVEL,
                 json.dumps(c.DATA_TO_FRONT, indent=4),
                 broadcast=True)
            app.logger.info({'userStart': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userStart': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


def runSocketIO():
    print('Iniciando Socket IO')
    socketio.run(app, port=c.PORT, debug=c.DEBUG_MODE)


if __name__ == '__main__':
    print('Inciando App de Radiografias del Banco de Mexico')
    runSocketIO()
