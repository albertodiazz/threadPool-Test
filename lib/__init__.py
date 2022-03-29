
import threading # noqa
from flask import Flask # noqa
from flask_socketio import SocketIO, emit # noqa
from flask_socketio import disconnect # noqa
from flask import copy_current_request_context # noqa
from flask_cors import CORS # noqa

import json # noqa
import pandas as pd # noqa
import numpy as np # noqa
import queue # noqa
import threading # noqa

# Librarys propias
from lib import config as c # noqa
from lib.usuario  import classJugador as Players # noqa
from lib.usuario import funcionesJugador # noqa
from lib.usuario import update_data # noqa
from lib.utilidades import resetAll # noqa
from lib.usuario import changeTipo # noqa
from lib.usuario import deletUser # noqa
from lib.usuario import numeroJugadores # noqa
from lib.utilidades import handle_json # noqa
from lib.utilidades import waitMoments # noqa
from lib.utilidades import whoLeavesCharacters # noqa
from lib.utilidades import updateModoDeJuego # noqa
from lib.utilidades import eventosJuego # noqa
from lib.utilidades import personajesArray # noqa

# El modulo de cronometro lo estoy corriendo de
# manera paralela con threading en app.py
from lib.utilidades import cronometro # noqa
# El modulo randon lo estoy ocupando en la funcion
# cronometro ya que ahi es donde elijo de forma aleatoria
# una vez que el tiempo se acaba
from lib.usuario import automaticElection # noqa
