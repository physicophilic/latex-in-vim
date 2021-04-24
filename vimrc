" SIMPLE SETTINGS FILE

" If vim was a human, this file would be its bloodstream. 
" Each line here therefore is like a hormone for vim.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" SO...NEVER...PUT...ANYTHING...HERE...THAT...YOU...DON'T...UNDERSTAND.  |
" .............. VIM WILL GET SICK and (can) DIE ........................|
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


" STARTUP

let mapleader = " " 
syntax on			    


" SET 
set autoindent                               
set linebreak 			             " Wrap lines; last word gets shifted
set mouse=a                          " optional: enable mouse everywhere
set number                           " doesn't get set by default
set spell
set spelllang=en_gb                  " closest to Indian

colorscheme nord


if exists('+termguicolors')
    set termguicolors              "16 million colours' support
endif

" MAP 

nmap <Leader>, :vs $MYVIMRC<CR>
nmap <F5> :source $MYVIMRC<CR>


" PLUGINS

" SPECIFY a directory for plugins
" - AVOID using standard Vim directory names like 'plugin'

call plug#begin('~/.vim/plugged')

" ULTISNIPS

" MAKE sure you use single quotes

Plug 'SirVer/ultisnips'         
Plug 'lervag/vimtex'         

" SETTINGS FOR ULTISNIPS 

let g:UltiSnipsExpandTrigger = '<Tab>'
let g:UltiSnipsJumpForwardTrigger = '<Tab>'
let g:UltiSnipsJumpBackwardTrigger = '<S-Tab>'
let g:UltiSnipsEditSplit = 'vertical'
let g:UltiSnipsEnableSnipMate = 0
"let g:UltiSnipsSnippetDirectories = [$HOME.'/vimfiles/UltiSnips'] "FOR WINDOWS
let g:UltiSnipsSnippetDirectories = [$HOME.'/.vim/UltiSnips'] "FOR THE REST

" INITIALIZE plugin system
call plug#end()

silent! source ~/.myvimrc         "Add your additions in this file
