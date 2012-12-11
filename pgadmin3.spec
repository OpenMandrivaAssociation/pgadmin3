%define name    pgadmin3
%define version 1.14.0
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
%{_bindir}/png2c

%changelog
* Fri Nov 18 2011 Sergey Zhemoitel <serg@mandriva.org> 1.14.0-1mdv2012.0
+ Revision: 731550
- add new version 1.14.0

* Wed Jun 29 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.12.2-3
+ Revision: 688165
- Rebuild for new PG libs

* Fri Mar 11 2011 Angelo Naselli <anaselli@mandriva.org> 1.12.2-2
+ Revision: 643799
- fixed desktop file icon

* Mon Feb 28 2011 Funda Wang <fwang@mandriva.org> 1.12.2-1
+ Revision: 640976
- update file list
- new version 1.12.2

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.10.1-3mdv2011.0
+ Revision: 614534
- the mass rebuild of 2010.1 packages

* Wed Jan 13 2010 Olivier Thauvin <nanardon@mandriva.org> 1.10.1-2mdv2010.1
+ Revision: 490615
- rebuild

* Tue Dec 15 2009 Frederik Himpe <fhimpe@mandriva.org> 1.10.1-1mdv2010.1
+ Revision: 479077
- update to new version 1.10.1

* Wed Jul 08 2009 Frederik Himpe <fhimpe@mandriva.org> 1.10.0-1mdv2010.0
+ Revision: 393703
- Update to new version 1.10.0
- pgagent is now distributed seperately

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 1.8.4-2mdv2009.0
+ Revision: 268957
- rebuild early 2009.0 package (before pixel changes)

  + Olivier Thauvin <nanardon@mandriva.org>
    - 1.8.4

* Tue Feb 05 2008 Olivier Thauvin <nanardon@mandriva.org> 1.8.2-1mdv2008.1
+ Revision: 162672
- 1.8.2

* Sat Jan 05 2008 Olivier Thauvin <nanardon@mandriva.org> 1.8.1-1mdv2008.1
+ Revision: 145673
- add source0 url
- 1.8.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Oct 27 2007 Olivier Thauvin <nanardon@mandriva.org> 1.8.0-1mdv2008.1
+ Revision: 102597
- 1.8.0

* Tue Jul 17 2007 Jérôme Soyer <saispo@mandriva.org> 1.6.3-1mdv2008.0
+ Revision: 53128
- New release 1.6.3

