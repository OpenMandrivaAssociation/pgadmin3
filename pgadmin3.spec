%define name    pgadmin3
%define version 1.12.2
%define release %mkrel 1
%define Summary Graphical client for PostgreSQL

Summary:        %{Summary}
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        Artistic
Group:          Databases
Source0:        ftp://ftp4.fr.postgresql.org/pub/mirrors/postgresql/pgadmin3/release/v%{version}/src/%{name}-%{version}.tar.gz
Patch0:		pgadmin3-1.12.2-link.patch
URL:            http://www.pgadmin.org/
BuildRequires:  wxgtku-devel >= 2.8
BuildRequires:  postgresql-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libxslt-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PostgreSQL Tools.

%prep
%setup -q
%patch0 -p0 -b .link

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
