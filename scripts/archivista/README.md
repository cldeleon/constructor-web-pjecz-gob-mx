
# Archivista

Instalar

    $ cd scripts/archivista/
    $ pip install --editable .

Ejecutar

    $ archivista
    Usage: archivista [OPTIONS] COMMAND [ARGS]...

    Options:
      --insumos-ruta TEXT   Ruta a los insumos en Nextcloud.
      --salida-ruta TEXT    Ruta de salida a Pelican.
      --metadatos-csv TEXT  Archivo CSV con metadatos
      --help                Show this message and exit.

    Commands:
      actualizar  Actualizar directorios y archivos
      crear       Crear directorios y archivos
      mostrar     Mostrar en pantalla directorios y archivos que puede crear
