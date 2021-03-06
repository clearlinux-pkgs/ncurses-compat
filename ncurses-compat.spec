Name:       ncurses-compat
Summary:    See the file ANNOUNCE for a summary of ncurses features and ports
Version:    5.9
Release:    43
Group:      System/Libraries
License:    MIT
URL:        http://mirrors.kernel.org/gnu/ncurses/ncurses-5.9.tar.gz
Source0:    http://mirrors.kernel.org/gnu/ncurses/ncurses-5.9.tar.gz
Patch0:     ncurses-5.9-gcc5_buildfixes-1.patch
Patch1:     CVE-2018-10754.patch
Patch2:     CVE-2019-17595.patch
Requires:   ncurses-lib
Requires:   ncurses-lib-narrow
BuildRequires:  python3-dev pkg-config-dev
BuildRequires : gcc-dev32
BuildRequires : gcc-libgcc32
BuildRequires : gcc-libstdc++32
BuildRequires : glibc-dev32
BuildRequires : glibc-libc32

%description
See the file ANNOUNCE for a summary of ncurses features and ports.
See the file INSTALL for instructions on how to build and install ncurses.
See the file NEWS for a release history and bug-fix notes.
See the file TO-DO for things that still need doing, including known bugs.


%package lib
Summary:    Library components for the ncurses package
Group:      Libraries
Requires:   ncurses-data

%description lib
Library files for the ncurses package

%package lib32
Summary:    Library components for the ncurses package
Group:      Libraries
Requires:   ncurses-data

%description lib32
Library files for the ncurses package

%package lib-narrow
Summary:    Library components for the ncurses package
Group:      Libraries
Requires:   ncurses-data

%description lib-narrow
Library files for the ncurses package


%prep
%setup -q -n ncurses-5.9
%patch0 -p1
%patch1 -p1
%patch2 -p1
pushd ../
cp -a ncurses-5.9 build32
cp -a ncurses-5.9 build32w
cp -a ncurses-5.9 ncurses-5.9w
popd


%build
export CFLAGS="$CFLAGS -Os -ffunction-sections"
export CXXFLGAGS="$CXXFLAGS -std=gnu++98 "

%configure --disable-static \
    --with-shared \
    --with-termlib \
    --with-progs \
    --enable-pc-files \
    --with-pkg-config=/usr/bin/pkg-config \
    --without-cxx-binding

make V=1 %{?_smp_mflags}

pushd ../ncurses-5.9w
export PKG_CONFIG_LIBDIR=/usr/lib64/pkgconfig

%configure --disable-static \
    --with-shared \
    --with-termlib \
    --enable-widec \
    --enable-pc-files \
    --with-pkg-config=/usr/bin/pkg-config \
    --without-cxx-binding

popd

export CFLAGS="$CFLAGS -m32 -mstackrealign"
export PKG_CONFIG_LIBDIR=/usr/lib32/pkgconfig

pushd ../build32
%configure --disable-static \
    --with-shared \
    --with-termlib \
    --with-progs \
    --enable-pc-files \
    --with-pkg-config=/usr/bin/pkg-config \
    --without-cxx-binding \
    --libdir=/usr/lib32

make V=1 %{?_smp_mflags}
popd

pushd ../build32w
export PKG_CONFIG_LIBDIR=/usr/lib64/pkgconfig

%configure --disable-static \
    --with-shared \
    --with-termlib \
    --enable-widec \
    --enable-pc-files \
    --with-pkg-config=/usr/bin/pkg-config \
    --without-cxx-binding \
    --libdir=/usr/lib32

popd


%install
rm -rf %{buildroot}

CFLAGS_ORIG="$CFLAGS"

mkdir -p %{buildroot}/usr/lib
export CFLAGS="$CFLAGS_ORIG -m32 -mstackrealign"

pushd ../build32
%make_install32
popd
pushd ../build32w
%make_install32
popd
export CFLAGS="$CFLAGS_ORIG -m64"

%make_install

pushd ../ncurses-5.9w
make V=1 %{?_smp_mflags}
%make_install
popd

### these utterly disgusting hacks are stolen from Fedora.

# don't require -ltinfo when linking with --no-add-needed
for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
    soname=$(basename $(readlink $l))
    rm -f $l
    echo "INPUT($soname -ltinfo)" > $l
done

rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so


%files
%defattr(-,root,root,-)
%exclude /usr/include/*.h
%exclude /usr/lib64/*.so
%exclude /usr/lib64/pkgconfig/*.pc
%exclude /usr/bin

%files lib
%defattr(-,root,root,-)
/usr/lib64/libformw.so.*
/usr/lib64/libmenuw.so.*
/usr/lib64/libncursesw.so.*
/usr/lib64/libpanelw.so.*
/usr/lib64/libtinfow.so.*
/usr/lib64/libtinfo.so.5
/usr/lib64/libtinfo.so.5.9

%files lib-narrow
/usr/lib64/libform.so.5
/usr/lib64/libform.so.5.9
/usr/lib64/libmenu.so.5
/usr/lib64/libmenu.so.5.9
/usr/lib64/libncurses.so.5
/usr/lib64/libncurses.so.5.9
/usr/lib64/libpanel.so.5
/usr/lib64/libpanel.so.5.9
/usr/lib64/libtinfo.so.5
/usr/lib64/libtinfo.so.5.9
%exclude /usr/lib/terminfo
%exclude /usr/share/terminfo
%exclude /usr/share/man
%exclude /usr/share/tabset

%files lib32
%exclude /usr/lib32/*.so
/usr/lib32/libform.so.5
/usr/lib32/libform.so.5.9
/usr/lib32/libformw.so.5
/usr/lib32/libformw.so.5.9
/usr/lib32/libmenu.so.5
/usr/lib32/libmenu.so.5.9
/usr/lib32/libmenuw.so.5
/usr/lib32/libmenuw.so.5.9
/usr/lib32/libncurses.so.5
/usr/lib32/libncurses.so.5.9
/usr/lib32/libncursesw.so.5
/usr/lib32/libncursesw.so.5.9
/usr/lib32/libpanel.so.5
/usr/lib32/libpanel.so.5.9
/usr/lib32/libpanelw.so.5
/usr/lib32/libpanelw.so.5.9
/usr/lib32/libtinfo.so.5
/usr/lib32/libtinfo.so.5.9
/usr/lib32/libtinfow.so.5
/usr/lib32/libtinfow.so.5.9
