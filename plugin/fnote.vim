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

" if you want to have args use <f-args>
command! -nargs=0 PrintCountry call Hello_world_vim()
command! -nargs=0 FNoteCheckHasNote call Check_has_fnote()

nnoremap <space>' :PrintCountry<CR><CR>

au BufRead,BufNewFile * call Check_has_fnote()


