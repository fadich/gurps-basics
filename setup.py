import os

from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='gurps',
    version='1.1.0',
    keywords=['gurps', 'gurps-basics', 'gurps_basics', ],
    url='https://github.com/fadich/gurps-basics',
    author='Fadi A.',
    author_email='royalfadich@gmail.com',
    description='GURPS utils',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=read('requirements.txt').split(),
    entry_points={
        'console_scripts': [
            'gurps-character-generator=gurps.ui.character_generator:main',
        ]
    },
)
