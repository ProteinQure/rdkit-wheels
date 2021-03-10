FROM fedora:33

# Install build dependencies
RUN dnf install -y rpm-build rpmdevtools make gcc-c++ cmake flex bison libpq-devel python3-numpy inchi-devel cairo-devel eigen3-devel chrpath swig java-devel junit python3-devel boost-python3-devel catch-devel
RUN rpmdev-setuptree

ADD assets/rdkit.spec /root/rpmbuild/SPECS/
ADD assets/*.patch /root/rpmbuild/SOURCES/

RUN spectool -g -R /root/rpmbuild/SPECS/rdkit.spec
RUN rpmbuild -bb /root/rpmbuild/SPECS/rdkit.spec
