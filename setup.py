import os
from setuptools import setup, find_packages

_readme_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'README.rst',
)
with open(_readme_path, encoding='utf-8') as _readme_file:
    _readme = _readme_file.read()


setup(
    name='cheat-server',
    url='https://github.com/bwhmather/cheat-server',
    version='0.0.1',
    author='Ben Mather',
    author_email='bwhmather@bwhmather.com',
    maintainer='',
    license='BSD',
    description=(
        "Server for hosting games of cheat"
    ),
    long_description=_readme,
    long_description_content_type='text/x-rst',
    classifiers=[
    ],
    install_requires=[
        'aiohttp',
        'validation',
    ],
    packages=find_packages(),
    package_data={
        '': ['*.pyi', 'py.typed'],
    },
    entry_points={
        'console_scripts': [
            'cheat-server=cheat_server:main',
        ],
    },
    test_suite='cheat_server.tests.suite',
)
