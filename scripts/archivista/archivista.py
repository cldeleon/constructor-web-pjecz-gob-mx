import click
import os
import sys
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from conocenos.conocenos import Conocenos
from sesiones.sesiones import Sesiones
from transparencia.transparencia import Transparencia
from transparenciatca.transparenciatca import TransparenciaTCA

home_ruta = str(Path.home())
pelican_ruta = f'{home_ruta}/VirtualEnv/Pelican/pjecz.gob.mx'
nextcloud_ruta = f'{home_ruta}/Nextcloud/Sitios Web/pjecz.gob.mx'

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
@click.option('--rama', default='Transparencia', type=str, help='Conócenos, Sesiones, Transparencia o Transparencia TCA')
@pass_config
def cli(config, rama):
    config.rama = rama
    click.echo('Hola, ¡soy Archivista!')
    config.salida_ruta = f'{home_ruta}/VirtualEnv/Pelican/pjecz.gob.mx/content'
    if config.rama == 'Conócenos':
        config.insumos_ruta = f'{nextcloud_ruta}/Conócenos'
        config.metadatos_csv = f'{pelican_ruta}/scripts/archivista/conocenos/conocenos.csv'
        plantillas_ruta = f'{pelican_ruta}/scripts/archivista/conocenos/plantillas'
    elif config.rama == 'Sesiones':
        config.insumos_ruta = f'{nextcloud_ruta}/Sesiones'
        config.metadatos_csv = f'{pelican_ruta}/scripts/archivista/sesiones/sesiones.csv'
        plantillas_ruta = f'{pelican_ruta}/scripts/archivista/sesiones/plantillas'
    elif config.rama == 'Transparencia':
        config.insumos_ruta = f'{nextcloud_ruta}/Transparencia'
        config.metadatos_csv = f'{pelican_ruta}/scripts/archivista/transparencia/transparencia.csv'
        plantillas_ruta = f'{pelican_ruta}/scripts/archivista/transparencia/plantillas'
    elif config.rama == 'Transparencia TCA':
        config.insumos_ruta = f'{nextcloud_ruta}/Transparencia TCA'
        config.metadatos_csv = f'{pelican_ruta}/scripts/archivista/transparenciatca/transparenciatca.csv'
        plantillas_ruta = f'{pelican_ruta}/scripts/archivista/transparenciatca/plantillas'
    else:
        sys.exit('Error: La rama no está programada.')
    if not os.path.exists(config.insumos_ruta):
        sys.exit(f'Error: No existe la ruta a los insumos en Nextcloud {config.insumos_ruta}')
    click.echo(f'  Ruta a Nextcloud con insumos: {config.insumos_ruta}')
    if not os.path.exists(config.salida_ruta):
        sys.exit(f'Error: No existe la ruta de salida a Pelican {config.salida_ruta}')
    click.echo(f'  Ruta a Pelican de contenidos: {config.salida_ruta}')
    if not os.path.exists(config.metadatos_csv):
        sys.exit(f'Error: No existe el archivo CSV con los metadatos {config.metadatos_csv}')
    click.echo(f'  Archivo CSV con metadatos:    {config.metadatos_csv}')
    if not os.path.exists(plantillas_ruta):
        sys.exit(f'Error: No existe la ruta a las plantillas {plantillas_ruta}')
    click.echo(f'  Ruta a las plantillas:        {plantillas_ruta}')
    config.plantillas_env = Environment(
        loader=FileSystemLoader(plantillas_ruta),
        trim_blocks=True,
        lstrip_blocks=True,
        )

@cli.command()
@pass_config
def mostrar(config):
    """ Mostrar en pantalla directorios y archivos que puede crear """
    click.echo('Voy a mostrar...')
    if config.rama == 'Conócenos':
        conocenos = Conocenos(
            insumos_ruta=config.insumos_ruta,
            salida_ruta='',
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(conocenos)
    elif config.rama == 'Sesiones':
        sesiones = Sesiones(
            insumos_ruta=config.insumos_ruta,
            salida_ruta='',
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(sesiones)
    elif config.rama == 'Transparencia':
        transparencia = Transparencia(
            insumos_ruta=config.insumos_ruta,
            salida_ruta='',
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(transparencia)
    elif config.rama == 'Transparencia TCA':
        transparenciatca = TransparenciaTCA(
            insumos_ruta=config.insumos_ruta,
            salida_ruta='',
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(transparenciatca)
    else:
        sys.exit('Error: La rama no está programada.')

@cli.command()
@pass_config
def crear(config):
    """ Crear directorios y archivos """
    click.echo('Voy a crear...')
    if config.rama == 'Conócenos':
        conocenos = Conocenos(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        sobreescribir_archivo(f'{config.salida_ruta}/{conocenos.destino}', conocenos.contenido())
        click.echo(f'  {conocenos.destino}')
        # recursivo ?
    elif config.rama == 'Sesiones':
        sesiones = Sesiones(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        sobreescribir_archivo(f'{config.salida_ruta}/{sesiones.destino}', sesiones.contenido())
        click.echo(f'  {sesiones.destino}')
        for sala in sesiones.salas:
            sobreescribir_archivo(f'{config.salida_ruta}/{sala.destino}', sala.contenido())
            click.echo(f'  {sala.destino}')
            for celebracion in sala.celebraciones:
                sobreescribir_archivo(f'{config.salida_ruta}/{celebracion.destino}', celebracion.contenido())
                click.echo(f'  {celebracion.destino}')
    elif config.rama == 'Transparencia':
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
    elif config.rama == 'Transparencia TCA':
        transparenciatca = TransparenciaTCA(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        sobreescribir_archivo(f'{config.salida_ruta}/{transparenciatca.destino}', transparenciatca.contenido())
        click.echo(f'  {transparenciatca.destino}')
        for articulo in transparenciatca.articulos:
            sobreescribir_archivo(f'{config.salida_ruta}/{articulo.destino}', articulo.contenido())
            click.echo(f'  {articulo.destino}')
            for fraccion in articulo.fracciones:
                sobreescribir_archivo(f'{config.salida_ruta}/{fraccion.destino}', fraccion.contenido())
                click.echo(f'  {fraccion.destino}')
    else:
        sys.exit('Error: La rama no está programada.')

cli.add_command(mostrar)
cli.add_command(crear)
