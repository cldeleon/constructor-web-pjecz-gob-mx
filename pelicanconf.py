#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Tema
#THEME = 'themes/startbootstrap-business-frontpage'
THEME = 'themes/pjecz-2020-04'

# Para desarrollo, los vinculos son relativos
SITEURL = ''
RELATIVE_URLS = True

# Metadatos de todo el sitio web
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
    'acuerdos',
    'comunicados',
    'sesiones',
    ]

# Directorios que tienen páginas fijas, no artículos
PAGE_PATHS = [
    'aviso-de-privacidad',
    'conocenos',
    'consejo-judicatura',
    'consultas',
    'licencias',
    'poder-judicial',
    'politicas-de-uso',
    'tramites-servicios',
    'transparencia',
    'transparencia-tca',
    'votos-particulares',
    ]

# Directorios y archivos que son fijos
# Agregue también los directorios que tienen archivos para artículos y páginas
STATIC_PATHS = [
    'acuerdos',
    'comunicados',
    'conocenos',
    'consejo-judicatura',
    'consultas',
    'poder-judicial',
    'sesiones',
    'tramites-servicios',
    'transparencia',
    'transparencia-tca',
    'CNAME',
    'favicon.ico',
    'robots.txt',
    ]

# NO usar el directorio como la categoria
USE_FOLDER_AS_CATEGORY = False

# Los artículos van en directorios por /categoria/YYYY/slug/
ARTICLE_URL = '{category}/{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{slug}/index.html'

# En cada pagina debe haber metadatos url y save_as
# por lo que no necesitamos esto
#PAGE_URL = 'directorio/directorio/'
#PAGE_SAVE_AS = 'directorio/directorio/index.html'

# Lenguaje y zona horaria
DEFAULT_LANG = 'es'
TIMEZONE = 'America/Monterrey'

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

# NO BORRAR de output los siguientes directorios y archivos
OUTPUT_RETENTION = ['.git', '.gitignore']

# Paginacion
#DEFAULT_PAGINATION = False
DEFAULT_PAGINATION = True
DEFAULT_PAGINATION = 8
DEFAULT_ORPHANS = 2

# Para desarrollo BORRAR todo el directorio de salida
DELETE_OUTPUT_DIRECTORY = True

# Para desarrollo DESACTIVAR el caché
LOAD_CONTENT_CACHE = False

# Para desarrollo NO hay cargas desde Internet
USE_REMOTE_SERVICES = False
