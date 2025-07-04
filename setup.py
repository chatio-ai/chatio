#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="chatio",
    version="0.0.5",
    author="Roman Valov",
    author_email="roman.valov@gmail.com",
    description="LLM API",
    url="https://github.com/kurultai-dev/chatio",
    license="",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[],
)
