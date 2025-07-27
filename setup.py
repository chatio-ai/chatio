
from setuptools import setup, find_packages

setup(
    name="chatio",
    version="0.0.5",
    author="Roman Valov",
    author_email="roman.valov@gmail.com",
    description="LLM API",
    url="https://github.com/chatio-ai/chatio",
    license="",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[],
    entry_points={
        'console_scripts': [
            'chatio = chatio.cli.main:main',
            'chatio-tcnt = chatio.cli.tcnt:main',
            'chatio-loop = chatio.cli.loop:main',
            'chatio-pipe = chatio.cli.pipe:main',
            'chatio-test = chatio.cli.test:main',
        ],
    },
)
