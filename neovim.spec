# build will override this anyway, so let's skip it
%define _fortify_cflags %nil

%define luaver	5.3

Name:		neovim
Version:	0.4.4
Release:	1
Summary:	Vim-fork focused on extensibility and usability
Group:		Editors
License:	ASL 2.0
URL:		https://neovim.io/
Source0:	https://github.com/neovim/neovim/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        sysinit.vim
Source2:        spec-template
# We add an extra build option to disable this error from stopping the build
Patch0:		01-Wno-misleading-indentation.patch
Patch1:		neovim-0.2.1-bitop.patch
BuildRequires:	cmake
BuildRequires:	gperf
BuildRequires:	lua-lpeg
BuildRequires:	lua-mpack
BuildRequires:	libluv-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig(lua) >= %{luaver}
BuildRequires:	pkgconfig(libuv)
BuildRequires:	pkgconfig(msgpack)
BuildRequires:	pkgconfig(unibilium)
BuildRequires:	pkgconfig(termkey)
BuildRequires:	pkgconfig(vterm)
BuildRequires:	pkgconfig(jemalloc)
BuildRequires:	pkgconfig(libbsd)
Requires:	%{name}-data >= %{version}-%{release}
# NeoVIM requires lua5.2 at runtime
# (kekepower) 20181231
Requires:	lua5.2
Provides:	nvim = %{version}-%{release}
Recommends:	xclip
Recommends:	python2dist(pynvim)
Recommends:	python3dist(pynvim)

%description
Neovim is a project that seeks to aggressively refactor Vim in order to:

- Simplify maintenance and encourage contributions
- Split the work between multiple developers
- Enable advanced UIs without modifications to the core
- Maximize extensibility

%package data
Summary:	Data files for %{name}
BuildArch:	noarch

%description data
Data files for %{name}.

%prep
%autosetup -p1

sed -i "s|sys/end|bsd/sys/end|g" config/CMakeLists.txt

%build
%cmake	-GNinja \
	-DPREFER_LUA=ON \
	-DUSE_BUNDLED_LUAJIT=OFF \
	-DUSE_BUNDLED=OFF \
	-DLUA_PRG=%{_bindir}/lua%{luaver}

%ninja_build

%install
%ninja_install -C build

install -p -m 644 %SOURCE1 %{buildroot}%{_datadir}/nvim/sysinit.vim
install -p -m 644 %SOURCE2 %{buildroot}%{_datadir}/nvim/template.spec

%find_lang nvim

%files
%license LICENSE
%doc BACKERS.md CONTRIBUTING.md README.md
%{_bindir}/nvim
%{_mandir}/man1/nvim.1*
%{_datadir}/pixmaps/nvim.png
%{_datadir}/applications/nvim.desktop

%files data -f nvim.lang
%{_datadir}/nvim/
