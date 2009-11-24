%define version   1.5.7
%define release   %mkrel 1

%define anthy_version      6620
%define m17n_lib_version   1.3.4

%define uim_major 6
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

%define with_qt3 0
%{?_with_qt3: %{expand: %%global with_qt3 1}}

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
Patch0:    uim-1.5.4-pkgconfig-qt3.patch
Patch1:    uim-1.5.5-fix-str-fmt.patch
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
BuildRequires:   libgnome2-devel gnomeui2-devel
BuildRequires:   gnome-panel-devel
BuildRequires:	 libglade2-devel
BuildRequires:   m17n-lib-devel >= %{m17n_lib_version}
BuildRequires:   m17n-db
BuildRequires:   anthy-devel >= %{anthy_version}
BuildRequires:   intltool
BuildRequires:   libncurses-devel, automake
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
Requires:  gtk2
Provides:  uim-applet-gtk
Provides:  uim-applet = %{version}

%description gtk
GNOME helper for uim. It contains some apps like toolbar, 
system tray, applet, candidate window for Uim library.

%if %{with_qt3}
%package   qt
Summary:   KDE helper for uim
Group:     System/Internationalization
Requires:  %{name} = %{version}
Requires:  qt3 > 3.3.4-9mdk
BuildRequires: qt3-devel
Provides:  uim-applet = %{version}

%description qt
KDE helper for uim. It contains some apps like toolbar,
system tray, applet, candidate window for Uim library.

%package   qtimmodule
Summary:   Plugin for using UIM on qt-immodule
Group:     System/Internationalization
Requires:  %{name} = %{version}
Requires:  qt3 > 3.3.4-9mdk
Obsoletes: quiminputcontextplugin

%description qtimmodule
A plugin for using UIM on qt-immodule.
%endif

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
%setup -q
%patch0 -p0
%patch1 -p0

%build
./autogen.sh
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
%if %{with_qt3}
   --with-qt \
   --with-qt-immodule \
%endif
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
%find_lang uim-chardict-qt

%clean
rm -rf $RPM_BUILD_ROOT


%post gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README
%doc sigscheme/doc/*
%{_bindir}/uim-el*-agent
%{_bindir}/uim-fep*
%{_bindir}/uim-module-manager
%{_bindir}/uim-sh
%{_bindir}/uim-xim
%{_bindir}/uim-m17nlib-relink-icons
%{_datadir}/applications/*
%{_datadir}/emacs/site-lisp/uim-el/*.el
%{_mandir}/man1/*
%dir %{_datadir}/uim
%{_datadir}/uim/*.scm
%{_datadir}/uim/helperdata/*
%{_datadir}/uim/lib/*.scm
%{_datadir}/uim/pixmaps/*

%files gtk
%defattr(-,root,root)
%doc COPYING
%{_bindir}/uim-*-gtk*
%{_bindir}/uim-input-pad-ja
%{_libdir}/uim-candwin-gtk
%{_libdir}/gtk-2.0/*/immodules/*.so

%if %{with_qt3}
%files qt -f uim-chardict-qt.lang
%defattr(-,root,root)
%doc COPYING
%{_bindir}/uim-*-qt*
%{_libdir}/uim-candwin-qt

%files qtimmodule
%defattr(-,root,root)
%doc COPYING
%{qt3plugins}/inputmethods/*.so
%endif

%files qt4immodule
%doc COPYING
%{qt4plugins}/inputmethods/*.so

%files base
%defattr(-,root,root)
%{_libdir}/uim-helper-server
%{_libdir}/bonobo/servers/*.server
%{_libexecdir}/uim-toolbar-applet
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
