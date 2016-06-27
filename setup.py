# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='mysqlparser',
      version='0.1',
      description='MySQL parser for my.cnf',
      author='Cornelius Kölbel',
      author_email='cornelius.koelbel@netknights.it',
      url='https://github.com/privacyidea/mysqlparser',
      py_modules=['mysqlparser'],
      install_requires = [
          'pyparsing>=2.0'
      ]
)
