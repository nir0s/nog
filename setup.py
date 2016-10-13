import os
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='nog',
    version="0.1.0",
    url='https://github.com/nir0s/nog',
    author='nir0s',
    author_email='nir36g@gmail.com',
    license='LICENSE',
    platforms='All',
    description='nog complements git',
    long_description=read('README.rst'),
    packages=['nog'],
    entry_points={'console_scripts': ['nog = nog.nog:main']},
    install_requires=[
        "click==6.6",
        "tinydb==3.2.1",
    ],
    extras_require={},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
