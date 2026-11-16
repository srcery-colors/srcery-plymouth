Name:           plymouth-theme-srcery
Version:        1.0.0
Release:        1%{?dist}
Summary:        Srcery colorscheme boot splash theme for Plymouth

License:        MIT AND CC-BY-4.0
URL:            https://github.com/srcery-colors/srcery-plymouth
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       plymouth
Requires:       plymouth-plugin-script
Requires(postun): plymouth-scripts

%description
Srcery is a dark, contrast-forward colorscheme. This package installs a
Plymouth boot splash theme that renders the Srcery eye glyph, a progress
bar, and password/question dialogs in the Srcery palette.

Installing this package does not switch your active Plymouth theme. Run
`plymouth-set-default-theme -R srcery` afterwards (see README.md).

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to compile: this package ships static Plymouth theme data only.

%install
install -d %{buildroot}%{_datadir}/plymouth/themes/srcery
install -p -m 0644 srcery/srcery.plymouth %{buildroot}%{_datadir}/plymouth/themes/srcery/
install -p -m 0644 srcery/srcery.script %{buildroot}%{_datadir}/plymouth/themes/srcery/
install -p -m 0644 srcery/*.png %{buildroot}%{_datadir}/plymouth/themes/srcery/

%postun
if [ "$1" -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme 2>/dev/null)" == "srcery" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset || :
    fi
fi

%files
%license LICENSE
%doc README.md ATTRIBUTION.md
%dir %{_datadir}/plymouth/themes/srcery
%{_datadir}/plymouth/themes/srcery/srcery.plymouth
%{_datadir}/plymouth/themes/srcery/srcery.script
%{_datadir}/plymouth/themes/srcery/*.png

%changelog
* Tue Jul 21 2026 Birger Johan Nordølum <me@mindtooth.no> - 1.0.0-1
- Initial COPR packaging: noarch spec, no forced theme activation on
  install, %%postun-only cleanup guarded by erase ($1 == 0) and
  currently-active-theme checks (docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/).
