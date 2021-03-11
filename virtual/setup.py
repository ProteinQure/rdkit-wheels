#!/usr/bin/python3
import os
from setuptools import setup

RDKIT_VERSION = os.getenv("RDKIT_VERSION")

# Package name
package_name = "pq_rdkit"

# Specify the dependencies of the package
requirements = [
    "numpy",
    f"pq_rdkit_cp38 == {RDKIT_VERSION}; python_version==\"3.8\"",
    f"pq_rdkit_cp39 == {RDKIT_VERSION}; python_version==\"3.9\"",
]

# Package setup.
setup(
    name=package_name,
    version=f"{RDKIT_VERSION}",
    python_requires=">=3.8.0",
    install_requires=requirements,
    long_description=open("README.md").read(),
    author="ProteinQure team",
    author_email="team@proteinqure.com",
    license="BSD-3",
)
