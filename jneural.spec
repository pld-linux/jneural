Summary:	Jet's Neural library - for making neural net apps
Summary(pl):	Jet's Neural library - tworzenie aplikacji neuronowych
Name:		jneural
Version:	1.05
Release:	5
License:	GPL v2
Group:		Libraries
Source0:	http://www.voltar.org/jneural/%{name}-%{version}.tar.gz
# Source0-md5:	79afdc55601a7e5a22b303b566c37525
Patch0:		%{name}-make.patch
Patch1:		%{name}-yacc.patch
Patch2:		%{name}-c++.patch
BuildRequires:	bison
BuildRequires:	latex2html
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	tetex-latex-bibtex
BuildRequires:	texinfo-texi2dvi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
I wrote this on account of being completely fed up with starting from
scratch every time I wanted to write a neural app. I had found some
libraries that did this, but none of them were any good. Arguably this
isn't either... But I like it. ;) Probably cuz it's mine right?

-Jet (jettero@voltar-confed.org)

%description -l pl
Ten pakiet powsta³, poniewa¿ autor mia³ ju¿ do¶æ zaczynania za ka¿dym
razem od zera, kiedy chcia³ napisaæ aplikacjê neuronow±. Znalaz³ kilka
bibliotek do tego celu, ale ¿adna nie by³a dobra. Prawdopodobnie ta
te¿ nie jest, ale przynajmniej autor j± lubi ;)

%package apps
Summary:	Example jneural applications
Summary(pl):	Przyk³adowe programy, wykorzystuj±ce jneural
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description apps
Example jneural applications.

%description apps -l pl
Przyk³adowe programy, wykorzystuj±ce jneural.

%package devel
Summary:	jneural header files
Summary(pl):	Pliki nag³ówkowe jneural
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
jneural header files.

%description devel -l pl
Pliki nag³ówkowe biblioteki jneural.

%package static
Summary:	jneural static library
Summary(pl):	Statyczna biblioteka jneural
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of jneural library.

%description static -l pl
Statyczna wersja biblioteki jneural.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
%configure

# make shared lib with PIC
%{__make} libjneural.so libjneural.a \
	CC="%{__cxx}" \
	DFLAGS="%{rpmcflags} -fPIC" \
	YACC="bison -y"

# and make apps, without unnecessary PIC
%{__make} \
	CC="%{__cxx}" \
	DFLAGS="%{rpmcflags}"

cd docs
texi2dvi -I %{_datadir}/latex2html/texinputs jneural_doc.tex

%install
rm -rf $RPM_BUILD_ROOT

# broken as much as possible
#%%{__make} install

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

#install apps/grid_w $RPM_BUILD_ROOT%{_bindir}/jn_grid_w
#install apps/sin    $RPM_BUILD_ROOT%{_bindir}/jn_sin

install libjneural.so $RPM_BUILD_ROOT%{_libdir}/libjneural.so.%{version}
install libjneural.a  $RPM_BUILD_ROOT%{_libdir}/libjneural.a
ln -s libjneural.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libjneural.so.1
ln -s libjneural.so.1          $RPM_BUILD_ROOT%{_libdir}/libjneural.so

for i in arch nets utils; do
	install -d $RPM_BUILD_ROOT%{_includedir}/$i
	install include/$i/*.h $RPM_BUILD_ROOT%{_includedir}/$i
done

for i in `find apps/ -perm -700 -type f`; do
	install $i $RPM_BUILD_ROOT%{_bindir}
done

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README PROGRESSLOG
%attr(755,root,root) %{_libdir}/*.so.*.*

%files apps
%defattr(644,root,root,755)
%doc apps/matricies.*
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%doc docs/jneural_doc.dvi
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/arch
%{_includedir}/nets
%{_includedir}/utils

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
