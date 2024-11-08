import vim
from .file import NFile

def is_buffer_open(func):
    def wrapper(*args, **kwargs):
        func(wrapper.is_open, wrapper.window_handle, wrapper.buffer_handle, *args, **kwargs)
        if wrapper.is_open:
            wrapper.is_open = False
        else:
            wrapper.is_open = True
            wrapper.window_handle = vim.api.get_current_win()
            wrapper.buffer_handle = vim.api.get_current_buf()

    wrapper.is_open = False
    wrapper.window_handle = ""
    wrapper.buffer_handle = ""
    return wrapper


DEBUG_INFO = """
[Debug]: File is: {}
[Debug]: Current line hash is: {}
[Debug]: Current line is: {}
[Debug]: Is open: {}
[Debug]: Buffer handle: {}
"""

def check_has_fnote(file: str):
    if NFile.check_file_exists(file):
        # this places an "NF" in your signcolumn indicating you have 
        # a note on such file... XXX: work out why only the third sign
        # seems to be showing...
        vim.command("sign define NFILE text=NF texthl=Search")
        vim.command('exe ":silent :sign place 2 line=1 name=NFILE file=" . expand("%:p")')
        vim.command('exe ":silent :sign place 2 line=2 name=NFILE file=" . expand("%:p")')
        vim.command('exe ":silent :sign place 2 line=3 name=NFILE file=" . expand("%:p")')




@is_buffer_open
def main(is_buffer_open: bool, window_handle: str, buffer_handle: str, file: str): 
    """

    Args:
        file: current file 
        title: title of the line 
    """
    DEBUG = False

    nfile = NFile(file)

    current_line = vim.current.line
    result = hash(current_line)

    if is_buffer_open:
        # we close
        if window_handle in vim.api.list_wins():
            lines = vim.api.buf_get_lines(buffer_handle, 0, 100, False)
            vim.api.win_close(window_handle, True)

            # XXX: we close the buffer and get the current file
            # (otherwise we write to empty buffer, filename = '')
            current_file = vim.eval("resolve(expand('%:p'))")
            nfile = NFile(current_file)
            nfile.dump(lines)
            

    else:
        buffer = vim.api.create_buf(False, True)
        vim.api.open_win(buffer, True, {'relative': 'win', 'width': 100, 'height': 40, 'col': 0,
                                        'row': 1, 'anchor': 'SW', 'style': 'minimal', 'border': 'single'})

        vim.api.buf_set_option(buffer, 'modifiable', True)
        vim.api.command('set filetype=markdown')

        if DEBUG:
            lines = DEBUG_INFO.format(file, result, current_line, is_buffer_open, window_handle).split("\n")
            lines = [x for x in lines if x != ""]
        else:
            lines = []

        lines.extend(nfile.get_lines())


        vim.api.buf_set_lines(buffer, 0, 0, True, lines)

