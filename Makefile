py39:
	docker build --build-arg FEDORA_VERSION=33 --build-arg PY_VER=cp39 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

py38:
	docker build --build-arg FEDORA_VERSION=32 --build-arg PY_VER=cp38 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

py37:
	docker build --build-arg FEDORA_VERSION=29 --build-arg PY_VER=cp37 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

py36:
	docker build --build-arg FEDORA_VERSION=27 --build-arg PY_VER=cp36 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .
