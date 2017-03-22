"Turn on line numbers:
set nu

"Turn on search highlighting:
set hlsearch

"Set color scheme:
set t_Co=256
colorscheme molokai

"Turn on syntax highlighting:
syntax on

"Set tab config
set autoindent
set tabstop=2
set shiftwidth=2
set expandtab

"indentLine config (https://github.com/Yggdroot/indentLine)
"let g:indentLine_char = '|'

"Turn on right margin
set colorcolumn=81

"Turn on mouse interaction
set mouse=a

"Highlight trailing whitespace
match ErrorMsg '\s\+$'

"Shift+Tab unindents in insert mode
imap <S-Tab> <C-d>

"Turn on folding
set foldmethod=manual

"Make views automatic
set viewoptions=folds,cursor
autocmd BufWinLeave *.* mkview
autocmd BufWinEnter *.* silent loadview

"Save and run current script
nmap <F2> :w<CR>:!%:p<CR>

"Toggle paste mode
set pastetoggle=<F3>

"Paste from clipboard
nmap <C-p> "+p

"Toggle Tagbar
nmap <F8> :TagbarToggle<CR>

"Change windows
nmap <silent> h :wincmd h<CR>
nmap <silent> l :wincmd l<CR>

"Delete trailing spaces
nmap <F9> :%s/\s\+$//g<CR>

"Show full path of current file
command Path echo expand('%:p')
