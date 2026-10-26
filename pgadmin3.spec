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
# wx-config asks pkg-config for these, then overwrites the include flags.
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  python

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
# ColTypClass() is const and fills this cache. wxArrayInt::operator[] is const there.
sed -i 's/wxArrayInt colClasses;/mutable wxArrayInt colClasses;/' pgadmin/include/db/pgSet.h
# A bitmap converts to both wxBitmap and wxBitmapBundle, so AddTool is ambiguous.
python << 'PY'
import os


def split_args(text, paren):
    if paren >= len(text) or text[paren] != "(":
        return None, None
    k = paren + 1
    depth = 1
    spans = []
    start = k
    in_str = None
    esc = False
    while k < len(text) and depth:
        c = text[k]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
        else:
            if c in ("'", '"'):
                in_str = c
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    spans.append((start, k))
                    return spans, k
            elif c == "," and depth == 1:
                spans.append((start, k))
                start = k + 1
        k += 1
    return None, None


def rewrite(text):
    out = []
    i = 0
    while True:
        j = text.find("AddTool(", i)
        if j < 0:
            out.append(text[i:])
            break
        spans, end = split_args(text, j + len("AddTool"))
        if spans is None or len(spans) not in (4, 5):
            out.append(text[i:j + 1])
            i = j + 1
            continue
        a, b = spans[2]
        raw = text[a:b]
        stripped = raw.strip()
        if not stripped or stripped.startswith("wxBitmapBundle("):
            out.append(text[i:end + 1])
            i = end + 1
            continue
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()) :]
        out.append(text[i:a])
        out.append(lead + "wxBitmapBundle(" + stripped + ")" + trail)
        out.append(text[b:end + 1])
        i = end + 1
    return "".join(out)


for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        if not filename.endswith((".cpp", ".h", ".cc")):
            continue
        path = os.path.join(dirpath, filename)
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if "AddTool(" not in text:
            continue
        new = rewrite(text)
        if new != text:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)
PY

%build
autoreconf -fi
# The Qt wx-config records these include paths, then replaces them.
export CXXFLAGS="$CXXFLAGS -Wno-narrowing $(pkg-config --cflags Qt5Core Qt5Gui Qt5Widgets Qt5OpenGL Qt5Test)"
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
