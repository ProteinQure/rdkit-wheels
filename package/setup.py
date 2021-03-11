#!/usr/bin/python3
import os
from setuptools import find_packages, setup

PY_API = os.getenv("PY_API")
PY_MIN_VERSION = os.getenv("PY_MIN_VERSION")
PY_MAX_VERSION = os.getenv("PY_MAX_VERSION")
RDKIT_VERSION = os.getenv("RDKIT_VERSION")

# Package name
package_name = f"pq_rdkit_{PY_API}"

# Specify the dependencies of the package
requirements = ["numpy"]

# Package setup.
setup(
    name=package_name,
    version=f"{RDKIT_VERSION}",
    python_requires=f">={PY_MIN_VERSION}",
    install_requires=requirements,
    long_description=open("README.md").read(),
    author="ProteinQure team",
    author_email="team@proteinqure.com",
    license="BSD-3",
    packages=find_packages(),
    package_data={'rdkit': ['*.so', '*/*.so', '*/*/*.so', '*/*/*/*.so']},
)
