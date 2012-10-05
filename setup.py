from setuptools import setup
# from os import path
# here = path.abspath(path.dirname(__file__))

setup(
    name='remoting',
    version='0.0.1',
    author='Christopher Brown',
    author_email='chrisbrown@utexas.edu',
    packages=['remoting'],
    include_package_data=False,
    zip_safe=True,
    install_requires=[
        'redis',
        'pycurl',
    ]
)
