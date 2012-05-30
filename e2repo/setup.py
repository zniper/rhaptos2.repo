
'''
setup.py for frozone

*not* using distribute. Life is too short.

'''

from distutils.core import setup
import os, glob

here = os.path.abspath(__name__)

def get_scripts():
    files = [os.path.join('scripts', f) for f in  os.listdir('scripts')]
    return files

def get_www():
    files = [os.path.join('www', f) for f in  os.listdir('www')]
    return files


def get_thirdparty():
    files = [os.path.join('thirdparty', f) for f in  os.listdir('thirdparty')]
    return files



def main():

    setup(name='frozone',
          version='0.0.1',
          packages=['frozone',
                    'frozone.deploy',
                    'frozone.e2repo',
                    'frozone.e2server',
                    'frozone.libauth'],
          author='See AUTHORS.txt',
          author_email='paul@mikadosoftware.com',
          license='LICENSE.txt',
          description='Useful towel-related stuff.',
          long_description=open('README.rst').read(),
          install_requires=[
              "fabric >= 1.0.0",
                           ],

          scripts=get_scripts(),
          data_files=[('www', get_www()),]

          )


if __name__ == '__main__':
    main()

