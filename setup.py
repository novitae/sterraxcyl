from setuptools import setup, find_packages

description = 'A SOCMINT tool to analyse instagram followers | following of a target, and get informations from it.'

setup(
    name = 'sterra',
    version = '2.2.5',
    description = description,
    long_description = description,
    author = 'novitae',
    url = 'https://github.com/novitae/sterraxcyl',
    license = 'GNU General Public License v3 (GPLv3)',
    classifiers = [
        'Programming Language :: Python :: 3.9',
    ],
    packages = find_packages(),
    install_requires = ['aiohttp', 'argparse', 'datetime', 'openpyxl', 'requests', 'string-color', 'tqdm'],
    entry_points = {'console_scripts': ['sterra = sterra.core:main']}
)
