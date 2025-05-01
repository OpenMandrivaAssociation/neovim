let g:python_host_prog = '/usr/bin/python'
let g:python3_host_prog = '/usr/bin/python'

if has("autocmd")
  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$")
    \| exe "normal! g'\"" |endif
endif

augroup Fedora
  autocmd!
  " RPM spec file template
  autocmd BufNewFile *.spec silent! 0read /usr/share/nvim/template.spec
augroup END

colorscheme vim

" This disables mouse integration such as the right-click context menu,
" but allows cut&paste to work as long time vi users have come to expect.
" If you prefer mouse integration, override this value with
" set mouse=nvi
" in your per-user ~/.config/nvim/init.vim
set mouse=

" vim: et ts=2 sw=2
