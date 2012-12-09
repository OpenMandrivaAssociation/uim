%define version   1.7.0
%define release   %mkrel 4

%define anthy_version      6620
%define m17n_lib_version   1.3.4

%define uim_major 7
%define libname_orig lib%{name}
%define libname %mklibname %{name} %uim_major
%define develname %mklibname -d %{name}

%define custom_major 2
%define libcustom_orig libuim-custom
%define libcustom %mklibname uim-custom %custom_major

%define gcroots_major 0
%define libgcroots_orig libgcroots
%define libgcroots %mklibname gcroots %gcroots_major

%define scm_major 0
%define libscm %mklibname uim-scm %scm_major

Name:      uim
Summary:   Multilingual input method library 
Version:   %{version}
Release:   %{release}
Group:     System/Internationalization
# uim itself is licensed under BSD
# scm/py.scm, helper/eggtrayicon.[ch], qt/pref-kseparator.{cpp,h}
#   and qt/chardict/chardict-kseparator.{cpp,h} is licensed under LGPLv2+
# pixmaps/*.{svg,png} is licensed under BSD or LGPLv2
License:   BSD and LGPLv2+ and (BSD or LGPLv2)
URL:       http://code.google.com/p/uim/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:   http://uim.googlecode.com/files/%name-%version.tar.bz2
Requires:        %{libname} = %{version}
Requires:        uim-gtk
Requires:        anthy >= %{anthy_version}
Requires:        m17n-lib >= %{m17n_lib_version}
Requires:        skkdic
Requires(post):   %_bindir/gtk-query-immodules-2.0
Requires(postun): %_bindir/gtk-query-immodules-2.0
Conflicts:       gtk+2.0 < 2.4.4-2mdk
Obsoletes:       uim-anthy, uim-m17nlib, uim-prime, uim-skk
Provides:        uim-anthy, uim-m17nlib, uim-prime, uim-skk
BuildRequires:   gtk+2-devel >= 2.4.0
BuildRequires:   gtk+3-devel
BuildRequires:   libgnome2-devel 
BuildRequires:   pkgconfig(libgnomeui-2.0)
BuildRequires:   gnome-panel-devel
BuildRequires:	 pkgconfig(libglade-2.0)
BuildRequires:   m17n-lib-devel >= %{m17n_lib_version}
BuildRequires:   m17n-db
BuildRequires:   anthy-devel >= %{anthy_version}
BuildRequires:   intltool
BuildRequires:   pkgconfig(ncurses)
BuildRequires:   automake
BuildRequires:   qt4-devel
BuildRequires:	 ed
BuildRequires:	 libtool

%description
Uim is a multilingual input method library. Uim's project goal is 
to provide secure and useful input method for all languages.

%package   gtk
Summary:   GNOME helper for uim
Group:     System/Internationalization
Requires:  %{name} = %{version}
Requires:  gtk+2
Provides:  uim-applet-gtk
Provides:  uim-applet = %{version}

%description gtk
GNOME helper for uim. It contains some apps like toolbar, 
system tray, applet, candidate window for Uim library.

%package   gtk3
Summary:   GNOME3 helper for uim
Group:     System/Internationalization
Requires:  %{name} = %{version}
Requires:  gtk+3
Provides:  uim-applet-gtk3
Provides:  uim-applet = %{version}

%description gtk3
GNOME3 helper for uim. It contains some apps like toolbar,
system tray, applet, candidate window for Uim library.

%package   qt4immodule
Summary:   A plugin for using UIM on qt4-immodule
Group:     System/Internationalization
Requires:  %{name} = %{version}
Requires:  qt4-common

%description qt4immodule
A plugin for using UIM on qt4-immodule.

%package    base
Summary:    Misc files needed by UIM library
Group:      System/Internationalization
Conflicts:  %{mklibname uim 1}
Conflicts:  %{mklibname uim 5} < 1.4.0-1mdv

%description base
Misc files needed by UIM library.

