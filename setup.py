import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


setup(name='stats_ptech_master',
      version='0.0.1',
      description='statistics distributions percentiles.',
      maintainer='Alfonso R. Reyes',
      maintainer_email='alfonso.r.reyes@gmail.com',
      url='https://github.com/AlfonsoRReyes/stats_ptech_master',
      license='MIT',
      platforms='any',
      packages=['stats_ptech'],
      keywords=['pandas', 'data analysis', 'statistics'],
      install_requires=[
          'numpy',
          'pandas',
          'matplotlib'
      ],
      classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
      ],
      #tests_require=['pytest'],
      #cmdclass={'test': PyTest}
      )
