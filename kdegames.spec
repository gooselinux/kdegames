Name:    kdegames
Summary: KDE Games
Epoch:   6
Version: 4.3.4
Release: 5%{?dist}

License: GPLv2
URL: http://www.kde.org/
Group:  Amusements/Games
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdegames-%{version}.tar.bz2
# copy from oxygen-icon-theme
Source1: bovo-icons.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# add hi-color icons
Patch1: kdegames-4.3.4-icons.patch

# 4.3 upstream fixes
Patch100: kdegames-4.3.5.patch

Obsoletes: kdegames4 < %{version}-%{release}
Provides:  kdegames4 = %{version}-%{release}

BuildRequires: desktop-file-utils
BuildRequires: ggz-client-libs-devel
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: qca2-devel

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Games for KDE 4, including:
* bomber
* bovo
* kapman
* katomic
* kblackbox
* kblocks
* kbounce
* kbreakout
* kdiamond
* kfourinline
* kgoldrunner
* killbots
* kiriki
* kjumpingcube
* klines
* kmahjongg
* kmines
* knetwalk
* kolf
* kollision
* konquest
* kpat
* kreversi
* ksame
* kshisen
* ksirk
* kspaceduel
* ksquares
* ksudoku
* ktuberling
* kubrick
* lskat

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries

%description libs
%{summary}.

%package devel
Group:    Development/Libraries
Summary:  Header files for compiling KDE 4 game applications
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: kdegames4-devel < %{version}-%{release}
Provides:  kdegames4-devel = %{version}-%{release}
Requires: kdelibs4-devel

%description devel
This package includes the header files you will need to compile
game applications for KDE 4.


%prep
%setup -q -n kdegames-%{version} -a 1

%patch1 -p1 -b .icons

# 4.3 upstream fixes
%patch100 -p1 -b .kde435

%build
# disable ktron/kbattleship because of trademarks issue
sed -i -e "s,macro_optional_add_subdirectory(kbattleship),,g" CMakeLists.txt
sed -i -e "s,macro_optional_add_subdirectory(ktron),,g" CMakeLists.txt
sed -i -e "s,add_subdirectory(kbattleship),,g" doc/CMakeLists.txt
sed -i -e "s,add_subdirectory(ktron),,g" doc/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%check
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
  desktop-file-validate $f
