
'''
setup.py for rhaptos2

'''

from distutils.core import setup
import os, glob




def main():

    setup(name='Rhaptos2',
          version="0.0.2",
          packages=['rhaptos2'
                    ,'rhaptos2.repo'
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
              ,"nose" 
              ,"pylint"
              ,"Flask-OpenID"
              ,"sqlalchemy"
#build issues...
              ,"pysqlite >= 2.6.2"
                           ],
          scripts=['scripts/rhaptos2_runrepo.py'],

          package_data={'rhaptos2.repo': ['templates/*.*', 'static/*.*']},

#          #intention here is to get setup to use nose to run setup.py test. 
#          tests_require="nose",
#          test_suite="nose.collector",
          
          )



if __name__ == '__main__':
    main()

