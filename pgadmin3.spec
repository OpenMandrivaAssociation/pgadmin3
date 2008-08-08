%define name    pgadmin3
%define version 1.8.4
%define release %mkrel 2
%define Summary Graphical client for PostgreSQL

Summary:        %{Summary}
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        Artistic
Group:          Databases
Source0:        ftp://ftp4.fr.postgresql.org/pub/mirrors/postgresql/pgadmin3/release/v%{version}/src/%{name}-%{version}.tar.gz
URL:            http://www.pgadmin.org/

BuildRequires:  wxgtku-devel >= 2.8
BuildRequires:  postgresql-devel
BuildRequires:  ImageMagick
BuildRequires:  libxslt-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PostgreSQL Tools.

%prep
%setup -q

%build
%configure
%make all

%install
rm -rf %{buildroot}
%makeinstall

cp -f pgadmin/include/images/elephant48.xpm %{buildroot}%{_datadir}/%{name}/%{name}.xpm
cp -f pkg/%{name}.desktop %{buildroot}/%{_datadir}/%{name}/%{name}.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{Summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Databases;Database;
EOF

install -d $RPM_BUILD_ROOT{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert -size 16x16 pgadmin/include/images/elephant32.xpm $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
convert -size 32x32 pgadmin/include/images/elephant32.xpm $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -size 48x48 pgadmin/include/images/elephant48.xpm $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/pgagent
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