%package -n %{libname}
Summary:    UIM library
Group:      System/Internationalization
Provides:   %{libname_orig} = %{version}-%{release}
Requires:   uim-base
Conflicts:  %{mklibname uim 1}

%description -n %{libname}
UIM library.

%package -n %{develname}
Summary:    Headers of uim for development
Group:      Development/C
Requires:   %{libname} = %{version}
Provides:   %{name}-devel = %{version}-%{release}
Provides:   %{libname_orig}-devel = %{version}-%{release}
Obsoletes:  %mklibname -d uim 5

%description -n %{develname}
Headers of %{name} for development.

%package -n %{libcustom}
Summary:    Custom library for UIM
Group:      System/Internationalization
Provides:   %{libcustom_orig} = %{version}-%{release}
Conflicts:  %{mklibname uim 1}

%description -n %{libcustom}
Custom library for UIM.

%package -n %{libgcroots}
Summary:    Gcroots library for UIM
Group:      System/Internationalization
Provides:   %{libgcroots_orig} = %{version}-%{release}
Conflicts:  %{mklibname uim 1}

%description -n %{libgcroots}
ohis library abstracts architecture-dependent part of garbage collector
roots acquisition such as register windows of SPARC and register stack
backing store of IA-64. 

With this library, one can easily write his own garbage collector for
small footprint, some application-specific optimizations, just learning or
testing experimental ideas.

%package -n %{libscm}
Summary:    Scm library for UIM
Group:      System/Internationalization

%description -n %{libscm}
Scm library for UIM.

%prep
%setup -qn %{name}-%{version}

%build
export QMAKE4=%{qt4bin}/qmake
%configure2_5x \
   --disable-static \
   --without-anthy \
   --with-anthy-utf8 \
   --with-m17nlib \
   --without-canna \
   --without-prime \
   --without-scim \
   --without-eb \
   --with-qt4-immodule \
   --enable-dict \
   --disable-warnings-into-error

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unnecessary files
find %{buildroot} -name *.la | xargs rm

# remove docs for sigscheme (they should be installed by %doc)
rm -rf %{buildroot}%{_datadir}/doc/sigscheme

%find_lang %{name}
#%find_lang uim-chardict-qt

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README
%doc sigscheme/doc/*
%{_bindir}/uim-el*-agent
%{_bindir}/uim-fep*
%{_bindir}/uim-help
%{_bindir}/uim-module-manager
%{_bindir}/uim-sh
%{_bindir}/uim-xim
%{_bindir}/uim-m17nlib-relink-icons
%{_datadir}/applications/*
%{_datadir}/emacs/site-lisp/uim-el/*.el
%{_datadir}/dbus-1/services/org.gnome.panel.applet.UimAppletFactory.service
%{_mandir}/man1/*
%{_datadir}/uim

%files gtk
%defattr(-,root,root)
%doc COPYING
%{_bindir}/uim-input-pad-ja
%{_bindir}/uim-dict-gtk
%{_bindir}/uim-im-switcher-gtk
%{_bindir}/uim-pref-gtk
%{_bindir}/uim-toolbar-gtk
%{_bindir}/uim-toolbar-gtk-systray
%{_libexecdir}/uim-candwin-gtk
%{_libexecdir}/uim-candwin-tbl-gtk
%{_libdir}/gtk-2.0/*/immodules/*.so

%files gtk3
%defattr(-,root,root)
%{_bindir}/uim-dict-gtk3
%{_bindir}/uim-im-switcher-gtk3
%{_bindir}/uim-input-pad-ja-gtk3
%{_bindir}/uim-pref-gtk3
%{_bindir}/uim-toolbar-gtk3
%{_bindir}/uim-toolbar-gtk3-systray
%{_libdir}/gtk-3.0/*/immodules/im-uim.so
%{_libexecdir}/uim-candwin-gtk3
%{_libexecdir}/uim-candwin-tbl-gtk3

