Summary:	Jet's Neural library -- for making neural net apps
Summary(pl):	Jet's Neural library -- tworzenie aplikacji neuronowych
Name:		jneural    
Version:	1.05
Release:	2
License:	GPL v2
Group:		Libraries
Source0:	http://www.voltar.org/jneural/jneural-%{version}.tar.gz
Patch0:		jneural-make.patch
BuildRequires:	latex2html tetex
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
I wrote this on account of being completely fed up with starting from
scratch every time I wanted to write a neural app.  I had found some
libraries that did this, but none of them were any good.  Arguably
this isn't either... But I like it. ;)  Probably cuz it's mine right?

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
Requires:	%{name} = %{version}

%description apps
Example jneural applications.

%description apps -l pl
Przyk³adowe programy, wykorzystuj±ce jneural.

%package devel
Summary:	jneural header files
Summary(pl):	Pliki nag³ówkowe jneural
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
jneural header files.

%description devel -l pl
Pliki nag³ówkowe biblioteki jneural.

%package static
Summary:	jneural static library
Summary(pl):	Statyczna biblioteka jneural
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of jneural library.

%description static -l pl
Statyczna wersja biblioteki jneural.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
./configure --prefix=$RPM_BUILD_ROOT/usr
%{__make}

cd docs
texi2dvi -I /usr/share/latex2html/texinputs jneural_doc.tex

%install
rm -rf $RPM_BUILD_ROOT

# broken as much as possible
#%{__make} install

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}

#install apps/grid_w $RPM_BUILD_ROOT%{_bindir}/jn_grid_w
#install apps/sin    $RPM_BUILD_ROOT%{_bindir}/jn_sin

install libjneural.so $RPM_BUILD_ROOT%{_libdir}/libjneural.so.%{version}
install libjneural.a  $RPM_BUILD_ROOT%{_libdir}/libjneural.a
ln -s libjneural.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libjneural.so.1
ln -s libjneural.so.1          $RPM_BUILD_ROOT%{_libdir}/libjneural.so

for i in arch nets utils; do
    install -d $RPM_BUILD_ROOT%{_includedir}/$i
    cp -v include/$i/*.h $RPM_BUILD_ROOT%{_includedir}/$i
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
%attr(755,root,root) %{_libdir}/*.so.*

%files apps
%attr(755,root,root) %{_bindir}/*
%doc apps/matricies.*

%files devel
%defattr(644,root,root,755)
%attr (755,root,root) %{_libdir}/*.so
#%attr (755,root,root) %{_libdir}/*.la
%{_includedir}/arch
%{_includedir}/nets
%{_includedir}/utils
%doc README PROGRESSLOG docs/jneural_doc.dvi

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
