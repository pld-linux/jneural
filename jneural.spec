Summary:	Jet's Neural library - for making neural net apps
Summary(pl.UTF-8):	Jet's Neural library - tworzenie aplikacji neuronowych
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
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	latex2html
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	tetex-latex-ams
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex-bibtex
BuildRequires:	texinfo-texi2dvi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
I wrote this on account of being completely fed up with starting from
scratch every time I wanted to write a neural app. I had found some
libraries that did this, but none of them were any good. Arguably this
isn't either... But I like it. ;) Probably cuz it's mine right?

-Jet (jettero@voltar-confed.org)

%description -l pl.UTF-8
Ten pakiet powstał, ponieważ autor miał już dość zaczynania za każdym
razem od zera, kiedy chciał napisać aplikację neuronową. Znalazł kilka
bibliotek do tego celu, ale żadna nie była dobra. Prawdopodobnie ta
też nie jest, ale przynajmniej autor ją lubi ;)

%package apps
Summary:	Example jneural applications
Summary(pl.UTF-8):	Przykładowe programy, wykorzystujące jneural
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description apps
Example jneural applications.

%description apps -l pl.UTF-8
Przykładowe programy, wykorzystujące jneural.

%package devel
Summary:	jneural header files
Summary(pl.UTF-8):	Pliki nagłówkowe jneural
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
jneural header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki jneural.

%package static
Summary:	jneural static library
Summary(pl.UTF-8):	Statyczna biblioteka jneural
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of jneural library.

%description static -l pl.UTF-8
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
#install apps/sin $RPM_BUILD_ROOT%{_bindir}/jn_sin

install libjneural.so $RPM_BUILD_ROOT%{_libdir}/libjneural.so.%{version}
install libjneural.a $RPM_BUILD_ROOT%{_libdir}/libjneural.a
ln -s libjneural.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libjneural.so.1
ln -s libjneural.so.1 $RPM_BUILD_ROOT%{_libdir}/libjneural.so

for i in arch nets utils; do
	install -d $RPM_BUILD_ROOT%{_includedir}/$i
	install include/$i/*.h $RPM_BUILD_ROOT%{_includedir}/$i
done

for i in `find apps/ -perm -700 -type f`; do
	install $i $RPM_BUILD_ROOT%{_bindir}
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
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
