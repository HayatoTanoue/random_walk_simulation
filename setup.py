import sys

from setuptools import setup, find_packages

import random_walk_simulation


setup(
    name='random_walk_simulation',
    version=random_walk_simulation.__version__,
    description='random_walk_simulation functions',
    long_description_content_type="text/markdown",
    long_description=random_walk_simulation.__doc__,
    url='https://github.com/HayatoTanoue/random_walk_simulation',
    license='MIT',

    author=random_walk_simulation.__author__,
    author_email='hayatotanoue7321@gmail.com',

    # include all packages
    packages=find_packages(),

    install_requires=[
        'networkx',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
)