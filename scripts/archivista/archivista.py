import click
import os
from transparencia.transparencia import Transparencia


pelican_ruta = '/home/guivaloz/VirtualEnv/Pelican'
entrada_csv = f'{pelican_ruta}/scripts/archivista/transparencia/transparencia.csv'

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
        self.entrada = ''


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--entrada', default=entrada_csv, type=str, help='Archivo CSV con insumos')
@pass_config
def cli(config, entrada):
    click.echo('Hola, ¡soy Archivista!')
    config.entrada = entrada

@cli.command()
@pass_config
def mostrar(config):
    """ Mostrar en pantalla directorios y archivos que puede crear """
    transparencia = Transparencia(entrada_csv=config.entrada)
    click.echo(transparencia)

@cli.command()
@pass_config
def crear(config):
    """ Crear directorios y archivos """
    transparencia = Transparencia(entrada_csv=config.entrada)
    sobreescribir_archivo(transparencia.destino(), transparencia.contenido())
    click.echo(f'Se creó {transparencia.destino()}')
    for articulo in transparencia.articulos:
        sobreescribir_archivo(articulo.destino(), articulo.contenido())
        click.echo(f'Se creó {articulo.destino()}')
        for fraccion in articulo.fracciones:
            sobreescribir_archivo(fraccion.destino(), fraccion.contenido())
            click.echo(f'Se creó {fraccion.destino()}')

@cli.command()
@pass_config
def actualizar(config):
    """ Actualizar los contenidos con los archivos descargables """
    transparencia = Transparencia(entrada_csv=config.entrada)
    actualizar_archivo(transparencia.destino(), transparencia.contenido())
    click.echo(f'Se actualizó {transparencia.destino()}')
    for articulo in transparencia.articulos:
        actualizar_archivo(articulo.destino(), articulo.contenido())
        click.echo(f'Se actualizó {articulo.destino()}')
        for fraccion in articulo.fracciones:
            actualizar_archivo(fraccion.destino(), fraccion.contenido())
            click.echo(f'Se actualizó {fraccion.destino()}')

cli.add_command(mostrar)
cli.add_command(crear)
cli.add_command(actualizar)
