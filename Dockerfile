FROM quay.io/pypa/manylinux2014_x86_64

# Set the LD path correctly
ARG PY_VER
ENV LD_LIBRARY_PATH=/opt/python/${PY_VER}/lib/:/opt/boost/lib/

# Install build dependencies
RUN yum remove -y libX11-devel libXext-devel libXrender-devel mesa-libGL-devel libICE-devel libSM-devel
RUN yum install -y wget make gcc-c++ cmake flex bison eigen3-devel chrpath freetype-devel

ARG RDKIT_VERSION
RUN wget https://github.com/rdkit/rdkit/archive/Release_${RDKIT_VERSION}.tar.gz && \
    tar xfz Release_${RDKIT_VERSION}.tar.gz && \
    mv rdkit-Release_${RDKIT_VERSION} /root/build/

ARG BOOST_VERSION
RUN wget https://dl.bintray.com/boostorg/release/`echo ${BOOST_VERSION} | sed 's/_/./g'`/source/boost_${BOOST_VERSION}.tar.gz
RUN tar -xzf boost_1_*
RUN cd boost_1_*; \
    ./bootstrap.sh --prefix=/opt/boost --with-libraries=system,iostreams,python,serialization,regex --with-python=/opt/python/${PY_VER}/bin/python; \
    ./b2 install -j8 --prefix=/opt/boost cxxflags="-Wno-deprecated-declarations -Wno-unused-function"

# Install numpy
ARG NUMPY_VERSION
RUN /opt/python/${PY_VER}/bin/python -m pip install numpy==${NUMPY_VERSION}

# Install RDKit
ARG PY_MAJOR_MINOR
WORKDIR /root/build/
RUN export PYTHON_HEADERS=/opt/python/${PY_VER}/include/python*/; \
    cmake -D RDK_INSTALL_INTREE=OFF \
          -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_CXX_FLAGS="-Wno-deprecated-copy" \
          -D RDK_BUILD_INCHI_SUPPORT:BOOL=ON \
          -D RDK_BUILD_THREADSAFE_SSS:BOOL=ON \
          -D RDK_BUILD_CAIRO_SUPPORT:BOOL=OFF \
          -D RDK_BUILD_DESCRIPTORS3D:BOOL=ON \
          -D RDK_BUILD_COORDGEN_SUPPORT:BOOL=OFF \
          -D RDK_BUILD_MOLINTERCHANGE_SUPPORT:BOOL=OFF \
          -D RDK_BUILD_PGSQL:BOOL=OFF \
          -D RDK_PGSQL_STATIC:BOOL=OFF \
          -D RDK_INSTALL_STATIC_LIBS:BOOL=OFF \
          -D RDK_USE_FLEXBISON:BOOL=OFF \
          -D RDK_TEST_MULTITHREADED:BOOL=OFF \
          -D PYTHON_INCLUDE_DIR=${PYTHON_HEADERS} \
          -D PYTHON_EXECUTABLE:FILEPATH=/opt/python/${PY_VER}/bin/python \
          -D RDK_BOOST_PYTHON3_NAME=python`echo ${PY_MAJOR_MINOR} | sed 's/\.//g'` \
          -D BOOST_ROOT=/opt/boost/ \
          . -B .

RUN make -j8
RUN make install

# Install Python tooling + patchelf
RUN ln -s /opt/python/${PY_VER}/bin/python /usr/bin/python-active
RUN python-active -m ensurepip
RUN python-active -m pip install -U pip
RUN python-active -m pip install wheel auditwheel twine
RUN yum install -y patchelf

# Copy skeleton for the Python package
ADD package/ /root/package/
WORKDIR /root/package/

# Copy the source code and build a binary wheel
RUN cp -r /usr/local/lib/python*/site-packages/rdkit rdkit
RUN python-active setup.py bdist_wheel --py-limited-api `echo $PY_VER | cut -d- -f1`

# Use auditwheel to patch RPATH of the modules and strip unnecessary symbols
RUN auditwheel repair --plat manylinux2014_x86_64 dist/pq_rdkit*.whl
RUN rename py3-none ${PY_VER} wheelhouse/*

# Upload to package to PQ Pypi
ARG PYPI_PASSWORD
RUN python-active -m twine upload -u pqpypi -p $PYPI_PASSWORD --repository-url https://pypi.internal.pq/ wheelhouse/*
