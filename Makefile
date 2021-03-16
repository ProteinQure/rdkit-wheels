py39:
	docker build \
	    --build-arg PY_MAJOR_MINOR=3.9 \
	    --build-arg PY_VER=cp39-cp39 \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .

py38:
	docker build \
		--build-arg PY_MAJOR_MINOR=3.8 \
		--build-arg PY_VER=cp38-cp38 \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .

py37:
	docker build \
		--build-arg PY_MAJOR_MINOR=3.7 \
		--build-arg PY_VER=cp37-cp37m \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .

py36:
	docker build \
		--build-arg PY_MAJOR_MINOR=3.6 \
		--build-arg PY_VER=cp36-cp36m \
		--build-arg NUMPY_VERSION=1.16.6 \
		--build-arg RDKIT_VERSION=2020_09_5 \
		--build-arg PYPI_PASSWORD \
		-t package-builder .
