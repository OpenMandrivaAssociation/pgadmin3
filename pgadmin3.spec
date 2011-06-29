%define name    pgadmin3
%define version 1.12.2
%define release %mkrel 3
%define Summary Graphical client for PostgreSQL

Summary:        %{Summary}
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        Artistic
Group:          Databases
Source0:        ftp://ftp4.fr.postgresql.org/pub/mirrors/postgresql/pgadmin3/release/v%{version}/src/%{name}-%{version}.tar.gz
Patch0:		pgadmin3-1.12.2-link.patch
Patch1:		pgadmin3-1.12.2-desktop-file.patch
URL:            http://www.pgadmin.org/
BuildRequires:  wxgtku-devel >= 2.8
BuildRequires:  postgresql-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libxslt-devel
BuildRequires:  imagemagick
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PostgreSQL Tools.

%prep
%setup -q
%patch0 -p0 -b .link
%patch1 -p0 -b .desktop

%build
autoreconf -fi
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

desktop-file-install --dir %{buildroot}/%{_datadir}/applications/ \
	--remove-category=Application \
	--add-category=Database \
	pkg/%{name}.desktop

install -d $RPM_BUILD_ROOT{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert -size 16x16 pgadmin/include/images/pgAdmin3.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
convert -size 32x32 pgadmin/include/images/pgAdmin3.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -size 48x48 pgadmin/include/images/pgAdmin3.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop
