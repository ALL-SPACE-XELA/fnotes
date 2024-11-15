import vim

class Window:
    def __init__(self, window_handle):
        if isinstance(window_handle, Window):
            self.window_handle = window_handle.get()
        else:
            self.window_handle = window_handle
        self.window_view = None
        self.window_buffer = None

    def add_window_view(self, window_view):
        self.window_view = window_view

    def add_window_buffer(self, buffer):
        self.window_buffer = buffer

    def get_buffer(self):
        return self.window_buffer

    def get(self):
        return self.window_handle

    def __repr__(self):
        return f"window handle: {self.window_handle},window buffer: {self.window_buffer}\n"

    def __str__(self):
        return f"window handle: {self.window_handle},window buffer: {self.window_buffer}\n"

class WindowCycle:
    def __init__(self):
        self.window_handles = self.update_windows()
        self.cycle_order = self.window_handles

    def update_cycle_order(self):
        # we always move the first to the back
        windows = self.cycle_order[1:] + self.cycle_order[:1]
        windows = [Window(x) for x in windows]
        for window in windows:
            window.add_window_view(self.save_window_view(window))
            window.add_window_buffer(self.get_window_buffer())
        return windows

    def update_windows(self):
        windows = [Window(x) for x in vim.api.list_wins() if x]
        for window in windows:
            window.add_window_view(self.save_window_view(window))
            window.add_window_buffer(self.get_window_buffer())
        return windows

    def move_window_to(self, window, to):
        self.switch_to_window(to)
        # swap buffer
        vim.command(f"exe 'hide buf' . {window.get_buffer()}")

    def switch_to_window(self, window):
        vim.current.window = window.get()

    def get_window_buffer(self):
        vim.command('let curBuf = bufnr( "%" )') 
        return vim.eval('curBuf') 


    def save_window_view(self, window) -> dict:
        # FIXME: switch cursor to that window
        self.switch_to_window(window)
        print(dir(vim.call))
        vim.command('let curView = winsaveview()') 
        return vim.eval('curView')


    def cycle(self):
        # to cycle windows, we get map current_window cycle with next
        current_cycle = self.cycle_order
        next_cycle = self.update_cycle_order()
        current_to_next = dict(zip(current_cycle, next_cycle))

        print(current_to_next)

        for (window, to) in current_to_next.items():
            print("HERE: ", to)
            self.move_window_to(window, to)
        print("hidden")



        



def cyclewindows():
    """
    we grab all available windows and create a cycle order

    """
    windowcycle = WindowCycle()
    windowcycle.cycle()
    pass






















































