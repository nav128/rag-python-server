# make all sub dires under src a package
from setuptools import setup, find_packages
# install requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    # install the packages with pip on command

    
setup(
    name='rag',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
)