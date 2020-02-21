from jinja2 import Environment, FileSystemLoader


pelican_ruta = '/home/guivaloz/VirtualEnv/Pelican'
env = Environment(
    loader=FileSystemLoader(f'{pelican_ruta}/scripts/archivista/transparencia/plantillas'),
    trim_blocks=True,
    lstrip_blocks=True,
    )
