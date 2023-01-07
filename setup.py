import time

from setuptools import setup, find_packages

# Get the current time and date
current_time = time.gmtime()

# Format the time and date as a string
build_number = time.strftime("%y%m%H%M%S", current_time)

setup(
    name='cloudbillingtool-{}'.format(build_number),
    version='1.9.6',
    python_requires='>=3.6',
    packages=find_packages(exclude=('tests', 'docs'))
)