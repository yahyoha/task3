from setuptools import setup, find_packages

setup(
    name='cloudbillingtool',
    version='1.4',
    python_requires='>=3.6',
    packages=find_packages(exclude=('tests', 'docs'))
)