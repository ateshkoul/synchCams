#from setuptools import setup
from distutils.core import setup

setup(
    name='synchCams',
    version='0.1',
    license='MIT',
    author="Atesh Koul",
    author_email='atesh.koul@gmail.com',
    packages=['synchCams'],
    url = 'https://github.com/ateshkoul/SynchCams',   # Provide either the link to your github or to your website  
    download_url = 'https://github.com/ateshkoul/SynchCams/archive/v_01.tar.gz',    # I explain this later on
    keywords=['synch cams','dual','cams'],
    install_requires=[
          'opencv',
          'opencv-contrib-python',
          'pyserial',
          ''
      ],

)