from setuptools import setup, find_packages
import glob
import os

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

# Note: the _program variable is set in __init__.py.
# it determines the name of the package/final command line tool.
from cli import __version__, _program

setup(name='dahak_taco',
      version=__version__,
      packages=['cli'],
      test_suite='nose.collector',
      tests_require=['nose'],
      description='dahak taco, a command line interface for running dahak workflows',
      url='https://dahak-metagenomics.github.io/dahak-taco',
      author='DIB Lab',
      author_email='cmreid@ucdavis.edu',
      license='BSD-3-Clause',
      entry_points="""
      [console_scripts]
      {program} = cli.command:main
      """.format(program = _program),
      install_requires=required,
      keywords=[],
      zip_safe=False)

