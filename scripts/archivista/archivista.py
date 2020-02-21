import click
import os
from transparencia.transparencia import Transparencia


pelican_ruta = '/home/guivaloz/VirtualEnv/Pelican'
fracciones_csv = f'{pelican_ruta}/scripts/archivista/transparencia/transparencia.csv'

def actualizar_archivo(ruta, contenido):
    if not os.path.exists(os.path.dirname(ruta)):
        os.makedirs(os.path.dirname(ruta))
    with open(ruta, 'w') as file:
        file.write(contenido)
    click.echo(f'- Guardado {ruta}')

def sobreescribir_archivo(ruta, contenido):
    if not os.path.exists(os.path.dirname(ruta)):
        os.makedirs(os.path.dirname(ruta))
    with open(ruta, 'w') as file:
        file.write(contenido)
    click.echo(f'- Guardado {ruta}')

class Config(object):

    def __init__(self):
        self.entrada = ''


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--entrada', default=fracciones_csv, type=str, help='Archivo CSV con insumos')
@pass_config
def cli(config, entrada):
    click.echo('Hola, ¡soy Archivista!')
    config.entrada = entrada

@cli.command()
@pass_config
def mostrar(config):
    transparencia = Transparencia()
    transparencia.alimentar(config.entrada)
    click.echo(transparencia)
    articulo = transparencia.articulos.pop()
    click.echo(articulo)

@cli.command()
@pass_config
def crear(config):
    # Transparencia
    transparencia = Transparencia()
    transparencia.alimentar(config.entrada)
    sobreescribir_archivo(transparencia.destino(), transparencia.contenido())
    click.echo('Se creó transparencia.md')
    # Artículos
    articulo = transparencia.articulos.pop()
    sobreescribir_archivo(articulo.destino(), articulo.contenido())
    click.echo(f'Se creó articulo-21.md')
    # Fracciones
    contador = 0
    for fraccion in articulo.fracciones:
        sobreescribir_archivo(fraccion.destino(), fraccion.contenido())
        contador += 1
    click.echo(f'Se crearon {contador} fracciones.')

@cli.command()
@pass_config
def actualizar(config):
    # Transparencia
    transparencia = Transparencia()
    transparencia.alimentar(config.entrada)
    actualizar_archivo(transparencia.destino(), transparencia.contenido())
    click.echo('Se actualizó transparencia.md')
    # Artículos
    articulo = transparencia.articulos.pop()
    actualizar_archivo(articulo.destino(), articulo.contenido())
    click.echo(f'Se actualizó articulo-21.md')
    # Fracciones
    contador = 0
    for fraccion in articulo.fracciones:
        actualizar_archivo(fraccion.destino(), fraccion.contenido())
        contador += 1
    click.echo(f'Se actualizaron {contador} fracciones.')

cli.add_command(mostrar)
cli.add_command(crear)
cli.add_command(actualizar)
