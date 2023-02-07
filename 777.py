# 弹出式菜单案例

import tkinter


# def makeLabel():
#     global baseFrame
#     tkinter.Label(baseFrame, text="PHP是最好的编程语言，我用Python").pack()
#

baseFrame = tkinter.Tk()




menubar = tkinter.Menu(baseFrame)
for x in ['1', '2', '3']:
    # menubar.add_separator()
    menubar.add_command(label=x,command=lambda x1=x:print(x1))
# 事件处理函数一定要至少有一个参数，且第一个参数表示的是系统事件
def pop(event,a):
    # 注意使用 event.x 和 event.x_root 的区别
    # menubar.post(event.x, event.y)
    # print(a)
    menubar.post(event.x_root, event.y_root)

b=tkinter.Button(baseFrame, text ="保存文件为BIO和txt", )
b.bind("<Button-3>", lambda event,a=3:pop(event,a))# https://blog.csdn.net/qq_34633194/article/details/120631709 传参方法.
b.grid(row=1,column=0,padx=10)


baseFrame.mainloop()