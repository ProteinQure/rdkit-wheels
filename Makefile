py39:
	docker build \
	    --build-arg PY_RELEASE=3.9.2 \
	    --build-arg PY_VER=cp39-cp39 \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .

py38:
	docker build \
		--build-arg PY_RELEASE=3.8.8 \
		--build-arg PY_VER=cp38-cp38 \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .

py37:
	docker build \
		--build-arg PY_RELEASE=3.7.10 \
		--build-arg PY_VER=cp37-cp37m \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .

py36:
	docker build \
		--build-arg PY_RELEASE=3.6.13 \
		--build-arg PY_VER=cp36-cp36m \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .
