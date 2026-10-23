
from setuptools import setup

setup(
    name='tratamiento_datasets',
    version='0.0.1',
    author='Jon Lorenzo Insausti',
    description='Funciones para la gestion y tratamiento estadistico de los datasets',
    packages=['gestion_datasets'],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib'
    ]
)
