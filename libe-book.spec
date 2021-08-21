#
# Conditional build:
%bcond_with	experimental	# with experimental HTML
%bcond_without	static_libs	# don't build static libraries

Summary:	Library and tools for reading and converting various non-HTML reflowable e-book formats
Summary(pl.UTF-8):	Biblioteka i narzedzia do odczytu i konwersji różnych formatów e-booków
Name:		libe-book
Version:	0.1.3
Release:	5
License:	LGPL v2.1+ or MPL v2.0+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libebook/%{name}-%{version}.tar.xz
# Source0-md5:	2956f1c5e7950b0018979a132165da8b
Patch0:		%{name}-missing.patch
Patch1:		icu68.patch
URL:		http://libebook.sourceforge.net/
BuildRequires:	boost-devel
BuildRequires:	cppunit-devel
BuildRequires:	doxygen
BuildRequires:	gperf
%{?with_experimental:BuildRequires:	libCSS-devel >= 0.6.0}
%{?with_experimental:BuildRequires:	libhubbub-devel >= 0.3.0}
BuildRequires:	libicu-devel
BuildRequires:	liblangtag-devel
%{?with_experimental:BuildRequires:	libmspack-devel}
BuildRequires:	libparserutils-devel
BuildRequires:	librevenge-devel >= 0.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libwapcaplet-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
%{?with_experimental:Requires:	libCSS >= 0.6.0}
%{?with_experimental:Requires:	libhubbub >= 0.3.0}
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
%{?with_experimental:Requires:	libCSS-devel >= 0.6.0}
%{?with_experimental:Requires:	libhubbub-devel >= 0.3.0}
Requires:	libicu-devel
Requires:	liblangtag-devel
%{?with_experimental:Requires:	libmspack-devel}
Requires:	librevenge-devel >= 0.0
Requires:	libstdc++-devel >= 6:4.7
Requires:	libxml2-devel >= 2.0
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
BuildArch:	noarch

%description apidocs
API documentation for libe-book library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libe-book.

%package tools
Summary:	Tools to transform e-books into other formats
Summary(pl.UTF-8):	Programy przekształcania e-booków do innych formatów
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description tools
Tools to transform e-books into other formats. Currently supported:
HTML, text, raw.

%description tools -l pl.UTF-8
Narzędzia do przekształcania e-booków do innych formatów. Aktualnie
obsługiwane są HTML, tekst i format surowy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export CXXFLAGS="%{rpmcxxflags} -Wno-unused-function"
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable experimental} \
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
%attr(755,root,root) %{_libdir}/libe-book-0.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libe-book-0.1.so.1
%{?with_experimental:%{_datadir}/libe-book}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libe-book-0.1.so
%{_includedir}/libe-book-0.1
%{_pkgconfigdir}/libe-book-0.1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libe-book-0.1.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/doxygen/html/*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ebook2html
%attr(755,root,root) %{_bindir}/ebook2raw
%attr(755,root,root) %{_bindir}/ebook2text
