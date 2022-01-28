#!/usr/bin/env python
import os
import re

from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'aspider/__init__.py')) as fp:
    try:
        version = re.findall(
            r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='aspider',
    version=version,
    author='Xiaobo Shang',
    description="A lightweight,asynchronous, distributed scraping micro-framework",
    long_description=read('README.md'),
    author_email='huashanqitu@gmail.com',
    install_requires=['aiofiles', 'aiohttp', 'cchardet', 'cssselect', 'lxml', 'pyppeteer'],
    url="https://github.com/howie6879/aspider/blob/master/README.md",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Documentation': 'https://github.com/howie6879/aspider',
        'Source': 'https://github.com/howie6879/aspider',
    },
    package_data={'aspider': ['utils/*.txt']},
    extras_require={
        'uvloop': ['uvloop']
    }
)