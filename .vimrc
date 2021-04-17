" Simple settings file

" STARTUP

let mapleader = " " 
syntax on			     "ADDED LATER


" SET 
set autoindent                               
set linebreak 			              " Wrap lines; last word gets shifted
set mouse=a                          " optional: enable mouse everywhere
set number                           " doesn't get set by default
set spell
set spelllang=en_gb                  "closest to Indian

colorscheme nord

"save https://raw.githubusercontent.com/arcticicestudio/nord-vim/develop/colors/nord.vim 
"to ~/.vim/colors/ or ~/vimfiles/colors/

if exists('+termguicolors')
    set termguicolors              "16 million colours' support
endif

" MAP 

nmap <Leader>, :vs $MYVIMRC<CR>
