Name:           xgap
Version:        4.22
Release:        1%{?dist}
Summary:        GUI for GAP

License:        GPLv2+
URL:            http://www-groups.mcs.st-and.ac.uk/~neunhoef/Computer/Software/Gap/%{name}4.html
Source0:        http://www-groups.mcs.st-and.ac.uk/~neunhoef/Computer/Software/Gap/%{name}4/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
# This patch quiets some compiler warnings.
Patch0:         %{name}-warning.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gap-devel
BuildRequires:  libXaw-devel
Requires:       gap-core

%description
A X Windows GUI for GAP.

%prep
%setup -q -n %{name}
%patch0

%build
export LDFLAGS="$RPM_LD_FLAGS -Wl,--as-needed"
%configure --with-gaproot=%{_gap_arch_dir}
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_gap_dir}/pkg/%{name}
cp -a *.g README doc examples htm lib $RPM_BUILD_ROOT%{_gap_dir}/pkg/%{name}

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p bin/*/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}.bin

# The xgap.sh generated during build contains paths in the build root
sed -e "s|@gapdir@|%{_gap_dir}|" \
    -e "s|^XGAP_PRG=.*|XGAP_PRG=%{_bindir}/%{name}.bin|" \
    -e "s|\$XGAP_DIR/pkg/%{name}/bin/||" \
    -e "s|\$GAP_DIR/bin/\$GAP_PRG|\$GAP_PRG|" \
    %{name}.shi > $RPM_BUILD_ROOT%{_bindir}/%{name}
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/%{name}

# Install the desktop file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --mode=644 --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}

%posttrans -p %{_bindir}/update-gap-workspace

%post
update-desktop-database %{_datadir}/applications &>/dev/null ||:

%postun
%{_bindir}/update-gap-workspace
update-desktop-database %{_datadir}/applications &>/dev/null ||:

%files
%doc Changelog.*
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_gap_dir}/pkg/%{name}

%changelog
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
