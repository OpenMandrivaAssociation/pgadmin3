%define Summary Graphical client for PostgreSQL

Summary:        %{Summary}
Name:           pgadmin3
Version:        1.22.2
Release:        2
License:        Artistic
Group:          Databases
Source0:        https://ftp.postgresql.org/pub/pgadmin/pgadmin3/v%{version}/src/%{name}-%{version}.tar.gz
Patch0:		pgadmin3-1.12.2-desktop-file.patch
Patch1:         fix-openssl11.patch
URL:            https://www.pgadmin.org/
#BuildRequires:  wxgtku-devel >= 2.8
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:  postgresql-devel
BuildRequires:  desktop-file-utils
BuildRequires:  lib64wxu3.2-devel
# wx-config is a symlink to the Qt config script, which lives in this package.
BuildRequires:  lib64wxqtu3.2-devel
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  imagemagick

%description
PostgreSQL Tools.

%prep
%setup -q
%patch 0 -p0 -b .desktop
%patch 1 -p0 -b .openssl11
# PostgreSQL kwlist.h now passes a fourth PG_KEYWORD argument.
sed -i 's/#define PG_KEYWORD(a,b,c)/#define PG_KEYWORD(a,b,c,d)/' pgadmin/db/keywords.c
# wxQt defines none of the ports this file tests, so bordersize stayed unset.
sed -i 's/#ifdef __WXGTK__/#if defined(__WXGTK__) || defined(__WXQT__)/' \
	pgadmin/ctl/ctlDefaultSecurityPanel.cpp pgadmin/ctl/ctlSecurityPanel.cpp

%build
autoreconf -fi
export CXXFLAGS="$CXXFLAGS -Wno-narrowing"
%configure  --with-wx-version=3.2

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
