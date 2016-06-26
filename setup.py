#!/usr/bin/env python3

from setuptools import setup

setup(name='vagga-docker',
      version='0.1',
      description='A wrapper to run vagga in docker (easier on osx)',
      author='Paul Colomiets',
      author_email='paul@colomiets.name',
      url='http://github.com/tailhook/vagga-docker',
      packages=['vagga_docker'],
      install_requires=[
        'depends',
      ],
      entry_points = {
          'console_scripts': ['vagga=vagga_docker.main:main'],
      }
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      )
