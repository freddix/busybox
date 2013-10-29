Summary:	Set of Unix utilities for rescue and embedded system
Name:		busybox
Version:	1.21.1
Release:	4
License:	GPL
Group:		Applications
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	795394f83903b5eec6567d51eebb417e
Source1:	%{name}-live.config
Source2:	%{name}-huge.config
Patch0:		%{name}-include.patch
URL:		http://www.busybox.net/
BuildRequires:	perl-tools-pod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BusyBox combines tiny versions of many common UNIX utilities into a
single small executable. It provides minimalist replacements for most
of the utilities you usually find in fileutils, shellutils, findutils,
textutils, grep, gzip, tar, etc. BusyBox provides a fairly complete
POSIX environment for any small or embedded system. The utilities in
BusyBox generally have fewer options than their full-featured GNU
cousins; however, the options that are included provide the expected
functionality and behave very much like their GNU counterparts.

%package live
Summary:	Basic BusyBox version
Group:		Applications

%description live
BusyBox version with essential features set for use with live media.

%prep
%setup -q
%patch0 -p1

%{__sed} -i 's|#!/bin/sh|#!/usr/bin/bash|' scripts/gen_build_files.sh

%build
install -d built
install %{SOURCE1} .config

# live
%{__make} oldconfig
%{__make} \
	CC="%{__cc}"		\
	LDFLAGS="%{rpmldflags}"	\
	V=1
%{__mv} busybox_unstripped built/busybox.live
%{__make} distclean

# huge
install %{SOURCE2} .config
%{__make} oldconfig
%{__make} -j1 \
	CC="%{__cc}"		\
	LDFLAGS="%{rpmldflags}"	\
	V=1
%{__make} busybox.links docs/busybox.1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir}/busybox}

install built/busybox.live $RPM_BUILD_ROOT%{_bindir}

install busybox_unstripped $RPM_BUILD_ROOT%{_bindir}/busybox
ln -sf %{_bindir}/busybox $RPM_BUILD_ROOT%{_bindir}/vi
install busybox.links $RPM_BUILD_ROOT%{_libdir}/busybox
install docs/busybox.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README .config
%attr(755,root,root) %{_bindir}/vi
%attr(755,root,root) %{_bindir}/busybox
%dir %{_libdir}/busybox
%attr(755,root,root) %{_libdir}/busybox/busybox.links
%{_mandir}/man1/busybox.1*

%files live
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/busybox.live

