%define modname sysload
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B20_%{modname}.ini

Summary:	PHP Sysload extension
Name:		php-%{modname}
Version:	1.0.0
Release:	5
Group:		Development/PHP
License:	PHP
URL:		http://www.xarg.org/project/php-sysload/
Source0:	http://www.xarg.org/download/sysload-%{version}.tar.gz
Source1:	B20_sysload.ini
BuildRequires:	php-devel >= 3:5.2.0

%description
PHP Sysload is a simple monitoring Extension for PHP backends behind a reverse
proxy server or for other tasks where you have a need to send a specified HTTP
header on overrun.

%prep

%setup -q -n %{modname}-%{version}

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

