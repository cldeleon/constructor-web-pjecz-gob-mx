from setuptools import setup

setup(
    name='Archivista',
    version='0.2',
    py_modules=['archivista'],
    install_requires=[
        'Click',
        'Jinja2',
        'tabulate',
        ],
    entry_points="""
        [console_scripts]
        archivista=archivista:cli
        """,
)
