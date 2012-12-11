%define modname idna
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B19_%{modname}.ini

Summary:	PHP IDNA Extension
Name:		php-%{modname}
Version:	1.0.0
Release:	5
Group:		Development/PHP
License:	PHP
URL:		http://www.xarg.org/project/php-idna/
Source0:	http://www.xarg.org/download/idna-%{version}.tar.gz
Source1:	B19_idna.ini
Patch0:		idna-1.0.0-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	idn-devel

%description
This extension provides a PHP implementation of the Internationalized Domain
Name Applications (IDNA) standard.

%prep

%setup -q -n %{modname}-%{version}
%patch0 -p0

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%files
%doc CREDITS
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5
+ Revision: 797081
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4
+ Revision: 761258
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3
+ Revision: 696434
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2
+ Revision: 695409
- rebuilt for php-5.3.7

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Clean spec file for rpm5

* Fri May 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1
+ Revision: 676257
- import php-idna


* Fri May 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2010.2
- initial Mandriva package