%files qt4immodule
%doc COPYING
%{qt4plugins}/inputmethods/*.so

%files base
%defattr(-,root,root)
%{_libexecdir}/uim-helper-server
#%{_libdir}/bonobo/servers/*.server
%{_datadir}/gnome-panel/4.0/applets/UimApplet.panel-applet
%{_libexecdir}/uim-toolbar-applet*
%{_libdir}/uim/plugin/libuim-*.so

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libuim.so.%{uim_major}*

%files -n %{libgcroots}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libgcroots.so.%{gcroots_major}*

%files -n %{libcustom}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libuim-custom.so.%{custom_major}*

%files -n %{libscm}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libuim-scm.so.%{scm_major}*

%files -n %{develname}
%defattr(-,root,root)
%doc COPYING
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue May 17 2011 Funda Wang <fwang@mandriva.org> 1.7.0-2mdv2011.0
+ Revision: 675887
- more fix
- fix requires

* Tue May 17 2011 Funda Wang <fwang@mandriva.org> 1.7.0-1
+ Revision: 675855
- new version 1.7.0

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-2
+ Revision: 670740
- mass rebuild

* Fri Jan 21 2011 Funda Wang <fwang@mandriva.org> 1.6.1-1
+ Revision: 631951
- update to new version 1.6.1

* Sat Aug 21 2010 Funda Wang <fwang@mandriva.org> 1.6.0-1mdv2011.0
+ Revision: 571675
- 1.6.0 final

* Mon Aug 09 2010 Funda Wang <fwang@mandriva.org> 1.6.0-0.beta.1mdv2011.0
+ Revision: 567854
- 1.6.0 beta
  drop all old patches
  completely drop qt3 build

* Tue Nov 24 2009 Funda Wang <fwang@mandriva.org> 1.5.7-1mdv2010.1
+ Revision: 469421
- fix linkage of qt4 immodule
- new version 1.5.7

* Tue Aug 11 2009 Funda Wang <fwang@mandriva.org> 1.5.6-1mdv2010.0
+ Revision: 414795
- New version 1.5.6

* Tue Feb 10 2009 Funda Wang <fwang@mandriva.org> 1.5.5-2.svn5782.1mdv2009.1
+ Revision: 339267
- BR glade
- Update to svn
- use system libtool

  + Helio Chissini de Castro <helio@mandriva.com>
    - Removed qt3 compilation. ne libtool is breaking compilation

* Thu Jan 22 2009 Funda Wang <fwang@mandriva.org> 1.5.5-1mdv2009.1
+ Revision: 332414
- 1.5.5

* Sat Nov 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.4-3mdv2009.1
+ Revision: 301015
- rebuilt against new libxcb

  + Funda Wang <fwang@mandriva.org>
    - more strict license
    - BSD only license

* Thu Oct 30 2008 Funda Wang <fwang@mandriva.org> 1.5.4-2mdv2009.1
+ Revision: 298696
- use pkgconfig to detect qt3

* Sat Oct 25 2008 Funda Wang <fwang@mandriva.org> 1.5.4-1mdv2009.1
+ Revision: 297230
- bye bye, qt3 stuffs
- New version 1.5.4

* Sun Sep 07 2008 Funda Wang <fwang@mandriva.org> 1.5.3-1mdv2009.0
+ Revision: 282105
- New version 1.5.3

* Tue Aug 26 2008 Funda Wang <fwang@mandriva.org> 1.5.2-2mdv2009.0
+ Revision: 276106
- add m17n-db as BR

* Mon Aug 04 2008 Funda Wang <fwang@mandriva.org> 1.5.2-1mdv2009.0
+ Revision: 263382
- hard code qt3 plugin dir
- remove *.la
- only move files when needed
- no need to move .so anymore
- BR anthy
- new version 1.5.2

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun May 18 2008 Funda Wang <fwang@mandriva.org> 1.5.1-2mdv2009.0
+ Revision: 208607
- fix summary
- fix dir of qt4plugins
- enalbe qt4 build

* Sat May 17 2008 Funda Wang <fwang@mandriva.org> 1.5.1-1mdv2009.0
+ Revision: 208337
- New version 1.5.1

* Wed May 07 2008 Funda Wang <fwang@mandriva.org> 1.5.0-2mdv2009.0
+ Revision: 202888
- fix requires of devel package

* Wed May 07 2008 Funda Wang <fwang@mandriva.org> 1.5.0-1mdv2009.0
+ Revision: 202776
- New version 1.5.0

* Sun Mar 09 2008 Funda Wang <fwang@mandriva.org> 1.4.2-1mdv2009.0
+ Revision: 182404
- use configure2_5x
- New version 1.4.2

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.4.1-7mdv2008.1
+ Revision: 171152
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Sep 21 2007 Pixel <pixel@mandriva.com> 1.4.1-6mdv2008.0
+ Revision: 91744
- fix subfile-not-in-%%lang issue: LC_MESSAGES/uim-chardict-qt.mo must be handled
  by find_lang, and is better in uim-qt

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.1-5mdv2008.0
+ Revision: 90342
- rebuild

* Mon Aug 27 2007 Pixel <pixel@mandriva.com> 1.4.1-4mdv2008.0
+ Revision: 71846
- rebuild for fixed find-lang.pl

* Thu Aug 23 2007 Funda Wang <fwang@mandriva.org> 1.4.1-3mdv2008.0
+ Revision: 69839
- Obsoletes quiminputcontextplugin

  + Thierry Vignaud <tv@mandriva.org>
    - replace %%{_datadir}/man by %%{_mandir}!

* Sat Jul 07 2007 Funda Wang <fwang@mandriva.org> 1.4.1-2mdv2008.0
+ Revision: 49340
- New develpackage policy
- new homepage URL

* Mon Apr 23 2007 Funda Wang <fwang@mandriva.org> 1.4.1-1mdv2008.0
+ Revision: 17161
- New upstream version 1.4.1
- use qt3* macros rather than lib-magic.


* Tue Feb 27 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.4.0-2mdv2007.0
+ Revision: 126599
- fix upgrade (#28959):
  o split all libraries in their own packages
  o split non versionated stuff needed by library users in uim-base
- ensure one cannot build a wrong package when major is bumped

* Tue Feb 20 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.4.0-1mdv2007.1
+ Revision: 123079
- kill bogus provides & obsoletes
- add kdelibs-devel to buildrequires (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)
- new release (utumi)
- new release

* Wed Oct 18 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.1-3.svn3879.1mdv2007.0
+ Revision: 66002
- latest snapshot (fix Bugzilla #24472) (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)

* Thu Aug 17 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.1-1mdv2007.0
+ Revision: 56451
- new release (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)

* Fri Aug 11 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.0-1mdv2007.0
+ Revision: 55507
- new release (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)

* Fri Aug 04 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.0-0.2mdv2007.0
+ Revision: 43071
- new release (1.2.0-beta) (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

  + Helio Chissini de Castro <helio@mandriva.com>
    - Uploading package ./uim

* Tue May 10 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.6-7.svn0837.1mdk
- remove patch0,1 (merged upstream)
- latest snapshot

* Wed Mar 30 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.6-7.svn0811.1mdk
- add skkserv support (patch0,1)
- latest snapshot
- update source2,3,4 for prime-1.0.0.1
- add some comments for new packagers
- modify buildrequires

* Wed Mar 30 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.6-6mdk
- ensure either qt or gtk is installed with uim so that setup panel, helper
  toolbar etc... works (#14947)

* Tue Mar 22 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.6-5mdk
- fix upgrade (uim-applet is dead)

* Sat Mar 12 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.4.6-4mdk
- add BuildRequires: libanthy-devel, libncurses-devel

* Thu Mar 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.4.6-3mdk
- fix build on lib64 platforms
- fix buildrequires (again, titi watch out!)

* Wed Mar 02 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.6-2mdk
- update source2 for prime-0.9.4-rc1
- add obsoletes prime <= 0.9.4-0.alpha3.1mdk
- fix requires

* Mon Feb 28 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.6-1mdk
- new release (uim-0.4.6-final)
- replace prime.scm (source2)
- add uim-qtimmodule (default = disabled)

* Wed Feb 23 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.6-1.beta2.3mdk
- add source1 uim-update-imlist
- (uim doesn't update im engine list automatically)

* Tue Feb 22 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.6-1.beta2.2mdk
- split in several subpackages (uim-anthy, uim-m17n, uim-prime, uim-skk)

* Mon Feb 21 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.6-1.beta2.1mdk
- fix requires (rpmlint)
- new release (security fix) (UTUMI Hirosi <utuhiro78@yahoo.co.jp>)

* Fri Feb 18 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.6-0.svn0667.2mdk
- change buildrequires prime-dict to libprime
- add buildrequires kdelibs-devel (for uim-qt)
- add buildrequires libeb-devel (for electronic book support)
- remove "post qt" and "postun qt". uim-qt doesn't have libraries.

* Thu Feb 17 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.6-0.svn0667.1mdk
- fix buildrequires
- UTUMI Hirosi <utuhiro78@yahoo.co.jp>:
  o latest snapshot (uim-0.4.6-alpha)
  o spec cleanup
  o add uim-gtk, uim-qt
  o uim-applet is merged into libuim0

* Wed Feb 16 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.4.5-5.20050113.3mdk
- fix requires

* Mon Jan 31 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.5-5.20050113.2mdk
- kill wrong buildrequires

* Thu Jan 13 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.5-5.20050113.1mdk
- latest snapshot
- add "Prereq:  gtk-query-immodules-2.0"
- remove prime.scm (It should be installed by prime. prime-x.y.z needs prime-x.y.z.scm.)

* Thu Dec 30 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.5-4mdk
- add patch0, patch1
- remove "--with-canna", "--enable-dict" (experimental)

* Sun Nov 14 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.5-3mdk
- new release
- add BuildRequires: canna-devel (another Japanese translation engine)
- add uim-dict (a tool for managing dictionary)

* Fri Oct 22 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.4.3-2mdk
- mklibname fixes
- no XFCE4 applet generated

* Sun Sep 05 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.3-1mdk
- new release

* Sun Aug 01 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.2.1-1mdk
- new release

* Fri Jul 30 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.2-1mdk
- new release
- fix build from official releases
- fix uim-fep build

* Fri Jul 30 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.1-3.svn1041.1mdk
- svn 1041

* Thu Jul 29 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.4.1-3.svn1029.1mdk
- svn 1029

* Thu Jul 29 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.1-2.svn0997.2mdk
- biarch support

* Wed Jul 21 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.1-2.svn0997.1mdk
- do not package useless files in doc
- UTUMI Hirosi <utuhiro78@yahoo.co.jp>:
  o new release
  o svn 997

* Wed Jun 30 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.3.9-2.svn912.2mdk
- svn 912
- (source) svn checkout http://freedesktop.org:8080/svn/uim/trunk

* Tue Jun 15 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.9-1mdk
- new release
- remove patch 0 (merged upstream)

* Mon Jun 14 2004 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.3.8-4mdk
- svn 899
- add patch0 (made by James - it will be merged)

* Wed Jun 09 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.8-3mdk
- rebuild for new g++

* Fri May 28 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.8-2mdk
- add m17n support (UTUMI Hirosi)

* Fri May 28 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.8-1mdk
- new release
- do not overwrite config files on update

* Fri Apr 09 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.4.2-2mdk
- fix duplicated buildrequires

* Thu Apr 08 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.4.2-1mdk
- new release
- fix buildrequires
- include download url in source0
- change summary and description (UTUMI Hirosi, by authors request)
- link with gtk+2.4.0 (because of new immodules path)

* Fri Apr 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.3-1mdk
- new release
- drop patches 0 and 1 (merged upstream)

* Fri Mar 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.2.8-5mdk
- Patch1: fix crash in nautilus

* Mon Mar 08 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.8-4mdk
- patch 0: fix numeric pad in KDE applications (transmitted by UTUMI Hirosi)

