#!/usr/bin/env python3
import tkinter as tk

class LabelEdit(tk.Label):
    def __init__(self, master, **kwargs):
        self.text = tk.StringVar()
        super().__init__(master, textvariable = self.text,
                anchor='w', font='monospace',
                bg='white', relief='ridge', cursor='xterm',
                takefocus=True, highlightthickness=1, **kwargs)

        self.focus_flag = False
        def flash_cursor():
            if self.cursor.cget("bg") == "black" or not self.focus_flag:
                self.cursor.config(bg='white')
            else:
                self.cursor.config(bg='black')
            self.master.after(500, flash_cursor)

        self.cursor = tk.Frame(self, bg='black', height=18, width=1)
        self.space = 10
        self.move_cursor(move_to=0)
        flash_cursor()

        self.init_handlers()

    def init_handlers(self):
        def focus_in(_):
            self.focus_flag = True
        self.bind('<FocusIn>', focus_in)

        def focus_out(_):
            self.focus_flag = False
            self.cursor.config(bg='white')
        self.bind('<FocusOut>', focus_out)

        def key_handler(event):
            text = self.text.get()
            if event.keysym in ('Tab', 'Return'):
                return
            elif event.keysym in ('Left', 'KP_Left'):
                self.move_cursor(shift_by=-1)
            elif event.keysym in ('Right', 'KP_Right'):
                self.move_cursor(shift_by=+1)
            elif event.keysym == 'Home':
                self.move_cursor(move_to=0)
            elif event.keysym == 'End':
                self.move_cursor(move_to=len(text))
            elif event.keysym == 'Delete':
                self.text.set(text[:self.cursor_position] + text[self.cursor_position + 1:])
            elif event.keysym == 'BackSpace':
                self.text.set(text[:max(self.cursor_position - 1, 0)] + text[self.cursor_position:])
                self.move_cursor(shift_by=-1)
            elif event.char:
                self.text.set(text[:self.cursor_position] + event.char + text[self.cursor_position:])
                self.move_cursor(shift_by=+1)
        self.bind('<Any-Key>', key_handler)

        def mouse_handler(event):
            self.focus_set()
            self.move_cursor(move_to=event.x // self.space)
        self.bind('<Button-1>', mouse_handler)

    def move_cursor(self, move_to=None, shift_by=None):
        if move_to != None:
            self.cursor_position = move_to
        if shift_by != None:
            self.cursor_position += shift_by
        if self.cursor_position < 0:
            self.cursor_position = 0
        l = len(self.text.get())
        if self.cursor_position > l:
            self.cursor_position = l
        self.cursor.place(x=self.cursor_position * self.space, y=2)

class Application(tk.Frame):
    '''Sample tkinter application class'''

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        #self.master.resizable(width=False, height=False)
        self.createWidgets()

    def createWidgets(self):
        '''Create all the widgets'''
        self.columnconfigure(0, weight=1)
        self.E = LabelEdit(self)
        self.E.grid(column=0, row=0, sticky="WE")
        self.E.focus_set()

        self.B = tk.Button(self, text = "Quit", command = self.master.quit)
        self.B.grid(column=0, row=3, sticky="E")

app = Application(title="LabelEdit")
app.mainloop()
