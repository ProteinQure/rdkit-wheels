py39:
	docker build --build-arg FEDORA_VERSION=33 --build-arg PY_API=cp39 --build-arg PY_MIN_VERSION=3.9.0 --build-arg PY_MAX_VERSION=3.10.0 --build-arg RDKIT_VERSION=2020.09.5 --build-arg PYPI_PASSWORD -t package-builder .

py38:
	docker build --build-arg FEDORA_VERSION=32 --build-arg PY_API=cp38 --build-arg PY_MIN_VERSION=3.8.0 --build-arg PY_MAX_VERSION=3.9.0 --build-arg RDKIT_VERSION=2020.09.5 --build-arg PYPI_PASSWORD -t package-builder .
