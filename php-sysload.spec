%define modname sysload
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B20_%{modname}.ini

Summary:	PHP Sysload extension
Name:		php-%{modname}
Version:	1.0.0
Release:	6
Group:		Development/PHP
License:	PHP
URL:		https://www.xarg.org/project/php-sysload/
Source0:	http://www.xarg.org/download/sysload-%{version}.tar.gz
Source1:	B20_sysload.ini
Patch0:		sysload-1.0.0-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0

%description
PHP Sysload is a simple monitoring Extension for PHP backends behind a reverse
proxy server or for other tasks where you have a need to send a specified HTTP
header on overrun.

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
%doc CREDIT
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5
+ Revision: 797005
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4
+ Revision: 761333
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3
+ Revision: 696478
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2
+ Revision: 695473
- rebuilt for php-5.3.7

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Clean spec file layout

* Fri May 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1
+ Revision: 676259
- import php-sysload


* Fri May 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2010.2
- initial Mandriva package
