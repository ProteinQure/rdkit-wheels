%global with_docs 0
%global with_tests 0

%global year        2020
%global month       09
%global extraver    5
%global pkgname     Release_%{year}_%{month}_%{extraver}
%global rootdir     rdkit-%{pkgname}

Name:           rdkit
Version:        %{year}.%{month}.%{extraver}
Release:        15%{?dist}
Summary:        Chemical informatics and machine learning toolkit
License:        BSD
URL:            http://www.rdkit.org/
Source0:        https://github.com/rdkit/rdkit/archive/%{pkgname}.tar.gz

BuildRequires: make
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libpq-devel
BuildRequires:  python3-numpy
BuildRequires:  inchi-devel
BuildRequires:  cairo-devel
BuildRequires:  eigen3-devel
BuildRequires:  chrpath
BuildRequires:  swig
BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  python3-devel
BuildRequires:  boost-python3-devel
BuildRequires:  catch-devel

%if 0%{?with_docs}
# Docs build deps
BuildRequires: python-sphinx-latex
BuildRequires: python3-recommonmark
BuildRequires: epydoc
BuildRequires: doxygen
BuildRequires: pandoc
BuildRequires: latexmk
%endif

# Needed for tests
%if 0%{?with_tests}
BuildRequires:  python3-cairocffi
BuildRequires:  python3-pandas
BuildRequires:  python3-pillow
BuildRequires:  xorg-x11-fonts-Type1
%endif

Patch0:         rdkit-2015.03-use_cairo_backend_on_tests.patch
Patch1:         rdkit-2018.03-do_not_install_sping.patch
#Patch2:         rdkit-Release_2019_03_3-gcc10.patch

%description
Chemical informatics and machine learning toolkit

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}

%description devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.


%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation files for %{name}.


%package -n python3-rdkit
Summary:        Python 3 bindings for RDKit libraries
%{?python_provide:%python_provide python3-rdkit}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-numpy
Requires:       python3-cairocffi
Requires:       python3-pillow
Requires:       xorg-x11-fonts-Type1

%description -n python3-rdkit
Python 3 bindings for RDKit libraries


%prep
%setup -c -q -n %{rootdir}
mv %{rootdir} python3
pushd python3
%patch0 -p1
%patch1 -p1
#%patch2 -p1

rm -rf rdkit/sping

# Copy docs to top dir
cp -pr license.txt ReleaseNotes.* ../
popd

find python3 -name '*.py' | xargs sed -i '1s|^#!.*|#!%{__python3}|'

# fix tests scripts for python3 runtime
find python3 -name 'test_list.py' | xargs sed -i 's/"python"/"python3"/g'
find python3 -name 'test_list.py' | xargs sed -i "s/'python'/'python3'/g"
sed -i.orig 's/python/python3/g' python3/Projects/DbCLI/TestDbCLI.py


%build
# fix rpmlint "unused-direct-shlib-dependency"
export CXXFLAGS="%{optflags} -Wl,--as-needed"

pushd python3

# Python 3 build
%cmake  -D RDK_INSTALL_INTREE=OFF \
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
        -D PYTHON_EXECUTABLE:FILEPATH=%{__python3} \
        -D RDK_BOOST_PYTHON3_NAME=python%{python3_version_nodots} \
        -D CATCH_DIR:FILEPATH=%{_includedir}/catch2 \
%ifnarch %{ix86} x86_64
        -D RDK_OPTIMIZE_NATIVE:BOOL=OFF \
%endif
        . -B .
#        -D RDK_BUILD_SWIG_WRAPPERS:BOOL=ON \

make %{?_smp_mflags}


%if 0%{with_docs}
# Documentation (does not currently build on EPEL)
export RDBASE=%{_builddir}/%{rootdir}/python3
export LD_LIBRARY_PATH=$RDBASE/lib
export PYTHONPATH=$RDBASE
pushd rdkit
epydoc --config epydoc.config
popd
pushd Code
doxygen doxygen/doxygen.config
popd
pushd Docs/Book
make latexpdf
popd
%endif

popd

