from distutils.core import setup
import py2exe
import os
import sys

setup(name='shelltag',
    version='0.01',
    description='ID3 tagger for a shell',
    author='David Hwang',
    author_email='d.hw4ng@gmail.com',
    url='http://code.google.com/p/shelltag/',
    packages=['shelltag_src']
    )

