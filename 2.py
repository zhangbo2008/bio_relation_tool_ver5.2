import tkinter as tk
import tkinter.messagebox as msg


def cbClicked(cbname):
    for cb in cb_group:
        cb_group[cb]["cbobj"]["fg"] = "red" if cb == cbname else "black"
    # msg.showinfo('您点击了', cbname)


cb_group = {
    "cb1": {'cbname': "按钮1", 'cbobj': None},
    "cb2": {'cbname': "按钮2", 'cbobj': None},
    "cb3": {'cbname': "按钮3", 'cbobj': None}
}

win = tk.Tk()

for inx, cb in enumerate(cb_group):
    b = tk.Button(win, width=10, height=1, text=cb_group[cb]["cbname"])
    b["command"] = lambda arg=cb: cbClicked(arg)
    b.grid(row=0, column=inx)
    cb_group[cb]["cbobj"] = b

win.mainloop()

