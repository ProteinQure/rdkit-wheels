FROM quay.io/pypa/manylinux2014_x86_64

# Install build dependencies
RUN yum install -y wget make gcc-c++ cmake flex bison inchi-devel cairo-devel eigen3-devel chrpath boost-devel

RUN wget https://github.com/rdkit/rdkit/archive/Release_2020_09_5.tar.gz && \
    tar xfz Release_2020_09_5.tar.gz && \
    mv rdkit-Release_2020_09_5 /root/build/

RUN wget https://phoenixnap.dl.sourceforge.net/project/boost/boost/1.58.0/boost_1_58_0.tar.gz
RUN tar -xzf boost_1_*
RUN cd boost_1_*; ./bootstrap.sh --prefix=/opt/boost; ./b2 install -j8 --prefix=/opt/boost --with=all

ENV LD_LIBRARY_PATH=/opt/python/cp39-cp39/lib/
WORKDIR /root/build/
ENV CXXFLAGS="-Wl,--as-needed"
RUN cmake -D RDK_INSTALL_INTREE=OFF \
          -D CMAKE_BUILD_TYPE=RelWithDebInfo \
          -D RDK_BUILD_INCHI_SUPPORT:BOOL=ON \
          -D RDK_BUILD_THREADSAFE_SSS:BOOL=ON \
          -D RDK_BUILD_CAIRO_SUPPORT:BOOL=ON \
          -D RDK_BUILD_DESCRIPTORS3D:BOOL=ON \
          -D RDK_BUILD_COORDGEN_SUPPORT:BOOL=OFF \
          -D RDK_BUILD_MOLINTERCHANGE_SUPPORT:BOOL=OFF \
          -D RDK_BUILD_PGSQL:BOOL=OFF \
          -D RDK_PGSQL_STATIC:BOOL=OFF \
          -D RDK_INSTALL_STATIC_LIBS:BOOL=OFF \
          -D RDK_USE_FLEXBISON:BOOL=OFF \
          -D RDK_TEST_MULTITHREADED:BOOL=OFF \
          -D PYTHON_EXECUTABLE:FILEPATH=python`echo $PY_RELEASE | cut -d. -f 1-2` \
          -D RDK_BOOST_PYTHON3_NAME=python`echo $PY_RELEASE | cut -d. -f 1-2 | sed 's/\.//g'` \
          . -B .

RUN make -j8
#make install DESTDIR=%{buildroot}
RUN make install

ARG PY_VER
ARG RDKIT_VERSION

# Install Python tooling + patchelf
RUN python3.9 -m ensurepip
RUN python3.9 -m pip install -U pip
RUN python3.9 -m pip install wheel auditwheel twine
RUN dnf install -y patchelf

# Copy skeleton for the Python package
ADD package/ /root/package/
WORKDIR /root/package/

# Copy the source code and build a binary wheel
RUN cp -r /usr/local/lib/python*/site-packages/rdkit rdkit
RUN python3.9 setup.py bdist_wheel --py-limited-api $PY_VER

# Use auditwheel to patch RPATH of the modules and strip unnecessary symbols
RUN dnf install -y unzip
RUN auditwheel repair --plat linux_x86_64 dist/pq_rdkit*.whl
RUN rename py3-none ${PY_VER}-${PY_VER} wheelhouse/*

# Upload to package to PQ Pypi
ARG PYPI_PASSWORD
RUN python3.9 -m twine upload -u pqpypi -p $PYPI_PASSWORD --repository-url https://pypi.internal.pq/ wheelhouse/*
