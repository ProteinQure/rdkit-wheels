py39:
	docker build --build-arg --build-arg PY_RELEASE=3.9.2 --build-arg PY_VER=cp39 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

py38:
	docker build --build-arg --build-arg PY_RELEASE=3.8.8 --build-arg PY_VER=cp38 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

py37:
	docker build --build-arg --build-arg PY_RELEASE=3.7.10 --build-arg PY_VER=cp37 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

py36:
	docker build --build-arg --build-arg PY_RELEASE=3.6.13 --build-arg PY_VER=cp36 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .
