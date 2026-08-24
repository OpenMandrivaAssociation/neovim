# build will override this anyway, so let's skip it
%define _fortify_cflags %nil
%if %{cross_compiling}
# clang -E historically dropped --target when the build system invoked
# the preprocessor; $TARGET-cpp from gcc does not. Keep gcc for now.
%define prefer_gcc 1
%endif

Name:		neovim
Version:	0.12.4
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
Patch2:		neovim-cross-compile.patch
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
BuildRequires:	make
BuildSystem:	cmake
BuildOption:	-DPREFER_LUA:BOOL=OFF
BuildOption:	-DUSE_BUNDLED_LUAJIT:BOOL=OFF
BuildOption:	-DUSE_BUNDLED:BOOL=OFF
BuildOption:	-DENABLE_TRANSLATIONS:BOOL=ON
BuildOption:	-DLUA_PRG=%{_bindir}/luajit
%if %{cross_compiling}
BuildOption:	-DNVIM_HOST_PRG=%{_bindir}/nvim
# Path is exported from %%conf -p (rpm does not expand %%{_builddir} here).
BuildOption:	-DNLUA0_HOST_PRG=$NLUA0_HOST_SO
BuildOption:	-DCOMPILE_LUA:BOOL=OFF
# find_program() otherwise picks sysroot gettext tools when crosscompiling (wrong ELF).
BuildOption:	-DXGETTEXT_PRG=%{_bindir}/xgettext
BuildOption:	-DGETTEXT_MSGFMT_EXECUTABLE=%{_bindir}/msgfmt
BuildOption:	-DGETTEXT_MSGMERGE_EXECUTABLE=%{_bindir}/msgmerge
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

%prep -a

%conf -p
%if %{cross_compiling}
# nlua0 is a Lua C module loaded by the host interpreter during codegen.
# The cross-built copy is the wrong ELF architecture, so build a host one.
HOST_LUA_INC=
for d in /usr/include/luajit-2.1 /usr/include/luajit-2.0 /usr/include/lua5.1; do
	if [ -f "$d/lua.h" ]; then
		HOST_LUA_INC="$d"
		break
	fi
done
HOST_LPEG=
for f in /usr/lib64/lua/5.1/lpeg.so /usr/lib/lua/5.1/lpeg.so; do
	if [ -f "$f" ]; then
		HOST_LPEG="$f"
		break
	fi
done
if [ -z "$HOST_LUA_INC" ] || [ -z "$HOST_LPEG" ]; then
	echo "Host luajit headers and luajit-lpeg are required to cross-compile neovim" >&2
	exit 1
fi
# Use the host compiler, not the target toolchain in CC/CFLAGS.
export NLUA0_HOST_SO="$(pwd)/host-nlua0/nlua0.so"
mkdir -p host-nlua0
/usr/bin/cc -shared -fPIC -O2 -DNVIM_NLUA0 \
	-o "$NLUA0_HOST_SO" \
	src/nlua0.c src/mpack/*.c \
	-I src -I "$HOST_LUA_INC" \
	"$HOST_LPEG"
test -s "$NLUA0_HOST_SO"
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
