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

" vim: et ts=2 sw=2
