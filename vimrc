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
"set foldmethod=marker
colorscheme nord

if exists('+termguicolors')
    set termguicolors              "16 million colours' support
endif

" }}}


" MAP {{{

nmap <Leader>, :vs $MYVIMRC<CR>
nmap <F5> :source $MYVIMRC<CR>

"}}}


" LET {{{

" UltiSnips {{{{
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
"}}}}

" VimTeX {{{{
"if has('win32')
"    let g:vimtex_view_general_viewer = '/path/to/SumatraPDF'
"    let g:vimtex_view_general_options
"                \ = '-reuse-instance -forward-search @tex @line @pdf'
"        let g:vimtex_view_general_options_latexmk = '-reuse-instance'
"    else
"        let g:vimtex_compiler_progname = 'nvr'
"        let g:vimtex_fold_enabled=1
"        let g:vimtex_fold_manual=1
"        let g:vimtex_quickfix_mode=0   "For Linux
"        let g:vimtex_view_general_options = '--unique file:@pdf\#src:@line@tex'
"        let g:vimtex_view_general_options_latexmk = '--unique'
"        let g:vimtex_view_method = 'zathura' 
"        let g:vimtex_view_method='general' 
"    endif
"  }}}}
"
"}}}


" PLUGINS {{{

call plug#begin('~/.vim/plugged')

" make sure you use single quotes
Plug 'SirVer/ultisnips'         
Plug 'lervag/vimtex'         

call plug#end()
"}}}

" YOUR CHANGES 
silent! source ~/.myvimrc         "Add your additions in this file
