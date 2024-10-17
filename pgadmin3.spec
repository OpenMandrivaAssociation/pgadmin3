%define Summary Graphical client for PostgreSQL

Summary:        %{Summary}
Name:           pgadmin3
Version:        1.22.2
Release:        1
License:        Artistic
Group:          Databases
Source0:        ftp://ftp4.fr.postgresql.org/pub/mirrors/postgresql/pgadmin3/release/v1.18.1/src/%{name}-%{version}.tar.gz
Patch0:		pgadmin3-1.12.2-desktop-file.patch
Patch1:         fix-openssl11.patch
URL:            https://www.pgadmin.org/
#BuildRequires:  wxgtku-devel >= 2.8
BuildRequires:  postgresql-devel
BuildRequires:  desktop-file-utils
BuildRequires:  wxgtku3.0-devel >= 3.0
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  imagemagick

%description
PostgreSQL Tools.

%prep
%setup -q
%patch0 -p0 -b .desktop
%patch1 -p0 -b .openssl11

%build
autoreconf -fi
export CXXFLAGS="$CXXFLAGS -Wno-narrowing"
%configure  --with-wx-version=3.0

%make_build

%install
%make_install

desktop-file-install --dir %{buildroot}/%{_datadir}/applications/ \
	--remove-category=Application \
	--add-category=Database \
	pkg/%{name}.desktop

install -d %{buildroot}{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert -size 16x16 pgadmin/include/images/pgAdmin3.png %{buildroot}%{_miconsdir}/%{name}.png
convert -size 32x32 pgadmin/include/images/pgAdmin3.png %{buildroot}%{_iconsdir}/%{name}.png
convert -size 48x48 pgadmin/include/images/pgAdmin3.png %{buildroot}%{_liconsdir}/%{name}.png

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop
