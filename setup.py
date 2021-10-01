from setuptools import setup, find_packages

setup(
    name = 'sterraxcyl',
    version = '1.2.0',
    description = 'OSINT tool to export followers and/or following details of an instagram account to an excel table',
    long_description = 'OSINT tool to export followers and/or following details of an instagram account to an excel table, see README of https://github.com/novitae/sterraxcyl',
    author = 'novitae',
    url = 'https://github.com/novitae/sterraxcyl',
    licence = 'GNU General Public License v3 (GPLv3)',
    classifiers = [
        'Programming Language :: Python :: 3.9',
    ],
    packages = find_packages(),
    install_requires = ['argparse', 'datetime', 'instaloader', 'openpyxl', 'requests', 'string-color', 'tqdm'],
    entry_points = {'console_scripts': ['sterra = sterraxcyl.core:main', 'sterraxcyl = sterraxcyl.core:main',]}
)