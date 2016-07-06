Name: neovim
Version: 0.1.4
Release: 1
# 
Source0: https://github.com/neovim/neovim/archive/v%{version}.tar.gz
Source1: https://github.com/neovim/deps/raw/master/opt/LuaJIT-2.0.4.tar.gz
Source2: https://github.com/mauke/unibilium/archive/v1.2.0.tar.gz
Source3: https://github.com/neovim/libvterm/archive/a9c7c6fd20fa35e0ad3e0e98901ca12dfca9c25c.tar.gz
Source4: https://github.com/msgpack/msgpack-c/archive/cpp-1.0.0.tar.gz
Source5: https://github.com/libuv/libuv/archive/v1.8.0.tar.gz
Source6: https://github.com/jemalloc/jemalloc/releases/download/4.0.2/jemalloc-4.0.2.tar.bz2
Source7: https://github.com/keplerproject/luarocks/archive/5d8a16526573b36d5b22aa74866120c998466697.tar.gz
Summary: A fork of the vim editor for better extensibility
URL: http://neovim.io/
License: GPL
Group: Editors
BuildRequires: pkgconfig(termkey)
BuildRequires: pkgconfig(unibilium)
BuildRequires: pkgconfig(vterm)
BuildRequires: cmake
BuildRequires: make
Recommends: xsel

%description
A fork of the vim editor for better extensibility

%prep
%setup
cat >local.mk <<'EOF'
CMAKE_BUILD_TYPE := Release
CMAKE_EXTRA_FLAGS += -DENABLE_JEMALLOC:BOOL=OFF -DCMAKE_INSTALL_PREFIX=%{_prefix} -DUSE_BUNDLED_DEPS:BOOL=OFF -DLIBTERMKEY_USE_STATIC:BOOL=OFF -DLIBUNIBILIUM_USE_STATIC:BOOL=OFF -DLIBUV_USE_STATIC:BOOL=OFF -DLIBVTERM_USE_STATIC:BOOL=OFF -DLUAJIT_USE_STATIC:BOOL=OFF -DMSGPACK_USE_STATIC:BOOL=OFF
EOF
mkdir -p build/downloads
cd build/downloads
mkdir luajit unibilium libvterm msgpack libuv jemalloc luarocks
ln %{SOURCE1} luajit/
ln %{SOURCE2} unibilium/
ln %{SOURCE3} libvterm/
ln %{SOURCE4} msgpack/
ln %{SOURCE5} libuv/
ln %{SOURCE6} jemalloc/
ln %{SOURCE7} luarocks/

%build
%make

%install
%makeinstall_std
%find_lang nvim

%files -f nvim.lang
%{_bindir}/*
%{_datadir}/nvim
%{_mandir}/man1/*
