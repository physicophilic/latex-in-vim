" SIMPLE SETTINGS FILE

" STARTUP {{{

let mapleader = " " 
syntax on 	
	

" }}}
" SET {{{

set autoindent                               
set linebreak 			     " Wrap lines; last word gets shifted
set mouse=a                          " optional: enable mouse everywhere
set number                           " doesn't get set by default
set spell
set spelllang=en_gb                  " closest to Indian
colorscheme nord
" set conceallevel=2

if exists('+termguicolors')
    set termguicolors              "16 million colours' support
endif

set foldmethod=marker
set encoding=utf8		     " required by VimTeX features

" }}}
" HIGHLIGHT {{{

"highlight Conceal guibg=bg

"}}}
" MAP {{{

nmap <Leader>, :vs $MYVIMRC<CR>
nmap <F5> :source $MYVIMRC<CR>

"}}}
" LET {{{

" UltiSnips {{{2

let g:UltiSnipsExpandTrigger = '<Tab>'
let g:UltiSnipsJumpForwardTrigger = '<Tab>'
let g:UltiSnipsJumpBackwardTrigger = '<S-Tab>'
let g:UltiSnipsEditSplit = 'vertical'
let g:UltiSnipsEnableSnipMate = 0

if has('win32')
    let g:UltiSnipsSnippetDirectories = [$HOME.'\vimfiles\UltiSnips'] "FOR WINDOWS
else
    let g:UltiSnipsSnippetDirectories = [$HOME.'/.vim/UltiSnips'] "FOR THE REST
endif

"}}}
" LaTeX with Vim {{{2

"let g:tex_flavor='latex'
"let g:vimtex_fold_enabled=1
"let g:tex_conceal='abdmgs'   
"let g:tex_conceal_frac=1
"let g:vimtex_fold_manual=1

"  }}}}

"}}}
" PLUGINS {{{

call plug#begin('~/.vim/plugged')

" make sure you use single quotes
Plug 'SirVer/ultisnips'         
Plug 'lervag/vimtex'         
"Plug 'KeitaNakamura/tex-conceal.vim'

call plug#end()

"}}}

" YOUR CHANGES 
silent! source ~/.myvimrc         "Add your additions in this file
