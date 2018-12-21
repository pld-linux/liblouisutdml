#
# Conditional build:
%bcond_without	java	# Java bindings
#
Summary:	Braille XML transcriber with UTDML
Summary(pl.UTF-8):	Biblioteka tłumacząca XML na alfabet Braille'a przy użyciu UTDML
Name:		liblouisutdml
Version:	2.7.0
Release:	1
License:	LGPL v3+ (library), GPL v3+ (tools)
Group:		Libraries
#Source0Download: http://liblouis.org/downloads/
Source0:	https://github.com/liblouis/liblouisutdml/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	acc6d9f41bb8a7c4316dd42d1f3d5f93
Patch0:		%{name}-info.patch
Patch1:		%{name}-pc.patch
Patch2:		%{name}-liblouis3.patch
URL:		http://liblouis.org/
%{?with_java:BuildRequires:	ant}
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
%{?with_java:BuildRequires:	jdk}
BuildRequires:	help2man
BuildRequires:	liblouis-devel >= 3.8.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	texinfo
Requires:	liblouis >= 3.8.0
# C part of Java bindings is contained in liblouisutdml library if built with java enabled
Provides:	%{name}(java) = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
liblouisutdml is an open-source library providing complete Braille
transcription services for XML, HTML and text documents. It translates
into appropriate Braille codes and formats according to its style
sheet and the specifications in the document. A command-line program,
file2brl which uses this library is also included.

%description -l pl.UTF-8
liblouisutdml to mająca otwarte źródła biblioteka udostępniająca
kompletne usługi tłumaczenia Braille'a dla dokumentów XML, HTML oraz
tekstowych. Wykonuje tłumaczenie na odpowiednie kody i formaty
Braille'a zgodnie z arkuszem styli oraz specyfikacją w dokumencie.
Dołączony jest także program file2brl wykorzystujący bibliotekę.

%package devel
Summary:	Header files for liblouisutdml library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki liblouisutdml
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	liblouis-devel >= 3.8.0

%description devel
Header files for liblouisutdml library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki liblouisutdml.

%package static
Summary:	Static liblouisutdml library
Summary(pl.UTF-8):	Statyczna biblioteka liblouisutdml
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static liblouisutdml library.

%description static -l pl.UTF-8
Statyczna biblioteka liblouisutdml.

%package -n java-liblouisutdml
Summary:	Java bindings for liblouisutdml library
Summary(pl.UTF-8):	Wiązania Javy do biblioteki liblouisutdml
Group:		Libraries/Java
# C part is contained in liblouisutdml library if built with java enabled
Requires:	%{name}(java) = %{version}-%{release}

%description -n java-liblouisutdml
Java bindings for liblouisutdml library.

%description -n java-liblouisutdml -l pl.UTF-8
Wiązania Javy do biblioteki liblouisutdml.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4 -I gnulib/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_java:--disable-java-bindings}

%{__make}

%if %{with java}
cd java
%ant
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
install java/jliblouisutdml.jar $RPM_BUILD_ROOT%{_javadir}
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblouisutdml.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/liblouisutdml

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/copyright-notice
%attr(755,root,root) %{_bindir}/file2brl
%attr(755,root,root) %{_libdir}/liblouisutdml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblouisutdml.so.8
%{_datadir}/liblouisutdml
%{_mandir}/man1/file2brl.1*

%files devel
%defattr(644,root,root,755)
%doc doc/liblouisutdml.html
%attr(755,root,root) %{_libdir}/liblouisutdml.so
%{_includedir}/liblouisutdml
%{_pkgconfigdir}/liblouisutdml.pc
%{_infodir}/liblouisutdml.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/liblouisutdml.a

%if %{with java}
%files -n java-liblouisutdml
%defattr(644,root,root,755)
%{_javadir}/jliblouisutdml.jar
%endif
