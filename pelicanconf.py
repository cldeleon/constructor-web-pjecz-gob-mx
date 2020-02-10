#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Tema
THEME = 'themes/startbootstrap-business-frontpage'

# Sitio web
SITEURL = ''
SITENAME = 'Poder Judicial del Estado de Coahuila de Zaragoza'
SITELOGO = 'theme/images/pjecz.png'
SITEDESCRIPTION = 'Sitio web del Poder Judicial del Estado de Coahuila de Zaragoza'
SITETWITTER = '@PJCoah'

# Autor por defecto
AUTHOR = 'PJECZ'

# Directorio donde esta el contenido
PATH = 'content'

# Directorios que tienen los articulos
ARTICLE_PATHS = [
    'boletines-judiciales',
    'comunicados',
    ]

# Directorios que tienen páginas fijas, no artículos
PAGE_PATHS = [
    'transparencia',
    ]

# Directorios y archivos que son fijos
# Agregue también los directorios que tienen archivos para artículos y páginas
STATIC_PATHS = [
    'favicon.ico',
    'robots.txt',
    'comunicados',
    'transparencia',
    ]

# El nombre del directorio es la categoría: comunicados
USE_FOLDER_AS_CATEGORY = False

# Los artículos van en directorios por /categoria/YYYY/slug/
ARTICLE_URL = '{category}/{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{slug}/index.html'

# Las páginas fijas deben definir su URL y Save_As
#PAGE_URL = 'directorio/directorio/'
#PAGE_SAVE_AS = 'directorio/directorio/index.html'

# Lenguaje y zona horaria
DEFAULT_LANG = 'es'
TIMEZONE = 'America/Monterrey'

# Para desarrollo, los vinculos son relativos
RELATIVE_URLS = True

# Para desarrollo, se desactiva la paginacion
DEFAULT_PAGINATION = False

# Para desarrollo, no hay cargas desde Internet
USE_REMOTE_SERVICES = False

# Para desarrollo se desactiva la generacion de feeds
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_RSS = None

# Para desarrollo BORRAR todo el directorio de salida
DELETE_OUTPUT_DIRECTORY = True

# NO BORRAR de output los siguientes directorios y archivos
# OUTPUT_RETENTION = ['.git', '.gitignore']

# Para desarrollo descactivar el caché
LOAD_CONTENT_CACHE = False
