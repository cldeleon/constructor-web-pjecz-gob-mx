import click
import os
import sys
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from comun.funciones import copiar_archivo, sobreescribir_archivo
from comun.metadatos import Metadatos
from transparencia.transparencia import Transparencia
from transparenciatca.transparenciatca import TransparenciaTCA
from universal.universal import Universal


class Config(object):

    def __init__(self):
        self.home_ruta = str(Path.home())
        self.pelican_ruta = f'{self.home_ruta}/VirtualEnv/Pelican/pjecz.gob.mx'
        self.nextcloud_ruta = f'{self.home_ruta}/Nextcloud/Sitios Web/pjecz.gob.mx'
        self.rama = ''
        self.salida_ruta = f'{self.home_ruta}/VirtualEnv/Pelican/pjecz.gob.mx/content'
        self.metadatos_csv = ''
        self.metadatos = None
        self.insumos_ruta = ''
        self.plantillas_env = None
        self.creado = '2020-05-04 09:12'
        self.modificado = '2020-05-04 09:12'


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--rama', default='Transparencia', type=str, help='Acuerdos, Comunicados, Conócenos, Sesiones, Trámites y Servicios, Transparencia o Transparencia TCA')
@pass_config
def cli(config, rama):
    click.echo('Hola, ¡soy Archivista!')
    # Definir rama
    config.rama = rama
    # Definir insumos_ruta
    config.insumos_ruta = f'{config.nextcloud_ruta}/{config.rama}'
    # Definir metadatos_csv y plantillas_ruta
    if config.rama == 'Acuerdos':
        config.metadatos_csv = f'{config.pelican_ruta}/scripts/archivista/acuerdos/metadatos.csv'
        plantillas_ruta = f'{config.pelican_ruta}/scripts/archivista/acuerdos/plantillas'
    elif config.rama == 'Comunicados':
        config.metadatos_csv = f'{config.pelican_ruta}/scripts/archivista/comunicados/metadatos.csv'
        plantillas_ruta = f'{config.pelican_ruta}/scripts/archivista/comunicados/plantillas'
    elif config.rama == 'Conócenos':
        config.metadatos_csv = f'{config.pelican_ruta}/scripts/archivista/conocenos/metadatos.csv'
        plantillas_ruta = f'{config.pelican_ruta}/scripts/archivista/conocenos/plantillas'
    elif config.rama == 'Sesiones':
        config.metadatos_csv = f'{config.pelican_ruta}/scripts/archivista/sesiones/metadatos.csv'
        plantillas_ruta = f'{config.pelican_ruta}/scripts/archivista/sesiones/plantillas'
    elif config.rama == 'Trámites y Servicios':
        config.metadatos_csv = f'{config.pelican_ruta}/scripts/archivista/tramites-servicios/metadatos.csv'
        plantillas_ruta = f'{config.pelican_ruta}/scripts/archivista/tramites-servicios/plantillas'
    elif config.rama == 'Transparencia':
        config.metadatos_csv = f'{config.pelican_ruta}/scripts/archivista/transparencia/transparencia.csv'
        plantillas_ruta = f'{config.pelican_ruta}/scripts/archivista/transparencia/plantillas'
    elif config.rama == 'Transparencia TCA':
        config.metadatos_csv = f'{config.pelican_ruta}/scripts/archivista/transparenciatca/transparenciatca.csv'
        plantillas_ruta = f'{config.pelican_ruta}/scripts/archivista/transparenciatca/plantillas'
    else:
        sys.exit('Error: La rama no está programada.')
    # Verificar que existan
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
    # Cargar metadatos
    if not (config.rama == 'Transparencia' or config.rama == 'Transparencia TCA'):
        config.metadatos = Metadatos(config.metadatos_csv)
        config.metadatos.cargar()
    # Cargar entorno Jinja2 con plantillas_ruta
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
    if config.rama == 'Transparencia':
        transparencia = Transparencia(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(transparencia)
    elif config.rama == 'Transparencia TCA':
        transparenciatca = TransparenciaTCA(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(transparenciatca)
    else:
        universal = Universal(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos=config.metadatos,
            plantillas_env=config.plantillas_env,
            titulo = config.rama,
            resumen = '.',
            etiquetas = config.rama,
            creado = config.creado,
            modificado = config.modificado,
            )
        click.echo(universal)

@cli.command()
@pass_config
def crear(config):
    """ Crear directorios y archivos """
    click.echo('Voy a crear...')
    if config.rama == 'Transparencia':
        transparencia = Transparencia(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(sobreescribir_archivo(f'{config.salida_ruta}/{transparencia.destino}', transparencia.contenido()))
        for articulo in transparencia.articulos:
            click.echo(sobreescribir_archivo(f'{config.salida_ruta}/{articulo.destino}', articulo.contenido()))
            for fraccion in articulo.fracciones:
                click.echo(sobreescribir_archivo(f'{config.salida_ruta}/{fraccion.destino}', fraccion.contenido()))
    elif config.rama == 'Transparencia TCA':
        transparenciatca = TransparenciaTCA(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            )
        click.echo(sobreescribir_archivo(f'{config.salida_ruta}/{transparenciatca.destino}', transparenciatca.contenido()))
        for articulo in transparenciatca.articulos:
            click.echo(sobreescribir_archivo(f'{config.salida_ruta}/{articulo.destino}', articulo.contenido()))
            for fraccion in articulo.fracciones:
                click.echo(sobreescribir_archivo(f'{config.salida_ruta}/{fraccion.destino}', fraccion.contenido()))
    else:
        universal = Universal(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos=config.metadatos,
            plantillas_env=config.plantillas_env,
            titulo = config.rama,
            resumen = '.',
            etiquetas = config.rama,
            creado = config.creado,
            modificado = config.modificado,
            )
        click.echo(sobreescribir_archivo(universal.destino_md_ruta, universal.contenido()))
        for rama in universal.ramas:
            click.echo(sobreescribir_archivo(rama.destino_md_ruta, rama.contenido()))
            for imagen in rama.imagenes:
                click.echo(copiar_archivo(imagen, rama.destino_ruta))

cli.add_command(mostrar)
cli.add_command(crear)
