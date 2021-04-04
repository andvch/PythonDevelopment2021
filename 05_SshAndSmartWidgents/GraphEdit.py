#!/usr/bin/env python3
import tkinter as tk
import random

class App(tk.Frame):
    def __init__(self, master=None, title="<application>", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")

        self.T = tk.Text(self, width=60, undo=True, wrap=tk.WORD, font="fixed")
        self.T.grid(row=0, column=0, sticky="NS")
        self.T.bind("<<Modified>>", lambda _: self.text2graphic())
        self.T.tag_config("error", background="red")

        self.C = tk.Canvas(self)
        self.C.grid(row=0, column=1, sticky="NEWS")
        self.C.bind("<Button>", self.click)
        self.C.bind("<Motion>", self.motion)
        self.C.bind("<ButtonRelease>", lambda _: self.graphic2text())

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def click(self, event):
        objIDs = self.C.find_overlapping(event.x, event.y, event.x, event.y)
        if objIDs:
            self.currentObj = objIDs[-1]
            self.mode = "move"
        else:
            self.currentObj = self.C.create_oval(event.x, event.y, event.x, event.y, \
                fill=random.choice(("red", "orange", "yellow", "green", "blue")))
            self.mode = "resize"
        self.objCoords = event.x, event.y

    def motion(self, event):
        if not event.state & 0x0100:
            return
        if self.mode == "move":
            self.C.move(self.currentObj, event.x - self.objCoords[0], event.y - self.objCoords[1])
            self.objCoords = event.x, event.y
        elif self.mode == "resize":
            self.C.coords(self.currentObj, self.objCoords[0], self.objCoords[1], event.x, event.y)

    def graphic2text(self):
        text = []
        for obj in self.C.find_all():
            d = self.C.itemconfigure(obj)
            line = [self.C.type(obj)] + list(map(str, self.C.coords(obj))) + \
                [f"{k}='{d[k][-1]}'" for k in ("fill", "outline", "width")]
            text.append(' '.join(line))
        self.T.delete(1.0, tk.END)
        self.T.insert("1.0", '\n'.join(text))
        self.T.edit_modified(False)

    def text2graphic(self):
        if not self.T.edit_modified():
            return
        for obj in self.C.find_all():
            self.C.delete(obj)
        self.T.tag_remove("error", "1.0", "end")
        lines = self.T.get("1.0", "end").splitlines()
        for i in range(len(lines)):
            if not lines[i]:
                continue
            try:
                objType, *params = lines[i].split()
                eval(f"self.C.create_{objType}({', '.join(params)})")
            except Exception:
                self.T.tag_add("error", f"{i + 1}.0", f"{i + 1}.0 + 1 line")
        self.T.edit_modified(False)

app = App(title="GraphEdit")
app.mainloop()
