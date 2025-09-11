#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(
    name='realtime_graph_udp',
    description='Lightweight real time graphing',
    version='0.0.1',
    author="Mohcine Qbaich",
    author_email='randeomcom@gmail.com',
    url='https://github.com/moqba/realtime-graph-udp',
    packages=find_packages(include=['realtime_graph_udp', 'realtime_graph_udp.*']),
    install_requires=['PyQt6', 'numpy', 'pyqtgraph'],
    extra_require={
        'dev': ['pytest'],
        'test': ['pytest']
    },
    python_requires='>=3.11',
)