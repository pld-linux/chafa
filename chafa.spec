#
# Conditional build:
%bcond_without	apidocs		# gtk-doc API documentation
%bcond_without	avx2		# AVX2 optimized functions
%bcond_without	static_libs	# static library

%ifarch %{ix86}
# uses _mm_extract_epi64 (x86_64 only)
%undefine	with_avx2
%endif

Summary:	Image to character art facsimile
Summary(pl.UTF-8):	Zamiana obrazów na podobiznę ze znaków
Name:		chafa
Version:	1.14.5
Release:	1
License:	LGPL v3+
Group:		Applications/Graphics
#Source0Download: https://github.com/hpjansson/chafa/releases
Source0:	https://github.com/hpjansson/chafa/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	fbf9312beef31e928f34cb6dbcc78bc2
URL:		https://github.com/hpjansson/chafa
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	gtk-doc >= 1.20
BuildRequires:	libavif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libjxl-devel
BuildRequires:	librsvg-devel >= 2.0
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libtool >= 2:2
BuildRequires:	libwebp-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Chafa is a command-line utility that converts image data, including
animated GIFs, into graphics formats or ANSI/Unicode character art
suitable for display in a terminal. It has broad feature support,
allowing it to be used on devices ranging from historical teleprinters
to modern terminal emulators and everything in between.

%description -l pl.UTF-8
Chafa to narzędzie linii poleceń przekształcające dane obrazów, w tym
animowane GIFy na formaty graficzne lub znaki ANSI/Unicode, nadające
się do wyświetlania na terminalu. Ma szeroki zestaw możliwości,
pozwalających na używanie na urządzeniach od historycznych dalekopisów
do współczesnych emulatorów terminali i wszystkiego pomiędzy.

%package libs
Summary:	Image to character art facsimile - shared library
Summary(pl.UTF-8):	Biblioteka współdzielona do zamiany obrazów na podobiznę ze znaków
Group:		Libraries
Requires:	glib2 >= 1:2.26

%description libs
Image to character art facsimile - shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona do zamiany obrazów na podobiznę ze znaków.

%package devel
Summary:	Header files for chafa library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki chafa
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26

%description devel
Header files for chafa library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki chafa.

%package static
Summary:	Static chafa library
Summary(pl.UTF-8):	Statyczna biblioteka chafa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static chafa library.

%description static -l pl.UTF-8
Statyczna biblioteka chafa.

%package apidocs
Summary:	API documentation for chafa library
Summary(pl.UTF-8):	Dokumentacja API biblioteki chafa
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for chafa library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki chafa.

%prep
%setup -q

%if %{without avx2}
%{__sed} -i -e 's/_mm256_abs_epi32/disable_avx2_by_searching_nonexisting_function/' configure.ac
%endif

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-gtk-doc} \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libchafa.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chafa
%{_mandir}/man1/chafa.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md SECURITY.md TODO
%attr(755,root,root) %{_libdir}/libchafa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchafa.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libchafa.so
%dir %{_libdir}/chafa
%{_libdir}/chafa/include
%{_includedir}/chafa
%{_pkgconfigdir}/chafa.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libchafa.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/chafa
%endif
