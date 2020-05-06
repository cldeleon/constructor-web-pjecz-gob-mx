# Archivista

El objetivo de este programa es tomar los insumos desde Nextcloud para crear los contenidos para Pelican. Así se pueden crear en Nextcloud los directorios con archivos para descargar, poner las imágenes y los contenidos markdown para Pelican.

Instalar

    $ cd scripts/archivista/
    $ pip install --editable .

Obtenga la ayuda con --help

    $ archivista --help
    Usage: archivista [OPTIONS] COMMAND [ARGS]...

    Options:
      --rama TEXT  Conócenos, Sesiones, Transparencia o Transparencia TCA
      --help       Show this message and exit.

    Commands:
      crear    Crear directorios y archivos
      mostrar  Mostrar en pantalla directorios y archivos que puede crear

Para mostrar una rama

    $ archivista --rama Sesiones mostrar

Para crear los contenidos para Pelican

    $ archivista --rama Sesiones crear
