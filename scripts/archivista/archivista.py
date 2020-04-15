import click
import os
import sys
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from transparencia.transparencia import Transparencia

home_ruta = str(Path.home())
pelican_ruta = f'{home_ruta}/VirtualEnv/Pelican/pjecz.gob.mx'
nextcloud_ruta = f'{home_ruta}/Nextcloud/Sitios Web/pjecz.gob.mx'

transparencia_insumos_ruta = f'{nextcloud_ruta}/Transparencia'
transparencia_salida_ruta = f'{home_ruta}/VirtualEnv/Pelican/pjecz.gob.mx/content'
transparencia_metadatos_csv = f'{pelican_ruta}/scripts/archivista/transparencia/transparencia.csv'
transparencia_plantillas_ruta = f'{pelican_ruta}/scripts/archivista/transparencia/plantillas'

def actualizar_archivo(destino, contenido):
    if not os.path.exists(os.path.dirname(destino)):
        os.makedirs(os.path.dirname(destino))
    with open(destino, 'w') as file:
        file.write(contenido)

def sobreescribir_archivo(destino, contenido):
    if not os.path.exists(os.path.dirname(destino)):
        os.makedirs(os.path.dirname(destino))
    with open(destino, 'w') as file:
        file.write(contenido)


class Config(object):

    def __init__(self):
        self.metadatos = ''


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--insumos-ruta', default=transparencia_insumos_ruta, type=str, help='Ruta a los insumos en Nextcloud.')
@click.option('--salida-ruta', default=transparencia_salida_ruta, type=str, help='Ruta de salida a Pelican.')
@click.option('--metadatos-csv', default=transparencia_metadatos_csv, type=str, help='Archivo CSV con metadatos')
@pass_config
def cli(config, insumos_ruta, salida_ruta, metadatos_csv):
    click.echo('Hola, ¡soy Archivista!')
    config.insumos_ruta = insumos_ruta
    config.salida_ruta = salida_ruta
    config.metadatos_csv = metadatos_csv
    if not os.path.exists(config.insumos_ruta):
        sys.exit(f'Error: No existe la ruta a los insumos en Nextcloud {config.insumos_ruta}')
    click.echo(f'  Ruta a Nextcloud con insumos: {config.insumos_ruta}')
    if not os.path.exists(config.salida_ruta):
        sys.exit(f'Error: No existe la ruta de salida a Pelican {config.salida_ruta}')
    click.echo(f'  Ruta a Pelican de contenidos: {config.salida_ruta}')
    if not os.path.exists(config.metadatos_csv):
        sys.exit(f'Error: No existe el archivo CSV con los metadatos {config.metadatos_csv}')
    click.echo(f'  Archivo CSV con metadatos:    {config.metadatos_csv}')
    if not os.path.exists(transparencia_plantillas_ruta):
        sys.exit(f'Error: No existe la ruta a las plantillas {transparencia_plantillas_ruta}')
    click.echo(f'  Ruta a las plantillas:        {transparencia_plantillas_ruta}')
    config.plantillas_env = Environment(
        loader=FileSystemLoader(transparencia_plantillas_ruta),
        trim_blocks=True,
        lstrip_blocks=True,
        )

@cli.command()
@pass_config
def mostrar(config):
    """ Mostrar en pantalla directorios y archivos que puede crear """
    click.echo('Voy a mostrar...')
    transparencia = Transparencia(
        insumos_ruta=config.insumos_ruta,
        salida_ruta='',
        metadatos_csv=config.metadatos_csv,
        plantillas_env=config.plantillas_env,
        )
    click.echo(transparencia)

@cli.command()
@pass_config
def crear(config):
    """ Crear directorios y archivos """
    click.echo('Voy a crear...')
    transparencia = Transparencia(
        insumos_ruta=config.insumos_ruta,
        salida_ruta=config.salida_ruta,
        metadatos_csv=config.metadatos_csv,
        plantillas_env=config.plantillas_env,
        )
    sobreescribir_archivo(f'{config.salida_ruta}/{transparencia.destino}', transparencia.contenido())
    click.echo(f'  {transparencia.destino}')
    for articulo in transparencia.articulos:
        sobreescribir_archivo(f'{config.salida_ruta}/{articulo.destino}', articulo.contenido())
        click.echo(f'  {articulo.destino}')
        for fraccion in articulo.fracciones:
            sobreescribir_archivo(f'{config.salida_ruta}/{fraccion.destino}', fraccion.contenido())
            click.echo(f'  {fraccion.destino}')

@cli.command()
@pass_config
def actualizar(config):
    """ Actualizar directorios y archivos """
    click.echo('Voya a actualizar...')
    transparencia = Transparencia(
        insumos_ruta=config.insumos_ruta,
        salida_ruta=config.salida_ruta,
        metadatos_csv=config.metadatos_csv,
        plantillas_env=config.plantillas_env,
        )
    actualizar_archivo(f'{config.salida_ruta}/{transparencia.destino}', transparencia.contenido())
    click.echo(f'  {transparencia.destino}')
    for articulo in transparencia.articulos:
        actualizar_archivo(f'{config.salida_ruta}/{articulo.destino}', articulo.contenido())
        click.echo(f'  {articulo.destino}')
        for fraccion in articulo.fracciones:
            actualizar_archivo(f'{config.salida_ruta}/{fraccion.destino}', fraccion.contenido())
            click.echo(f'  {fraccion.destino}')

cli.add_command(mostrar)
cli.add_command(crear)
cli.add_command(actualizar)
