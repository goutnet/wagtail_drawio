"""
Wagtail DrawIO setup file

License: MIT
"""

import os
import sys

from setuptools import find_packages, setup

import wagtail_drawio

if sys.version_info < (3, 10):
    sys.exit("This package requires a version of python 3.10 or above")


# Read info from the repo instead of hard-coding them in the setup.py:

with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    README = readme.read()

with open(
    os.path.join(os.path.dirname(__file__), "LICENSE"), encoding="utf-8"
) as license:
    LICENSE = license.read()

with open(
    os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8"
) as requirements:
    REQUIREMENTS = requirements.read().splitlines()

with open(
    os.path.join(os.path.dirname(__file__), "wagtail_drawio", "changelog.txt"),
    encoding="utf-8",
) as changelog:
    CHANGELOG = changelog.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

MODULE = wagtail_drawio

setup(
    name=MODULE.package_information()[0],
    version=MODULE.__version__,
    python_requires=">3.10.0",
    packages=find_packages(),
    include_package_data=True,
    license=LICENSE,
    chapter=CHANGELOG,
    description="Wagtail DrawIO Integration - DrawIO editor for Wagtail CMS.",
    long_description=README,
    url="www.github.com/goutnet/wagtail-drawio",
    author="Florian Delizy",
    author_email="florian.delizy@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Web Designers",
        "License :: MIT",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=REQUIREMENTS,
)
