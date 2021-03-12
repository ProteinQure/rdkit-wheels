py39:
	docker build --build-arg FEDORA_VERSION=33 --build-arg PY_VER=cp39 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

py38:
	docker build --build-arg FEDORA_VERSION=32 --build-arg PY_VER=cp38 --build-arg RDKIT_VERSION=2020.9.5 --build-arg PYPI_PASSWORD -t package-builder .

virt:
	pushd virtual; \
	python3 setup.py bdist_wheel; \
	python3 -m twine upload -u pqpypi -p ${PYPI_PASSWORD} --repository-url https://pypi.internal.pq/ dist/*; \
	popd;
