let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')


python << EOF
import sys
from os.path import normpath, join
import vim

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir))
sys.path.append(python_root_dir)

from fnote import fnote as fn

EOF

function! Hello_world_vim()
    python fn.main(vim.eval("resolve(expand('%:p'))"))
endfunction

function! Check_has_fnote()
    python fn.check_has_fnote(vim.eval("resolve(expand('%:p'))"))
endfunction

function! Screen_swap_command()
    python fn.cyclewindows()
endfunction

" if you want to have args use <f-args>
command! -nargs=0 PrintCountry call Hello_world_vim()
command! -nargs=0 FNoteCheckHasNote call Check_has_fnote()
command! -nargs=0 ScreenSwapCommand call Screen_swap_command()

nnoremap <space>' :PrintCountry<CR><CR>
nnoremap <space>r :ScreenSwapCommand<CR><CR>

au BufRead,BufNewFile * call Check_has_fnote()


