#!/usr/bin/python3
# xlnodeid_py/setup.py

""" Setuptools project configuration for xlnodeid_py. """

from os.path import exists
from setuptools import setup

LONG_DESC = None
if exists('README.md'):
    with open('README.md', 'r') as file:
        LONG_DESC = file.read()

setup(name='xlnodeid_py',
      version='0.0.11',
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      LONG_DESCription=LONG_DESC,
      packages=['xlnodeid'],
      package_dir={'': 'src'},
      py_modules=[],
      include_package_data=False,
      zip_safe=False,
      scripts=[],
      ext_modules=[],
      description='nodeid layer for xlattice_py',
      url='https://jddixon.github.io/xlnodeid_py',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 2.7',
          'Programming Language :: Python 3.5',
          'Programming Language :: Python 3.6',
          'Programming Language :: Python 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
