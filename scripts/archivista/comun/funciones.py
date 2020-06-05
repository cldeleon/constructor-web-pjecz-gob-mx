import os
import re
import shutil
import unicodedata
from datetime import datetime


def cambiar_acentos(text):
    """ Cambia los caracteres acentuados a caracteres sin acentos """
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return(str(text))

def cambiar_a_ruta_segura(text):
    """ Crea una ruta segura en minúsculas, espacios a guiones y sin caracteres acentuados, pero mantiene diagonales """
    text = cambiar_acentos(text.lower())
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_/-]', '', text)
    return(text)

def cambiar_a_identificador(text):
    """ Crea un identificador en minúsculas, guiones y sin caracteres acentuados """
    text = cambiar_acentos(text.lower())
    text = re.sub('[/]+', '-', text)
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return(text)

def sobreescribir_archivo(destino, contenido):
    """ Sobreescribir un archivo """
    if not os.path.exists(os.path.dirname(destino)):
        os.makedirs(os.path.dirname(destino))
    with open(destino, 'w') as file:
        file.write(contenido)
    return(' Sobreescribir ' + os.path.basename(destino))

def copiar_archivo(archivo_ruta, directorio_ruta):
    """ Copiar un archivo """
    if os.path.exists(archivo_ruta) and os.path.isfile(archivo_ruta) and os.path.exists(directorio_ruta) and os.path.isdir(directorio_ruta):
        nombre = os.path.basename(archivo_ruta)
        shutil.copyfile(archivo_ruta, f'{directorio_ruta}/{nombre}')
        return(f' Copiar {nombre}')
    else:
        return(f' FALLÓ copiar {archivo_ruta}')

def obtener_metadatos_del_nombre(nombre, fecha_hora_por_defecto):
    """ Obtener AAAA-MM-DD HHMM TITULO """
    if len(nombre) >= 15:
        # Si empieza con AAAA-MM-DD HHMM
        posible_tiempo = nombre[:15]
        try:
            dt = datetime.strptime(posible_tiempo, '%Y-%m-%d %H%M')
            fecha_hora = dt.strftime('%Y-%m-%d %H:%M')
            if len(nombre) > 15 and nombre[15:].strip() != '':
                titulo = nombre[15:].strip()
            else:
                titulo = 'Sin título'
        except ValueError:
            posible_fecha = nombre[:10]
            try:
                dt = datetime.strptime(posible_fecha, '%Y-%m-%d')
                fecha_hora = dt.strftime('%Y-%m-%d')
                if len(nombre) > 10 and nombre[10:].strip() != '':
                    titulo = nombre[10:].strip()
                else:
                    titulo = 'Sin título'
            except ValueError:
                titulo = nombre
                fecha_hora = fecha_hora_por_defecto
    elif len(nombre) >= 10:
        # Si empieza con AAAA-MM-DD
        posible_fecha = nombre[:10]
        try:
            dt = datetime.strptime(posible_fecha, '%Y-%m-%d')
            fecha_hora = dt.strftime('%Y-%m-%d') + ' 12:00'
            if len(nombre) > 10 and nombre[10:].strip() != '':
                titulo = nombre[10:].strip()
            else:
                titulo = 'Sin título'
        except ValueError:
            titulo = nombre
            fecha_hora = fecha_hora_por_defecto
    else:
        titulo = nombre
        fecha_hora = fecha_hora_por_defecto
    return(fecha_hora, titulo)
