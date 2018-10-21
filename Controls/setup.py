from setuptools import setup

setup(
    name='Controlpi',
    url='https://github.com/jladan/package_demo',
    author='John Ladan',
    author_email='jladan@uwaterloo.ca',
    # Needed to actually package something
    packages=['controlspi'],
    # Needed for dependencies
    install_requires=['pymongo'],
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Python package which needs to be installed on Raspberry Pi to be able to control it with Flaskberry',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
