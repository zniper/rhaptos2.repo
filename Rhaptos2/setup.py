
'''
setup.py for rhaptos2

'''

from distutils.core import setup
import os, glob




#def get_scripts():
#    setupdir = os.path.dirname(os.path.abspath(__file__))
#    files = [os.path.join('scripts', f) for f in  
#             os.listdir(os.path.join(setupdir, 'scripts'))]
#    return files

def main():

    setup(name='Rhaptos2',
          version="0.0.2",
          packages=['rhaptos2'
                    ,'rhaptos2.repo'
                    ,'rhaptos2.libauth'
                    ,'rhaptos2.librhaptos1'
                    ,'rhaptos2.client'
                    ,'rhaptos2.test'
                   ],
          author='See AUTHORS.txt',
          author_email='info@cnx.org',
          url='www.cnx.org',
          license='LICENSE.txt',
          description='New editor / repo / system for cnx.org -rhaptos2.readthedocs.org',
          long_description='see description',
          install_requires=[
              "fabric >= 1.0.0"
              ,"flask >= 0.8"
              ,"statsd"
              ,"requests"
              ,"nose", 'pylint'
                           ],
          scripts=['scripts/rhaptos2_runrepo.py'],

#          #intention here is to get setup to use nose to run setup.py test. 
#          tests_require="nose",
#          test_suite="nose.collector",
          
          )



if __name__ == '__main__':
    main()