done


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/locolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/locolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/locolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/locolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS README
%{_kde4_bindir}/*
%{_kde4_appsdir}/*
%exclude %{_kde4_appsdir}/cmake/
%{_kde4_configdir}/*
%{_kde4_datadir}/sounds/*.ogg
%{_kde4_datadir}/sounds/kapman/
%{_kde4_datadir}/applications/kde4/*
%{_kde4_datadir}/config.kcfg/*
%{_kde4_docdir}/HTML/en/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/locolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_ggz_configdir}/ggz.modules.d/kdegames

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_kde4_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_kde4_appsdir}/cmake/modules/*
%{_kde4_includedir}/*
%{_kde4_libdir}/lib*.so


%changelog
* Wed Jun 30 2010 Than Ngo <than@redhat.com> - 6:4.3.4-5
- Resolves: bz#587899, menu icon issue

* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 6:4.3.4-4
- rebuilt against qt-4.6.2

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 6:4.3.4-3
- backport 4.3.5 fixes

* Sat Dec 12 2009 Than Ngo <than@redhat.com> - 6:4.3.4-2
- cleanup

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Wed Nov 11 2009 Than Ngo <than@redhat.com> - 4.3.3-2
- rebase kdegames-4.3.3-trademarks.patch

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Sat Sep 12 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.1-4
- also fix ktron.desktop rebranding for non-US locales

* Thu Sep 10 2009 Than Ngo <than@redhat.com> - 4.3.1-3
- drop ktron/kbattleship in RHEL

* Thu Sep 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- adjust trademarks patch to include ktron.desktop

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.0-2
- Conflicts: kdegames3 < 3.5.10-6
- %%check: desktop-file-validate
- use %%?_isa in -libs deps

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Fri Jul 10 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Sat Jul 04 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.95-2
- reenable and rebrand the ship sinking game and the snake duel game (#502359)

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Wed Apr 08 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.2-6
- fix KsirK crash when starting a 2nd local game with Qt 4.5 (#486380)

* Sat Apr 04 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.2-4
- fix KsirK crash when starting a local game with Qt 4.5 (#486380, kde#187235)

* Thu Apr 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-3
- fix ggz scriptlet logic

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Thu Feb 26 2009 Than Ngo <than@redhat.com> - 4.2.0-5
- fix build problem against gcc-4.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-3
- %%description: omit mention of awol kbackgammon

* Sat Jan 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-2
- unowned dirs (#438314)

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Fri Dec 12 2008 <than@redhat.com> 4.1.85-1
- 4.2beta2

* Fri Dec 05 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:4.1.80-4
- rebuild for fixed kde-filesystem (macros.kde4) (get rid of rpaths)

* Thu Dec 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:4.1.80-3
- add missing BR qca2-devel (for ksirk)
- add killbots, kapman and bomber to the description

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> 6:4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast
- drop _default_patch_fuzz 2

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Thu Sep 18 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.1-2
- drop no longer needed devel symlink hacks

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Sat Aug 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-2
- fix Bovo not drawing placed marks (#457944, kde#160419)
- update/fix game list in description

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.rog> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Wed May 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.80-3
- add kbreakout and ksirk to description

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.80-2
- Obsoletes/Provides ksirk

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Thu May 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.72-2
- ggz-config --force , to ensure updates to possibly-changed ggz modules

* Sat May 10 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72
- update description to list new games (kblocks, kdiamond, kollision, kubrick)
- handle new ksquares GGZ module.dsc

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-4
- use new macros.ggz

* Thu Feb 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-3
- Requires(post,preun): ggz-client-libs (for ggz-config)

* Wed Feb 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-2
- omit /etc/ggz.modules (#431726)
- %%post/%%preun: use ggz-config to register ggz modules (#431726)
- -devel: include cmake modules here

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- kde-4.0.1

* Tue Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0.0-1
- kde-4.0.0

* Tue Dec 25 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-3
- move libkdegames.so to %%{_libdir}/kde4/devel and patch search order (#426730)

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-2
- rebuild for changed _kde4_includedir

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.97.0-1
- kde-3.97.0

* Thu Nov 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.2-1
- kde-3.96.2

* Tue Nov 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.1-1
- kde-3.96.1

* Thu Nov 15 2007 Rex Dieter <rdieter[AT]fedoraproject.rog> 3.96.0-1
- kde-3.96.0

* Fri Nov 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.95.2-1
- kdegames-3.95.2

* Wed Nov 07 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.95.0-2
- Obsoletes/Provides: ksudoku (#371131)

* Tue Nov 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.95.0-1
- kdegames-3.95

* Wed Oct 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-3
- -libs conditional (f8+)
- -libs: %%post/%%postun -p /sbin/ldconfig

* Sun Oct 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-2
- fix/update trademarks patch

* Sat Oct 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-1
- kde-3.5.8
- libs subpkg (more multilib friendly)

* Thu Sep 20 2007 Than Ngo <than@redhat.com> 6:3.5.7-4
- bz248343, remove the Tron and Sokoban trademarks, thanks to Kevin Kofler

* Mon Aug 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-3
- License: GPLv2, libs/devel License: LGPLv2
- (Build)Requires: kdelibs3(-devel)
- Provides: kdegames3(-devel)

* Mon Jun 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-1
- 3.5.7

* Tue Apr 24 2007 Than Ngo <than@redhat.com> - 6:3.5.6-3.fc7
- cleanup

* Tue Mar 06 2007 Than Ngo <than@redhat.com> - 6:3.5.6-2.fc7
- cleanup

* Wed Feb 07 2007 Than Ngo <than@redhat.com> 6:3.5.6-1.fc7
- 3.5.6

* Thu Aug 10 2006 Than Ngo <than@redhat.com> 6:3.5.4-1
- rebuild

* Mon Jul 24 2006 Than Ngo <than@redhat.com> 6:3.5.4-0.pre1
- prerelease of 3.5.4 (from the first-cut tag)

* Thu Jul 13 2006 Dennis Gregorovic <dgregor@redhat.com> - 6:3.5.3-2.2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6:3.5.3-2.1
- rebuild

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 6:3.5.3-2
- move only *.so symlinks to -devel subpackage
- enable --enable-new-ldflags since ld bug fixed

* Fri Jun 02 2006 Than Ngo <than@redhat.com> 6:3.5.3-1
- update to 3.5.3

* Tue Apr 04 2006 Than Ngo <than@redhat.com> 6:3.5.2-1
- update to 3.5.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6:3.5.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6:3.5.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Than Ngo <than@redhat.com> 6:3.5.1-1
- 3.5.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec 05 2005 Than Ngo <than@redhat.com> 6:3.5.0-1
- 3.5

* Tue Nov 15 2005 Than Ngo <than@redhat.com> 6:3.4.92-2
- apply patch to fix build problem with gcc4

* Tue Oct 25 2005 Than Ngo <than@redhat.com> 6:3.4.92-1
- update to 3.5 Beta2

* Wed Oct 05 2005 Than Ngo <than@redhat.com> 6:3.4.91-1
- update to 3.5 Beta1

* Mon Aug 08 2005 Than Ngo <than@redhat.com> 6:3.4.2-1
- update to 3.4.2

* Tue Jun 28 2005 Than Ngo <than@redhat.com> 6:3.4.1-1
- 3.4.1

* Fri Mar 18 2005 Than Ngo <than@redhat.com> 6:3.4.0-1
- 3.4.0

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 6:3.4.0-0.rc1.2
- rebuilt against gcc-4.0.0-0.31

* Sat Feb 26 2005 Than Ngo <than@redhat.com> 6:3.4.0-0.rc1.1
- KDE-3.4.0 rc1

* Sun Feb 20 2005 Than Ngo <than@redhat.com> 6:3.3.92-0.1
- KDE-3.4 beta2

* Mon Jan 31 2005 Than Ngo <than@redhat.com> 3.3.2-0.2
- fix a bug in changeBackside #146609

* Fri Dec 03 2004 Than Ngo <than@redhat.com> 6:3.3.2-0.1
- update to 3.3.2

* Mon Oct 18 2004 Than Ngo <than@redhat.com> 6:3.3.1-2
- add missing klickety icons #135614

* Wed Oct 13 2004 Than Ngo <than@redhat.com> 6:3.3.1-1
- update to 3.3.1

* Fri Oct 08 2004 Than Ngo <than@redhat.com> 6:3.3.0-2
- fix buildrequire on automake
- disable ksokoban

* Mon Aug 23 2004 Than Ngo <than@redhat.com> 3.3.0-1
- update to 3.3.0 release

* Tue Aug 10 2004 Than Ngo <than@redhat.com> 3.3.0-0.1.rc2
- update to 3.3.0 rc2

* Tue Aug 10 2004 Than Ngo <than@redhat.com> 3.3.0-0.1.rc1
- update to 3.3.0 rc1

* Wed Aug 04 2004 Than Ngo <than@redhat.com> 3.2.92-1
- update to 3.3 Beta 2

* Sat Jun 19 2004 Than Ngo <than@redhat.com> 3.2.3-2
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 02 2004 Than Ngo <than@redhat.com> 6:3.2.3-0.1
- update to 3.2.3

* Wed Apr 14 2004 Than Ngo <than@redhat.com> 6:3.2.2-1
- update to 3.2.2

* Thu Apr 08 2004 Than Ngo <than@redhat.com> 6:3.2.1-4
- fix dependency bug again, bug #120399

* Wed Apr 07 2004 Than Ngo <than@redhat.com> 3.2.1-3
- add missing icons, bug #118281

* Mon Mar 22 2004 Than Ngo <than@redhat.com> 6:3.2.1-2
- fixed klickety crash, bug #118280

* Sun Mar 07 2004 Than Ngo <than@redhat.com> 6:3.2.1-1
- 3.2.1 release

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Than Ngo <than@redhat.com> 6:3.2.0-1.4
- gcc 3.4 build problem

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 05 2004 Than Ngo <than@redhat.com> 6:3.2.0-0.3
- 3.2.0 release
- built against qt 3.3.0
- add Prereq /sbin/ldconfig

* Mon Jan 19 2004 Than Ngo <than@redhat.com> 6:3.1.95-0.1
- KDE 3.2 RC1

* Mon Dec 01 2003 Than Ngo <than@redhat.com> 6:3.1.94-0.1
- KDE 3.2 Beta2

* Thu Nov 27 2003 Than Ngo <than@redhat.com> 6:3.1.93-0.2
- get rid of rpath

* Tue Nov 11 2003 Than Ngo <than@redhat.com> 6:3.1.93-0.1
- KDE 3.2 Beta1
- cleanup specfile
- remove some patch files, which are included in new upstream

* Mon Oct 13 2003 Than Ngo <than@redhat.com> 6:3.1.4-2
- backport from CVS to fix atlantikdesigner crashed on startup
- fix miscompiled code, (bug #106198, #106888)

* Tue Sep 30 2003 Than Ngo <than@redhat.com> 6:3.1.4-1
- 3.1.4

* Tue Aug 12 2003 Than Ngo <than@redhat.com> 6:3.1.3-3
- fix build problem with gcc 3.3

* Wed Aug 06 2003 Than Ngo <than@redhat.com> 6:3.1.3-2
- rebuilt

* Sun Aug 03 2003 Than Ngo <than@redhat.com> 6:3.1.3-1
- 3.1.3

* Mon Jul  7 2003 Than Ngo <than@redhat.com> 3.1.2-5
- fix a bug in katomic, which caused icons are invisible (bug #89628)

* Thu Jun 26 2003 Than Ngo <than@redhat.com> 3.1.2-4
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 19 2003 Than Ngo <than@redhat.com> 3.1.2-0.9x.2
- 3.1.2

* Thu May  8 2003 Than Ngo <than@redhat.com> 3.1.1-3
- fix command line option (bug #90082)

* Wed Apr 30 2003 Elliot Lee <sopwith@redhat.com> 3.1.1-2
- headusage patch (from kdebindings) for ppc64

* Wed Mar 19 2003 Than Ngo <than@redhat.com> 3.1.1-1
- 3.1.1

* Thu Feb 27 2003 Than Ngo <than@redhat.com> 3.1-5
- add requires kdebase (#84679)

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Fri Feb 21 2003 Than Ngo <than@redhat.com> 3.1-3
- get rid of gcc path from dependency_libs

* Thu Feb 13 2003 Than Ngo <than@redhat.com> 3.1-2
- rebuild against new arts

* Tue Jan 28 2003 Than Ngo <than@redhat.com> 3.1-1
- 3.1 final

* Mon Jan 27 2003 Than Ngo <than@redhat.com> 3.1-0.6
- add missing plugins
- cleanup specfile

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 6:3.1-0.5
- rebuild

* Tue Jan 14 2003 Thomas Woerner <twoerner@redhat.com> 3.1-0.3
- fixed missing file

* Tue Jan 14 2003 Thomas Woerner <twoerner@redhat.com> 3.1-0.3
- rc6
- removed size_t check
- excluded ia64

* Fri Nov 29 2002 Than Ngo <than@redhat.com> 3.1-0.2
- desktop file issues

* Wed Nov 27 2002 Than Ngo <than@redhat.com> 3.1-0.1
- update to 3.1 rc4

* Sun Nov 10 2002 Than Ngo <than@redhat.com> 3.0.5-1
- update to 3.0.5

* Tue Oct 15 2002 Than Ngo <than@redhat.com> 3.0.4-1
- 3.0.4

* Fri Sep 13 2002 Than Ngo <than@redhat.com> 3.0.3-3.1
- Fixed to build on x86_64

* Thu Aug 29 2002 Preston Brown <pbrown@redhat.com>
- remove kbattleship and ktron (#72763)

* Fri Aug 23 2002 Than Ngo <than@redhat.com> 3.0.3-2
- desktop files issues (bug #72408)

* Mon Aug 12 2002 Than Ngo <than@redhat.com> 3.0.3-1
- 3.0.3
- desktop files issues

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 3.0.2-2
- build using gcc-3.2-0.1

* Tue Jul 09 2002 Than Ngo <than@redhat.com> 3.0.2-1
- 3.0.2
- use desktop-file-install

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.1-1
- 3.0.1

* Tue Apr 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-2
- Change sonames

* Wed Mar 27 2002 Than Ngo <than@redhat.com> 3.0.0-1
- final



