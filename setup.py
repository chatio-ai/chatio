
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
            'streamer = chatio.cli.streamer:main',
            'tokencnt = chatio.cli.tokencnt:main',
            'loopback = chatio.cli.loopback:main',
            'machiner = chatio.cli.machiner:main',
            'debugger = chatio.cli.debugger:main',
        ],
    },
)
