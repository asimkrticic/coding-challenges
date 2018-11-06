from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='package-challenge',
    version='0.1.0',
    description='Mobiquity Package Challenge',
    long_description=readme,
    author='Asim Krticic',
    packages=find_packages(exclude=('tests', 'docs'))
)

