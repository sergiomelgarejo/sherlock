from datetime import datetime
import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from pathlib import Path
import json
import sys


global CFILE
CFILE = Path(__file__).parent / 'config.json'

def parametros_config(parametro):
    """
    Retorna uno o más parámetros del archivo de configuración JSON.
    :param parametro: parametro del diccionario JSON.
    :param parametros: (Opcional) parametros del diccionario JSON.
    :return config_params: parametro(s) parseado(s) del archivo config.
    """   
    with open(CFILE) as connect_config_file:
        config_file = json.load(connect_config_file)
        
        if type(parametro) == list:
            config_params = []
            for param_index in parametro:
                param = config_file[param_index]
                config_params.append(param)
        else:
            config_params = config_file[parametro] 

        return config_params

def fast_connect():
    """Lee archivo de configuración json y crea una cadena de conexion
    @param configfile: path de archivo de configuración
    @type configfile: str
    """
    try:
        with open(CFILE) as connect_config_file:
            config_file = json.load(connect_config_file)

            server = config_file['server']
            uid = config_file['uid']
            pwd = config_file['pwd']
        #Arma cadena de conexión e intena conectarse
        if sys.platform == "win32":
            string = 'Driver={SQL Server};Server=%s;Database=STG;UID=%s;PWD=%s;' % (server, uid, pwd)
        elif sys.platform == "linux":
            # ****produccion***** 
            # string = 'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};Server=%s;Database=STG;UID=%s;PWD=%s;' % (server, uid, pwd)
            # ****desarrollo***** 
            string = 'Driver={/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.0.so.1.1};Server=%s;Database=STG;UID=%s;PWD=%s;TrustServerCertificate=yes;' % (server, uid, pwd)
        else:
            print("No hay compatibilidad con MacOS")

        return string
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f'Error al intentar conectar a la base de datos: {sqlstate}')
        raise Exception(sqlstate)

def db_connect():
    """
    Crea una instancia engine de SQLAlchemy para ejecutar comandos o consultas SQL.
    """
    connection_string = fast_connect()
    conn = urllib.parse.quote_plus(connection_string) 
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn}")

    return engine

def truncate(object_name, log_platform, object='table'):
    try:
        engine = db_connect()
        engine.execute(sa_text(f'truncate {object} {object_name};').execution_options(autocommit=True))
    except Exception as e:
        msg = f"Error al intentar truncar'{object_name}'. {e}"
        print(msg)
        raise Exception(msg)