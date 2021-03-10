#!/usr/bin/python3
import os
from setuptools import find_packages, setup

# Package name
package_name = "pq_rdkit"

# Specify the dependencies of the package
requirements = ["numpy"]

PY_MIN_VERSION = os.getenv("PY_MIN_VERSION")
PY_MAX_VERSION = os.getenv("PY_MAX_VERSION")
RDKIT_VERSION = os.getenv("RDKIT_VERSION")

# Package setup.
setup(
    name=package_name,
    version=f"{RDKIT_VERSION}",
    python_requires=f">={PY_MIN_VERSION},<{PY_MAX_VERSION}",
    install_requires=requirements,
    long_description=open("README.md").read(),
    author="ProteinQure team",
    author_email="team@proteinqure.com",
    license="BSD-3",
    packages=find_packages(),
    package_data={'rdkit': ['*.so', '*/*.so', '*/*/*.so', '*/*/*/*.so']},
)
