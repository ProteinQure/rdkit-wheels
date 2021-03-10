FROM fedora:33

# Install build dependencies
RUN dnf install -y rpm-build rpmdevtools make gcc-c++ cmake flex bison libpq-devel python3-numpy inchi-devel cairo-devel eigen3-devel chrpath swig java-devel junit python3-devel boost-python3-devel catch-devel
RUN rpmdev-setuptree

ADD assets/rdkit.spec /root/rpmbuild/SPECS/
ADD assets/*.patch /root/rpmbuild/SOURCES/

RUN spectool -g -R /root/rpmbuild/SPECS/rdkit.spec
RUN rpmbuild -bb /root/rpmbuild/SPECS/rdkit.spec

# Install the built packages
RUN ls /root/rpmbuild/RPMS/x86_64/*.rpm | grep -v -P 'debug|devel' | sed -e 's/^/.\//' | xargs dnf install -y

ENV PY_API=cp39
ENV PY_MIN_VERSION=3.9.0
ENV PY_MAX_VERSION=3.10.0
ENV RDKIT_VERSION=2020.09.5

ADD package/ /root/package/
WORKDIR /root/package/
RUN cp -r /usr/lib64/python*/site-packages/rdkit rdkit
RUN python3 -m pip install wheel auditwheel twine
RUN python3 setup.py bdist_wheel --py-limited-api $PY_API
RUN dnf install -y patchelf
RUN auditwheel repair --strip --plat linux_x86_64 dist/pq_rdkit*.whl
RUN rename none $PY_API wheelhouse/*
ARG PYPI_PASSWORD
RUN python3 -m twine upload -u pqpypi -p $PYPI_PASSWORD --repository-url https://pypi.internal.pq/ wheelhouse/*
