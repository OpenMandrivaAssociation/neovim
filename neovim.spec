Name: neovim
Version: 0.3.1
Release: 1
Source0: https://github.com/neovim/neovim/archive/v%{version}.tar.gz
Patch0:  neovim-0.1.7-bitop.patch
Summary: A fork of the vim editor for better extensibility
URL: http://neovim.io/
License: GPL
Group: Editors
BuildRequires: pkgconfig(termkey)
BuildRequires: pkgconfig(unibilium)
BuildRequires: pkgconfig(vterm)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libuv)
BuildRequires: pkgconfig(msgpack)
BuildRequires: pkgconfig(luajit)
BuildRequires: lua-mpack
BuildRequires: lua-lpeg
BuildRequires: gperf
BuildRequires: cmake
BuildRequires: make
Recommends: xsel

%description
A fork of the vim editor for better extensibility

%prep
%setup
%apply_patches

%build
%cmake -DLUA_PRG=%{_bindir}/lua -DUSE_BUNDLED=OFF
%make VERBOSE=1

%install
%makeinstall_std -C build
%find_lang nvim

%files -f nvim.lang
%{_bindir}/*
%{_datadir}/nvim
%{_mandir}/man1/*
%{_datadir}/applications/nvim.desktop
%{_datadir}/pixmaps/nvim.png
