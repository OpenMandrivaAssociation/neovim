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
Version:	0.11.0
Release:	1
Summary:	Vim-fork focused on extensibility and usability
Group:		Editors
License:	ASL 2.0
URL:		https://neovim.io/
Source0:	https://github.com/neovim/neovim/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        sysinit.vim
Source2:        spec-template
Patch0:		neovim-c++syntax-qt-extensions.patch
Patch1:		neovim-spec-syntax-updates.patch
BuildRequires:	gperf
BuildRequires:	gettext
BuildRequires:	luajit
BuildRequires:	luajit-lpeg
BuildRequires:	luajit-mpack
BuildRequires:	libluv-devel >= 1.43.0
# As of 0.9.4, SV translations are ISO-8859-1
BuildRequires:	locales-extra-charsets
BuildRequires:	pkgconfig(luajit)
BuildRequires:	pkgconfig(libuv)
BuildRequires:	pkgconfig(msgpack-c)
BuildRequires:	pkgconfig(unibilium)
BuildRequires:	pkgconfig(termkey)
BuildRequires:	pkgconfig(vterm)
BuildRequires:	pkgconfig(jemalloc)
BuildRequires:	pkgconfig(libbsd)
BuildRequires:	pkgconfig(tree-sitter)
BuildRequires:  pkgconfig(tree-sitter-c)
BuildRequires:  pkgconfig(tree-sitter-lua)
BuildRequires:  pkgconfig(tree-sitter-markdown)
BuildRequires:  pkgconfig(tree-sitter-query)
BuildRequires:  pkgconfig(tree-sitter-vim)
BuildRequires:  pkgconfig(tree-sitter-vimdoc)
BuildRequires:	pkgconfig(libutf8proc)
Requires:	%{name}-data >= %{version}-%{release}
Requires:	luajit
Requires:	luajit-lpeg
Requires:	luajit-mpack
Requires:   %{_lib}tree-sitter-c
Requires:   %{_lib}tree-sitter-lua
Requires:   %{_lib}tree-sitter-markdown
Requires:   %{_lib}tree-sitter-query
Requires:   %{_lib}tree-sitter-vim 
Requires:   %{_lib}tree-sitter-vimdoc
Requires:	libluv
Recommends:	xclip
Recommends:	python%{pyver}dist(pynvim)
Provides:   %{_lib}nvim = %{version}-%{release}
Provides:	nvim = %{version}-%{release}
Provides:	texteditor
%if %{cross_compiling}
BuildRequires:	neovim
%endif
BuildSystem:	cmake
BuildOption:	-DPREFER_LUA:BOOL=OFF
BuildOption:	-DUSE_BUNDLED_LUAJIT:BOOL=OFF
BuildOption:	-DUSE_BUNDLED:BOOL=OFF
BuildOption:	-DENABLE_TRANSLATIONS:BOOL=ON
BuildOption:	-DLUA_PRG=%{_bindir}/luajit

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

%prep -a
%if %{cross_compiling}
# Avoid running TARGET binaries...
sed -i -e 's,\$<TARGET_FILE:nvim>,%{_bindir}/nvim,g' src/nvim/po/CMakeLists.txt test/CMakeLists.txt
sed -i -e 's,\${PROJECT_BINARY_DIR}/bin/nvim,%{_bindir}/nvim,g' runtime/CMakeLists.txt
%endif

%build -p
export HOSTNAME=abf.openmandriva.org

%install -a
install -p -m 644 %SOURCE1 %{buildroot}%{_datadir}/nvim/sysinit.vim
install -p -m 644 %SOURCE2 %{buildroot}%{_datadir}/nvim/template.spec

ln -s nvim %{buildroot}%{_bindir}/vi

# Link to the directory in which sys
install -d %{buildroot}%{_libdir}/tree_sitter

mkdir -p  %{buildroot}%{_libdir}/tree_sitter
ln -s -r  %{buildroot}%{_libdir}/tree_sitter    %{buildroot}%{_datadir}/nvim/runtime/parser

%find_lang nvim

%files
%doc CONTRIBUTING.md README.md
%{_bindir}/vi
%{_bindir}/nvim
%{_mandir}/man1/nvim.1*
%{_datadir}/applications/nvim.desktop
%{_datadir}/icons/*/*/*/nvim.*

%files data -f nvim.lang
%{_datadir}/nvim
