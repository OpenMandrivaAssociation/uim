%define anthy_version      6620
%define m17n_lib_version   1.3.4

%define uim_major 8
%define libname %mklibname %{name} %{uim_major}
%define devname %mklibname -d %{name}

%define custom_major 2
%define libcustom %mklibname uim-custom %{custom_major}

%define gcroots_major 0
%define libgcroots %mklibname gcroots %{gcroots_major}

%define scm_major 0
%define libscm %mklibname uim-scm %{scm_major}

Summary:	Multilingual input method library 
Name:		uim
Version:	1.8.6
Release:	1
Group:		System/Internationalization
# uim itself is licensed under BSD
# scm/py.scm, helper/eggtrayicon.[ch], qt/pref-kseparator.{cpp,h}
#   and qt/chardict/chardict-kseparator.{cpp,h} is licensed under LGPLv2+
# pixmaps/*.{svg,png} is licensed under BSD or LGPLv2
License:	BSD and LGPLv2+ and (BSD or LGPLv2)
Url:		http://code.google.com/p/uim/
Source0:	http://uim.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRequires:	ed
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	m17n-db
BuildRequires:	pkgconfig(anthy) >= %{anthy_version}
BuildRequires:	pkgconfig(gtk+-x11-2.0)
BuildRequires:	pkgconfig(gtk+-x11-3.0)
BuildRequires:	pkgconfig(libedit)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgnome-2.0)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libpanelapplet-4.0)
BuildRequires:	pkgconfig(m17n-core) >= %{m17n_lib_version}
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
Requires:	anthy >= %{anthy_version}
Requires:	m17n-lib >= %{m17n_lib_version}
Requires:	skkdic
Requires(post,postun):	gtk2-modules

%description
Uim is a multilingual input method library. Uim's project goal is 
to provide secure and useful input method for all languages.

%files -f %{name}.lang
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
%{_datadir}/uim
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%package gtk
Summary:	GNOME helper for uim
Group:		System/Internationalization
Requires:	%{name} = %{EVRD}
Requires:	gtk+2.0

%description gtk
GNOME helper for uim. It contains some apps like toolbar, 
system tray, applet, candidate window for Uim library.

%files gtk
%{_bindir}/uim-input-pad-ja
%{_bindir}/uim-dict-gtk
%{_bindir}/uim-im-switcher-gtk
%{_bindir}/uim-pref-gtk
%{_bindir}/uim-toolbar-gtk
%{_bindir}/uim-toolbar-gtk-systray
%{_libexecdir}/uim-candwin-horizontal-gtk
%{_libexecdir}/uim-candwin-gtk
%{_libexecdir}/uim-candwin-tbl-gtk
%{_libdir}/gtk-2.0/*/immodules/*.so

#----------------------------------------------------------------------------

%package gtk3
Summary:	GNOME3 helper for uim
Group:		System/Internationalization
Requires:	%{name} = %{EVRD}
Requires:	gtk+3.0

%description gtk3
GNOME3 helper for uim. It contains some apps like toolbar,
system tray, applet, candidate window for Uim library.

%files gtk3
%{_bindir}/uim-dict-gtk3
%{_bindir}/uim-im-switcher-gtk3
%{_bindir}/uim-input-pad-ja-gtk3
%{_bindir}/uim-pref-gtk3
%{_bindir}/uim-toolbar-gtk3
%{_bindir}/uim-toolbar-gtk3-systray
%{_libdir}/gtk-3.0/*/immodules/im-uim.so
%{_libexecdir}/uim-candwin-horizontal-gtk3
%{_libexecdir}/uim-candwin-gtk3
%{_libexecdir}/uim-candwin-tbl-gtk3

#----------------------------------------------------------------------------

%package qt4immodule
Summary:	A plugin for using UIM on qt4-immodule
Group:		System/Internationalization
Requires:	%{name} = %{EVRD}
Requires:	qt4-common

%description qt4immodule
A plugin for using UIM on qt4-immodule.

%files qt4immodule
%{qt4plugins}/inputmethods/*.so

#----------------------------------------------------------------------------

%package base
Summary:	Misc files needed by UIM library
Group:		System/Internationalization

%description base
Misc files needed by UIM library.

%files base
%{_libexecdir}/uim-helper-server
%{_libexecdir}/uim-toolbar-applet*
%{_datadir}/gnome-panel/4.0/applets/UimApplet.panel-applet
%{_libdir}/uim/plugin/libuim-*.so

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	UIM library
Group:		System/Internationalization
Suggests:	uim-base

%description -n %{libname}
UIM library.

%files -n %{libname}
%{_libdir}/libuim.so.%{uim_major}*

#----------------------------------------------------------------------------

%package -n %{libcustom}
Summary:	Custom library for UIM
Group:		System/Internationalization

%description -n %{libcustom}
Custom library for UIM.

%files -n %{libcustom}
%{_libdir}/libuim-custom.so.%{custom_major}*

#----------------------------------------------------------------------------

%package -n %{libgcroots}
Summary:	Gcroots library for UIM
Group:		System/Internationalization

%description -n %{libgcroots}
ohis library abstracts architecture-dependent part of garbage collector
roots acquisition such as register windows of SPARC and register stack
backing store of IA-64.

With this library, one can easily write his own garbage collector for
small footprint, some application-specific optimizations, just learning or
testing experimental ideas.

%files -n %{libgcroots}
%{_libdir}/libgcroots.so.%{gcroots_major}*

#----------------------------------------------------------------------------

%package -n %{libscm}
Summary:	Scm library for UIM
Group:		System/Internationalization

%description -n %{libscm}
Scm library for UIM.

%files -n %{libscm}
%{_libdir}/libuim-scm.so.%{scm_major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers of uim for development
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libcustom} = %{EVRD}
Requires:	%{libgcroots} = %{EVRD}
Requires:	%{libscm} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Headers of %{name} for development.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%prep
%setup -q
libtoolize --force
aclocal -I m4
automake -a
autoconf

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
%makeinstall_std

# remove docs for sigscheme (they should be installed by %doc)
rm -rf %{buildroot}%{_datadir}/doc/sigscheme

%find_lang %{name}

