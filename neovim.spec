# build will override this anyway, so let's skip it
%define _fortify_cflags %nil
%if %{cross_compiling}
# FIXME The build system throws out some compiler flags while
# running cpp -E, so it doesn't invoke the correct -target
# when using clang (but does when using gcc, because it
# calls the separate $TARGET-cpp)
%define prefer_gcc 1
%endif

Name:		neovim
Version:	0.9.1
Release:	3
Summary:	Vim-fork focused on extensibility and usability
Group:		Editors
License:	ASL 2.0
URL:		https://neovim.io/
Source0:	https://github.com/neovim/neovim/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        sysinit.vim
Source2:        spec-template
Patch0:		neovim-c++syntax-qt-extensions.patch
BuildRequires:	cmake
BuildRequires:	gperf
BuildRequires:	luajit
BuildRequires:	luajit-lpeg
BuildRequires:	luajit-mpack
BuildRequires:	libluv-devel >= 1.43.0
BuildRequires:	ninja
BuildRequires:	pkgconfig(luajit)
BuildRequires:	pkgconfig(libuv)
BuildRequires:	pkgconfig(msgpack)
BuildRequires:	pkgconfig(unibilium)
BuildRequires:	pkgconfig(termkey)
BuildRequires:	pkgconfig(vterm)
BuildRequires:	pkgconfig(jemalloc)
BuildRequires:	pkgconfig(libbsd)
BuildRequires:	pkgconfig(tree-sitter)
Requires:	%{name}-data >= %{version}-%{release}
Requires:	luajit
Requires:	luajit-lpeg
Requires:	luajit-mpack
Provides:	nvim = %{version}-%{release}
Requires:	libluv
Recommends:	xclip
Recommends:	python%{pyver}dist(pynvim)
Provides:	texteditor
%if %{cross_compiling}
BuildRequires:	neovim
%endif

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

#sed -i "s|sys/end|bsd/sys/end|g" config/CMakeLists.txt

%if %{cross_compiling}
# Avoid running TARGET binaries...
sed -i -e 's,\$<TARGET_FILE:nvim>,%{_bindir}/nvim,g' src/nvim/po/CMakeLists.txt test/CMakeLists.txt
sed -i -e 's,\${PROJECT_BINARY_DIR}/bin/nvim,%{_bindir}/nvim,g' runtime/CMakeLists.txt
%endif

%build
export HOSTNAME=abf.openmandriva.org
%cmake	-GNinja \
	-DPREFER_LUA=OFF \
	-DUSE_BUNDLED_LUAJIT=OFF \
	-DUSE_BUNDLED=OFF \
	-DLUA_PRG=%{_bindir}/luajit

%ninja_build

%install
%ninja_install -C build

install -p -m 644 %SOURCE1 %{buildroot}%{_datadir}/nvim/sysinit.vim
install -p -m 644 %SOURCE2 %{buildroot}%{_datadir}/nvim/template.spec

ln -s nvim %{buildroot}%{_bindir}/vi

%find_lang nvim

%files
%doc BACKERS.md CONTRIBUTING.md README.md
%{_bindir}/vi
%{_bindir}/nvim
%{_mandir}/man1/nvim.1*
%{_datadir}/applications/nvim.desktop
%{_datadir}/icons/*/*/*/nvim.*

%files data -f nvim.lang
%{_datadir}/nvim
