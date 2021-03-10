FROM fedora:33

RUN dnf install rpm-build rpmdevtools -y
RUN rpmdev-setuptree
ADD assets/rdkit.spec /root/rpmbuild/SPECS/
ADD assets/*.patch /root/rpmbuild/SOURCES/
RUN spectool -g -R /root/rpmbuild/SPECS/rdkit.spec
RUN rpmbuild -bb /root/rpmbuild/SPECS/rdkit.spec
