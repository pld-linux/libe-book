#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library and tools for reading and converting various non-HTML reflowable e-book formats
Summary(pl.UTF-8):	Biblioteka i narzedzia do odczytu i konwersji różnych formatów e-booków
Name:		libe-book
Version:	0.0.2
Release:	1
License:	LGPL v2.1+ or MPL v2.0+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libebook/%{name}-%{version}.tar.xz
# Source0-md5:	41d601490e86682ddda93f43297ee561
URL:		http://libebook.sourceforge.net/
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	gperf
BuildRequires:	libicu-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libwpd-devel >= 0.9.5
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	libwpd >= 0.9.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libe-book is a library and a set of tools for reading and converting
various non-HTML reflowable e-book formats.

Currently supported are:
- eReader .pdb
- FictionBook v. 2 (including zipped files)
- PalmDoc Ebook
- Plucker .pdb
- QiOO (mobile format, for java-enabled cellphones)
- TCR (simple compressed text format)
- TealDoc
- zTXT
- ZVR (simple compressed text format)

%description -l pl.UTF-8
libe-book to biblioteka i zestaw narzędzi do odczytu i konwersji
różnych nie-HTML-owych, tekstowych formatów e-booków.

Obecnie obsługiwane są:
- eReader .pdb
- FictionBook w wersji 2 (wraz z plikami skompresowanymi zipem)
- PalmDoc Ebook
- Plucker .pdb
- QiOO (format przenośny, dla telefonów z Javą)
- TCR (prosty skompresowany format tekstowy)
- TealDoc
- zTXT
- ZVR (prosty skompresowany format tekstowy)

%package devel
Summary:	Header files for libe-book library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libe-book
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	libwpd-devel >= 0.9.5
Requires:	zlib-devel

%description devel
Header files for libe-book library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libe-book.

%package static
Summary:	Static libe-book library
Summary(pl.UTF-8):	Statyczna biblioteka libe-book
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libe-book library.

%description static -l pl.UTF-8
Statyczna biblioteka libe-book.

%package apidocs
Summary:	libe-book API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libe-book
Group:		Documentation

%description apidocs
API documentation for libe-book library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libe-book.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libe-book-*.la
# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libe-book

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/ebook2html
%attr(755,root,root) %{_bindir}/ebook2raw
%attr(755,root,root) %{_bindir}/ebook2text
%attr(755,root,root) %{_libdir}/libe-book-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libe-book-0.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libe-book-0.0.so
%{_includedir}/libe-book-0.0
%{_pkgconfigdir}/libe-book-0.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libe-book-0.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/doxygen/html/*