%install
# install Python 3 bindings
pushd python3
make install DESTDIR=%{buildroot}
popd

# remove installed doc files
rm -r %{buildroot}/%{_datadir}/RDKit

# Fix rpmlint warnings
FMCS=%{buildroot}%{python3_sitearch}/rdkit/Chem/fmcs/fmcs
sed '1{\@^#!%{__python3}@d}' $FMCS.py > $FMCS.new &&
touch -r $FMCS.py $FMCS.new &&
mv $FMCS.new $FMCS.py
rm $FMCS


%check
%if 0%{?with_tests}
# exclude PostgreSQL tests as they require a running DB instance
pushd python3
export RDBASE=%{_builddir}/%{rootdir}/python3
export LD_LIBRARY_PATH=$RDBASE/lib
export PYTHONPATH=$RDBASE
ARGS="-V -E 'pythonTestSping|testPgSQL'" make test
popd
%endif

%ldconfig_scriptlets


%files
%license license.txt
%doc ReleaseNotes.*
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/rdkit
%{_libdir}/lib*.so
%{_libdir}/cmake/rdkit/*.cmake

%files doc
%if 0%{?with_docs}
%doc python3/Docs/Book/_build/latex/RDKit.pdf
%endif

%files -n python3-rdkit
%{python3_sitearch}/rdkit

%changelog
* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 2019.03.3-15
- rebuild for libpq ABI fix rhbz#1908268

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2019.03.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 2019.03.3-13
- Rebuilt for Boost 1.75

* Thu Oct 01 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2019.03.3-12
- Make the package build with updated %%cmake macro (#1884363)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.03.3-11
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.03.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2019.03.3-9
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sat May 30 2020 Jonathan Wakely <jwakely@redhat.com> - 2019.03.3-8
- Rebuilt for Boost 1.73

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2019.03.3-7
- Rebuilt for Python 3.9

* Wed Mar 04 2020 Than Ngo <than@redhat.com> - 2019.03.3-6
- Fixed bz#1808661, FTBFS

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.03.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2019.03.3-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2019.03.3-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.03.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Gianluca Sforna <giallu@gmail.com> - 2019.03.3-1
- upstream release 2019.03.3

* Thu Apr 11 2019 Gianluca Sforna <giallu@gmail.com> - 2019.03.1-1
- upstream release 2019.03.1

* Thu Feb 28 2019 Gianluca Sforna <giallu@gmail.com> - 2018.09.2-1
- upstream release 2018.09.2
- drop upstreamed patch

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.03.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Jonathan Wakely <jwakely@redhat.com> - 2018.03.4-3
- Rebuilt for Boost 1.69

* Mon Oct 22 2018 Petr Kubat <pkubat@redhat.com> - 2017.03.4-2
- rebuild for PostgreSQL 11
- use lowercased postgresql boolean definitions

* Tue Sep 25 2018 Gianluca Sforna <giallu@gmail.com> - 2018.03.4-1
- upstream release 2018.03.4
- remove python 2 build for Fedora 30

* Wed Sep 05 2018 Pavel Raiskup <praiskup@redhat.com> - 2018.03.2-3
- rebuild against postgresql-server-devel (rhbz#1618698)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.03.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Gianluca Sforna <giallu@gmail.com> - 2018.03.2-1
- upstream release 2018.03.2
- disable few features to fix build (network access)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2017.09.3-4
- Rebuilt for Python 3.7

* Tue Apr  3 2018 Gianluca Sforna <giallu@gmail.com> - 2017.09.3-2
- Fix EPEL build

* Tue Mar 27 2018 Gianluca Sforna <giallu@gmail.com> - 2017.09.3-1
- upstream release 2017.09.3

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2017.09.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017.09.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 11 2017 Gianluca Sforna <giallu@gmail.com> - 2017.09.1-1
- new upstream release
- drop upstreamed patch

* Tue Oct 10 2017 Pavel Raiskup <praiskup@redhat.com> - 2017.03.3-6
- rebuild for PostgreSQL 10

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.03.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.03.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Björn Esser <besser82@fedoraproject.org> - 2017.03.3-3
- Rebuilt for Boost 1.64

* Fri Jul 21 2017 Gianluca Sforna <giallu@gmail.com> - 2017.3.3-2
- fix FTBS in rawhide

* Mon Jul 10 2017 Gianluca Sforna <giallu@gmail.com> - 2017.3.3-1
- new upstream release

* Mon Apr 03 2017 Gianluca Sforna <giallu@gmail.com> - 2017.3.1-1
- new upstream release

* Thu Feb 23 2017 Gianluca Sforna <giallu@gmail.com> - 2016.09.4-1
- new upstream release

* Tue Feb 07 2017 Kalev Lember <klember@redhat.com> - 2016.09.3-2
- Rebuilt for Boost 1.63

* Fri Dec 30 2016 Gianluca Sforna <giallu@gmail.com> - 2016.09.3-1
- new upstream release

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2016.09.2-4
- Rebuild for Python 3.6

* Sat Nov 26 2016 Gianluca Sforna <giallu@gmail.com> - 2016.09.2-3
- BR eigen3-devel to activate build of more descriptors

* Wed Nov 23 2016 Gianluca Sforna <giallu@gmail.com> - 2016.09.2-1
- new upstream release
- clean up spec (no more EL6 builds)

* Mon Nov 21 2016 Dan Horák <dan[at]danny.cz> - 2016.09.1-2
- fix non-x86 builds universally

* Fri Nov 11 2016 Gianluca Sforna <giallu@gmail.com> - 2016.09.1-1
- new upstream release
- fix ppc/ppc64 build
- drop upstreamed patches

* Wed Nov  2 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.5-1
- new upstream release
- fix moldraw headers installation with upstream patch
- drop upstreamed patches

* Mon Oct 10 2016 Pavel Raiskup <praiskup@redhat.com> - 2016.03.2-8
- rebuild for postgresql 9.6.0, add guard for incompatible PG plugin
  installation

* Sun Sep 18 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.2-7
- fix aarch64 build

* Fri Aug 19 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.2-6
- fix unused-direct-shlib-dependency rpmlint warning

* Wed Aug 17 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.2-5
- fix wrong-script-interpreter rpmlint error

* Thu Aug 11 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.2-4
- skip PgSQL tests not working in the build environment
- fix PgSQL cartridge installation

* Fri Aug  5 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.2-3
- fix arm build
- use CMAKE to build PgSQL cartridge

* Tue Aug  2 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.2-2
- fix build on rawhide

* Thu Jul 21 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.2-1
- new upstream release
- fix documentation build on Fedora 24
- add patch for broken cartridge build

* Mon Apr 18 2016 Gianluca Sforna <giallu@gmail.com> - 2016.03.1-1
- new upstream release

* Fri Dec  4 2015 Gianluca Sforna <giallu@gmail.com> - 2015.09.2-2
- Fix tests for python 3 wrappers

* Wed Nov 18 2015 Gianluca Sforna <giallu@gmail.com> - 2015.09.2-1
- new upstream release

* Sun Nov  8 2015 Gianluca Sforna <giallu@gmail.com> - 2015.09.1-1
- new upstream release

* Sat Sep 19 2015 Gianluca Sforna <giallu@gmail.com> - 2015.03.1-3
- more fixes from package review
- activate cairo rendering
- add python3 wrappers

* Mon Jul  6 2015 Gianluca Sforna <giallu@gmail.com> - 2015.03.1-2
- activate threading
- always test in verbose mode

* Thu Apr 30 2015 Gianluca Sforna <giallu@gmail.com> - 2015.03.1-1
* new upstream release

* Mon Dec  8 2014 Gianluca Sforna <giallu@gmail.com> - 2014.09.2-1
- new upstream release

* Wed Oct 29 2014 Gianluca Sforna <giallu@gmail.com> - 2014.09.1-1
- new upstream release
- rebase patches

* Wed Jul 16 2014 Gianluca Sforna <giallu@gmail.com> - 2014.03.1-3
- let base package own _datadir/RDKit

* Tue May 27 2014 Gianluca Sforna <giallu@gmail.com> - 2014.03.1-2
- fix EPEL build by adding python2_* macros

* Mon May 12 2014 Gianluca Sforna <giallu@gmail.com> - 2014.03.1-1
- new upstream release
- disable static build with cmake flag, drop related patch

* Sun Mar 30 2014 Gianluca Sforna <giallu@gmail.com> - 2013.09.2-1
- new upstream release
- more spec fixes from review ticket

* Mon Jan  6 2014 Gianluca Sforna <giallu@gmail.com> - 2013.09.1-2
- move cmake files under %%_libdir/cmake

* Mon Nov 11 2013 Gianluca Sforna <giallu@gmail.com> - 2013.09.1-1
- new upstream release

* Tue Jul 30 2013 Gianluca Sforna <giallu@gmail.com> - 2013.06.1-2
- use %%cmake macro
- fix tests in rawhide

* Sun Jul 28 2013 Gianluca Sforna <giallu@gmail.com> - 2013.06.1-1
- new upstream release
- spec clean up

* Thu May 30 2013 Gianluca Sforna <giallu@gmail.com> - 2013.03.2-1
- new upstream release
- fix shebang on rdkit/Chem/MCS.py

* Wed May 29 2013 Gianluca Sforna <giallu@gmail.com> - 2013.03-2
- spec fixes from package review (#804125)

* Sat Apr 27 2013 Gianluca Sforna <giallu@gmail.com> - 2013.03-1
- new upstream release

* Wed Feb  6 2013 Gianluca Sforna <giallu@gmail.com> - 2012.12-2
- add inchi support

* Tue Jan 22 2013 Gianluca Sforna <giallu@gmail.com> - 2012.12-1
- New upstream release
- BR fonts package

* Sun Oct 21 2012 Gianluca Sforna <giallu@gmail.com> - 2012.09-1
- New upstream release
- add python related requires

* Wed Jul 11 2012 Gianluca Sforna <giallu@gmail.com> - 2012.06-1
- New upstream release

* Fri Apr 13 2012 Gianluca Sforna <giallu@gmail.com> - 2012.03-1
- New upstream release
- Fix some packaging issues as per review (#804125)

* Wed Mar 07 2012 Gianluca Sforna <giallu@gmail.com> - 2011.12-1
- New upstream release

* Mon Dec 05 2011 Gianluca Sforna <giallu@gmail.com> - 2011.09-2.20111202svn1877
- Package a newer snapshot for postgres 9.1 support
- Remove rpath from postgres cartridge

* Fri Nov 25 2011 Gianluca Sforna <giallu@gmail.com> - 2011.09-1
- New upstream release
- rebase patches
- drop upstreamed patch

* Mon Aug 15 2011 Gianluca Sforna <giallu@gmail.com> - 2011.06-2
- Final release
- add SDMOlsupplier patch, fixes loop on tests

* Wed Jul  6 2011 Gianluca Sforna <giallu@gmail.com> - 2011.06-1
- New upstream (beta) release
- rebase patches

* Mon Jun 13 2011 Gianluca Sforna <giallu@gmail.com> - 2011.03-1
- New upstream release
- drop upstreamed patch

* Wed Apr  6 2011 Gianluca Sforna <giallu@gmail.com> - 2010.12-3
- Add draw_refactoring patch

* Fri Jan 14 2011 Gianluca Sforna <giallu@gmail.com> - 2010.12-2
- New upstream release
- filter auto-provides for python extensions

* Thu Dec 30 2010 Gianluca Sforna <giallu@gmail.com> - 2010.12-1
- New upstream (beta) release
- drop upstream patch
- add patches for rpath, static libs
- Fix spurious executable bits

* Mon Oct  4 2010 Gianluca Sforna <giallu@gmail.com> - 2010.09-1
- New upstream release
- Move build in tree to support tests
- build PostgreSQL cartridge

* Tue Sep  7 2010 Gianluca Sforna <giallu gmail com>
- Split subpackages

* Mon Jul  5 2010 Gianluca Sforna <giallu gmail com> - 2010.Q2-1
- Initial package
