# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = 'v0.5.6'

LONG_DESCRIPTION = """
This package contains a `Sphinx <http://www.sphinx-doc.org/en/master/>`_ extension 
for compiling RST to Jupyter notebooks. 

It contains two primary builders:

1. jupyter
2. jupyterpdf

The default behaviour of the `jupyter` builder is to provide notebooks that are readable 
with an emphasis on adding markdown into the notebooks. However, it can also be configured
to generate websites (such as `python.quantecon.org <https://python.quantcon.org>`_) 
and run coverage tests, which uses `ipynb` as an intermediate format. 

The `jupyterpdf` builder is focused on building `pdf` files (via an intermediate ipynb format).

This project is maintained and supported by `QuantEcon <http://quantecon.org/>`_.


Status
------

|status-docs| |status-travis|

.. |status-docs| image:: https://readthedocs.org/projects/sphinxcontrib-jupyter/badge/?version=latest
   :target: http://sphinxcontrib-jupyter.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |status-travis| image:: https://travis-ci.org/QuantEcon/sphinxcontrib-jupyter.svg?branch=master
   :target: https://travis-ci.org/QuantEcon/sphinxcontrib-jupyter

"""

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
    long_description=LONG_DESCRIPTION,
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
    install_requires=['docutils', 'nbformat', 'sphinx', 'dask', 'distributed', 'ipython', 'nbconvert', 'jupyter_client'],
    namespace_packages=['sphinxcontrib'],
)
