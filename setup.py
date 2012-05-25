
'''
setup.py for frozone

'''

from distutils.core import setup
setup(name='frozone',
      version='0.0.1',
      packages=['frozone',
                'frozone.deploy',
                'frozone.e2repo',
                'frozone.e2server',
                'frozone.libauth'],
      )

