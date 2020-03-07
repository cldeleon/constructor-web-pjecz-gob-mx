import click
import os
import sys
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from transparencia.transparencia import Transparencia

home_path = str(Path.home())
pelican_path = f'{home_path}/VirtualEnv/Pelican'
nextcloud_path = f'{home_path}/Nextcloud/Sitios Web/pjecz.gob.mx'

transparencia_input_path = f'{nextcloud_path}/Transparencia'
transparencia_output_path = f'{home_path}/VirtualEnv/Pelican/guivaloz-pjecz.gob.mx/content/transparencia'
transparencia_plantillas_path = f'{pelican_path}/scripts/archivista/transparencia/plantillas'
transparencia_metadatos_csv = f'{pelican_path}/scripts/archivista/transparencia/transparencia.csv'

def actualizar_archivo(ruta, contenido):
    if not os.path.exists(os.path.dirname(ruta)):
        os.makedirs(os.path.dirname(ruta))
    with open(ruta, 'w') as file:
        file.write(contenido)

def sobreescribir_archivo(ruta, contenido):
    if not os.path.exists(os.path.dirname(ruta)):
        os.makedirs(os.path.dirname(ruta))
    with open(ruta, 'w') as file:
        file.write(contenido)


class Config(object):

    def __init__(self):
        self.metadatos = ''


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--input-path', default=transparencia_input_path, type=str, help='Ruta a Nextcloud con insumos.')
@click.option('--output-path', default=transparencia_output_path, type=str, help='Ruta a Pelican de contenidos.')
@click.option('--metadatos-csv', default=transparencia_metadatos_csv, type=str, help='Archivo CSV con metadatos')
@pass_config
def cli(config, input_path, output_path, metadatos_csv):
    click.echo('Hola, ¡soy Archivista!')
    config.input_path = input_path
    config.output_path = output_path
    config.metadatos_csv = metadatos_csv
    if not os.path.exists(config.input_path):
        sys.exit('Error: No existe la ruta a Nextcloud.')
    click.echo(f'  Ruta a Nextcloud con insumos: {config.input_path}')
    if not os.path.exists(config.output_path):
        sys.exit('Error: No existe la ruta a contenidos de Pelican.')
    click.echo(f'  Ruta a Pelican de contenidos: {config.output_path}')
    if not os.path.exists(config.metadatos_csv):
        sys.exit('Error: No existe el archivo CSV con los metadatos.')
    click.echo(f'  Archivo CSV con metadatos:    {config.metadatos_csv}')
    if not os.path.exists(transparencia_plantillas_path):
        sys.exit('Error: No existe la ruta a las plantillas.')
    click.echo(f'  Ruta a las plantillas:        {transparencia_plantillas_path}')
    config.plantillas_env = Environment(
        loader=FileSystemLoader(transparencia_plantillas_path),
        trim_blocks=True,
        lstrip_blocks=True,
        )

@cli.command()
@pass_config
def mostrar(config):
    """ Mostrar en pantalla directorios y archivos que puede crear """
    click.echo('Voy a mostrar...')
    transparencia = Transparencia(
        input_path=config.input_path,
        output_path='',
        metadatos_csv=config.metadatos_csv,
        plantillas_env=config.plantillas_env,
        )
    click.echo(transparencia)

@cli.command()
@pass_config
def crear(config):
    """ Crear directorios y archivos """
    click.echo('Voy a crear...')

@cli.command()
@pass_config
def actualizar(config):
    """ Actualizar los contenidos con los archivos descargables """
    click.echo('Voya a actualizar...')

cli.add_command(mostrar)
cli.add_command(crear)
cli.add_command(actualizar)
