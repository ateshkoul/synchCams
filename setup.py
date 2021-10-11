from setuptools import setup
#from distutils.core import setup
import codecs
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
README_FILE = os.path.join(PROJECT_ROOT, "README.md")

def get_long_description():
    with codecs.open(README_FILE, "rt") as buff:
        return buff.read()

if len(set(("test", "easy_install")).intersection(sys.argv)) > 0:
    import setuptools

extra_setuptools_args = {}
setup(
    name='synchCams',
    version='0.1.5',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url = 'https://github.com/ateshkoul/SynchCams',
    license='MIT',
    description = 'A toolbox for synchronized dual camera acquisition',
    author="Atesh Koul",
    author_email='atesh.koul@gmail.com',
    packages=['synchCams'],
    download_url = 'https://github.com/ateshkoul/SynchCams/archive/v_01.tar.gz',    
    keywords=['synch cams','dual','cams'],
    install_requires=[
          'opencv-python',
          'opencv-contrib-python',
          'pyserial',
          ''
      ],
    **extra_setuptools_args,

)