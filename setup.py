# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = 'v0.3'

long_desc = '''
This package contains the Jupyter Sphinx extension.

.. add description here ..
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-jupyter',
    version=VERSION,
    url='https://github.com/QuantEcon/sphinxcontrib-jupyter',
    download_url='https://github.com/QuantEcon/sphinxcontrib-jupyter/archive/{}.tar.gz'.format(VERSION),
    license='BSD',
    author='QuantEcon',
    author_email='admin@quantecon.org',
    description='Sphinx "Jupyter" extension: Convert your RST files into executable Jupyter notebooks.',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['docutils', 'nbformat', 'sphinx'],
    namespace_packages=['sphinxcontrib'],
)
