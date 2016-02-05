Name:           xgap
Version:        4.23
Release:        12%{?dist}
Summary:        GUI for GAP

License:        GPLv2+
URL:            http://www-groups.mcs.st-and.ac.uk/~neunhoef/Computer/Software/Gap/%{name}4.html
Source0:        http://www-groups.mcs.st-and.ac.uk/~neunhoef/Computer/Software/Gap/%{name}4/%{name}-%{version}.tar.gz
# Created by Jerry James <loganjerry@gmail.com>
Source1:        %{name}.desktop
# Created by Paulo César Pereira de Andrade
# <paulo.cesar.pereira.de.andrade@gmail.com>
Source2:        XGap
# Sent upstream 9 May 2012.  This patch quiets some compiler warnings.
Patch0:         %{name}-warning.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gap-devel
BuildRequires:  libXaw-devel
BuildRequires:  tex-tex
BuildRequires:  tex(manfnt.tfm)
BuildRequires:  tth

Requires:       gap-core

Provides:       gap-pkg-xgap = %{version}-%{release}

%description
A X Windows GUI for GAP.

%prep
%setup -q -n %{name}
%patch0

# Autoloading this package interferes with SAGE (bz 819705).
sed -i "/^Autoload/s/true/false/" PackageInfo.g 

# Fix link to main GAP bibliography file
sed -i 's,doc/manual,&bib.xml,' doc/manual.tex

%build
export CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
export LDFLAGS="$RPM_LD_FLAGS -Wl,--as-needed"
%configure --with-gaproot=%{_gap_dir}
make %{?_smp_mflags}

# Link to main GAP documentation
ln -s %{_gap_dir}/etc ../../etc
ln -s %{_gap_dir}/doc ../../doc
make -C doc manual
rm -f ../../{doc,etc}

%install
mkdir -p %{buildroot}%{_gap_dir}/pkg/%{name}
cp -a *.g README doc examples htm lib %{buildroot}%{_gap_dir}/pkg/%{name}
rm -f %{buildroot}%{_gap_dir}/pkg/%{name}/doc/*.{bbl,ind,toc}

mkdir -p %{buildroot}%{_bindir}
cp -p bin/*/%{name} %{buildroot}%{_bindir}/%{name}.bin

# The xgap.sh generated during build contains paths in the build root
sed -e "s|@gapdir@|%{_gap_dir}|" \
    -e "s|^GAP_PRG=.*|GAP_PRG=%{_bindir}/gap|" \
    -e "s|^XGAP_PRG=.*|XGAP_PRG=%{_bindir}/%{name}.bin|" \
    -e "s|\$XGAP_DIR/pkg/%{name}/bin/||" \
    -e "s|\$GAP_DIR/bin/\$GAP_PRG|\$GAP_PRG|" \
    %{name}.shi > %{buildroot}%{_bindir}/%{name}
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Install the desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --mode=644 --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# Install the X resource file
mkdir -p %{buildroot}%{_datadir}/X11/app-defaults
cp -p %{SOURCE2} %{buildroot}%{_datadir}/X11/app-defaults

%post
update-desktop-database %{_datadir}/applications &>/dev/null ||:

%postun
update-desktop-database %{_datadir}/applications &>/dev/null ||:

%files
%doc Changelog.*
%docdir %{_gap_dir}/pkg/%{name}/doc
%docdir %{_gap_dir}/pkg/%{name}/examples
%docdir %{_gap_dir}/pkg/%{name}/htm
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/X11/app-defaults/XGap
%{_gap_dir}/pkg/%{name}/

%changelog
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Jerry James <loganjerry@gmail.com> - 4.23-11
- Simplify scriptlets; gap-core now uses rpm file triggers
- Rebuild documentation from source

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 24 2015 Jerry James <loganjerry@gmail.com> - 4.23-9
- Silence scriptlets when uninstalling
- Mark some content as documentation

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 22 2013 Jerry James <loganjerry@gmail.com> - 4.23-5
- Build with large file support

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Jerry James <loganjerry@gmail.com> - 4.23-3
- Rebuild for GAP 4.5

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Jerry James <loganjerry@gmail.com> - 4.23-1
- New upstream release
- Fix bz 819705 issues:
- Fix xgap shell script
- Install X11 resource file
- Turn off autoloading, as that interferes with SAGE

* Mon Apr 23 2012 Jerry James <loganjerry@gmail.com> - 4.22-1
- New upstream release
- Add gap-devel BR to get _gap_dir and _gap_arch_dir macros

* Wed Mar 28 2012 Jerry James <loganjerry@gmail.com> - 4.21-3
- Fix binary permissions

* Fri Feb 17 2012 Jerry James <loganjerry@gmail.com> - 4.21-2
- Add desktop file
- Fix inconsistent macro use

* Mon Jan 23 2012 Jerry James <loganjerry@gmail.com> - 4.21-1
- Initial RPM
