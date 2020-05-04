import click
import os
import sys
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from transparencia.transparencia import Transparencia
from transparenciatca.transparenciatca import TransparenciaTCA
from universal.universal import Universal

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
    # Definir variables
    config.salida_ruta = f'{home_ruta}/VirtualEnv/Pelican/pjecz.gob.mx/content'
    if config.rama == 'Conócenos' or config.rama == 'Sesiones':
        config.metadatos_csv = f'{pelican_ruta}/scripts/archivista/universal/universal.csv'
        plantillas_ruta = f'{pelican_ruta}/scripts/archivista/universal/plantillas'
    elif config.rama == 'Transparencia':
        config.metadatos_csv = f'{pelican_ruta}/scripts/archivista/transparencia/transparencia.csv'
        plantillas_ruta = f'{pelican_ruta}/scripts/archivista/transparencia/plantillas'
    elif config.rama == 'Transparencia TCA':
        config.metadatos_csv = f'{pelican_ruta}/scripts/archivista/transparenciatca/transparenciatca.csv'
        plantillas_ruta = f'{pelican_ruta}/scripts/archivista/transparenciatca/plantillas'
    else:
        sys.exit('Error: La rama no está programada.')
    # Definir insumos ruta
    config.insumos_ruta = f'{nextcloud_ruta}/{config.rama}'
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
    # Definir el entorno Jinja2 a la ruta con las plantillas
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
        conocenos = Universal(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            titulo = 'Conócenos',
            resumen = '.',
            etiquetas = 'Conócenos',
            creado = '2020-05-04 09:12',
            modificado = '2020-05-04 09:12',
            )
        click.echo(conocenos)
    elif config.rama == 'Sesiones':
        sesiones = Universal(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            titulo = 'Sesiones',
            resumen = '.',
            etiquetas = 'Sesiones',
            creado = '2020-05-04 09:12',
            modificado = '2020-05-04 09:12',
            )
        click.echo(sesiones)
    elif config.rama == 'Transparencia':
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
        sys.exit('Error: La rama no está programada.')

@cli.command()
@pass_config
def crear(config):
    """ Crear directorios y archivos """
    click.echo('Voy a crear...')
    if config.rama == 'Conócenos':
        conocenos = Universal(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            titulo = 'Conócenos',
            resumen = '.',
            etiquetas = 'Conócenos',
            creado = '2020-05-04 09:12',
            modificado = '2020-05-04 09:12',
            )
        sobreescribir_archivo(f'{conocenos.destino_md_ruta}', conocenos.contenido())
        click.echo(f'  {conocenos.destino_md_ruta}')
        for rama in conocenos.ramas:
            sobreescribir_archivo(rama.destino_md_ruta, rama.contenido())
            click.echo(f'  {rama.destino_md_ruta}')
    elif config.rama == 'Sesiones':
        sesiones = Universal(
            insumos_ruta=config.insumos_ruta,
            salida_ruta=config.salida_ruta,
            metadatos_csv=config.metadatos_csv,
            plantillas_env=config.plantillas_env,
            titulo = 'Sesiones',
            resumen = '.',
            etiquetas = 'Sesiones',
            creado = '2020-05-04 09:12',
            modificado = '2020-05-04 09:12',
            )
        sobreescribir_archivo(f'{sesiones.destino_md_ruta}', sesiones.contenido())
        click.echo(f'  {sesiones.destino_md_ruta}')
        for rama in sesiones.ramas:
            sobreescribir_archivo(rama.destino_md_ruta, rama.contenido())
            click.echo(f'  {rama.destino_md_ruta}')
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
