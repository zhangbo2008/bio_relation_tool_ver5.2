from tkinter import *
from tkinter import messagebox


def newFile():
    messagebox.showinfo("New File-apidemos", "New File-apidemos")


def openFile():
    messagebox.showinfo("Open File-apidemos", "Open File-apidemos")


def saveFile():
    messagebox.showinfo("Save File-apidemos", "Save File-apidemos")


def saveAsFile():
    messagebox.showinfo("Save as File-apidemos", "Save as File-apidemos")


def aboutMe():
    messagebox.showinfo("About Me-apidemos", "About Me...")


root = Tk()
root.title("apidemos.com")
root.geometry("300x180")

menubar = Menu(root)  # 建立最上层菜单
# 建立菜单类别对象,并将此菜单类别命名为File
filemenu = Menu(menubar)
menubar.add_cascade(label="File -apidemos", menu=filemenu)
# 在File菜单内建立菜单列表
filemenu.add_command(label="New File -apidemos", command=newFile)
filemenu.add_command(label="Open File -apidemos", command=openFile)
# filemenu.add_separator()
filemenu.add_command(label="Save File -apidemos############", command=saveFile)
# filemenu.add_separator()########################
filemenu.add_command(label="Save As File -apidemos", command=saveAsFile)
# filemenu.add_separator()
filemenu.add_command(label="Exit Exit-apidemos!", command=root.destroy)
# 建立菜单类别对象,并将此菜单类别命名为Help
helpmenu = Menu(menubar)
menubar.add_cascade(label="Help-apidemos", menu=helpmenu)
# 在Help菜单内建立菜单列表
helpmenu.add_command(label="About Me-apidemos", command=aboutMe)

root.config(menu=menubar)  # 显示菜单对象

root.mainloop()