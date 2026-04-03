"""
Wagtail DrawIO setup file

License: MIT
"""

import os
import re
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 10):
    sys.exit("This package requires a version of python 3.10 or above")


def _read_changelog():
    """Return (package_name, version) parsed from changelog.txt without importing the package."""
    changelog_path = os.path.join(
        os.path.dirname(__file__), "wagtail_drawio", "changelog.txt"
    )
    with open(changelog_path, encoding="utf-8") as f:
        first_line = f.readline()
    match = re.compile(r"([^ ]+) \(([^\)]+)\) .*").match(first_line)
    if not match:
        raise RuntimeError(f"Cannot parse version from changelog: {first_line!r}")
    name = match[1].replace("-", "_")
    version = match[2]
    return name, version


# Read info from the repo instead of hard-coding them in the setup.py:

with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    README = readme.read()

with open(
    os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8"
) as requirements:
    REQUIREMENTS = [
        r for r in requirements.read().splitlines() if r and not r.startswith("#")
    ]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

PACKAGE_NAME, VERSION = _read_changelog()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    python_requires=">3.10.0",
    packages=find_packages(exclude=["tests", "tests.*", "webroot", "webroot.*"]),
    include_package_data=True,
    license="MIT",
    long_description_content_type="text/markdown",
    description="Wagtail DrawIO Integration - DrawIO editor for Wagtail CMS.",
    long_description=README,
    url="https://github.com/goutnet/wagtail-drawio",
    author="Florian Delizy",
    author_email="florian.delizy@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Web Designers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=REQUIREMENTS,
)
