#资料:
# http://www.wb86.com/post/330.html

# https://tkdocs.com/tutorial/text.html

#2022-01-28,22点58
# 现在技术难点已经完全攻破.
#现在解释如下. 道理就是把文字片段的背景色进行修改.(点击界面下面的标注1---5),消除标签点击第一个标注为空按钮
#======这里面我们就标注为B-tag1,I-tag1,E-tag1......B-tag5,....B-tag5即可
#得到BIO文件之后,用户只需要根据自己定好的替换自己需要的标签即可.比如B-PRODUCT...
#解释一下为什么用背景色来区分各个标签.因为我们有时候要标注空格比如尼古拉斯 凯奇.
# 这个名字之间带个空格,那么我们空格也要标注为I-PERSON才行.用前景色无法把空格染色!所以我们用背景色技巧!

#====================第三版. 打开原来的bio文件进行读取之前bio结果.

#==================自定义配置都写最上面:#如何动态修改tkinter按钮.
#=========现在的方案是 按照bio里面的直接按照配色表生成.现在支持10个.#==========现在还是自动配色吧. 搞一个配色表存着太麻烦感觉.
# =======================配置!!!!!!!!!!!!!!!!!!!
color_and_biaoqian=[
#============这个网站能看查询所有颜色!!!!!!!http://color.liminba.com/c/ffb6c1/
    ['#FF6c82','per'],   # 这个就是标准红色. 写red 和#FF0000都行.
    ['yellow','loc'],
    ['Blue','time'],
    ['Cyan','org'],
    ['orange','law'],
    ['PeachPuff', 'veh'],
    ['Gray', 'stg'],
    # ['Brown', 'time4'],
    # ['Tan', 'time5'],
    # ['Beige', 'time6'],
    # ['Beige', 'time6'],
    # ['Beige', 'time6'],
    # ['Beige', 'time6'],


]

#最全的颜色表,如果标签大于上面那个color_and_biaoqian 就会用clis里面的自动.填充.
clis=   ['white',    'red'    ,'yellow','Blue','Cyan','orange','PeachPuff','Gray', 'Brown', 'Tan','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige','Beige',]
#=============支持2种模式, 可以先写bioes或者bio
tool_type='bioes'
# tool_type='bio'
yihangduoshaoniu=10 #====================按钮排版,一行多少个.







# 环境是win10 python3.6

from tkinter import *
#=============第一层是text
import tkinter
import tkinter as tk
root = Tk(className='                                                                                                                            信息抽取标注工具(一键生成bioes格式)')
# frame = Frame (root, relief=RAISED, borderwidth=20)


fon1=('宋体',15)



root.resizable(True,True)







#==============2023-02-09,10点01我们实现行号的添加!


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):

        '''redraw line numbers'''
        self.delete("all")
#====================self.textwidget.index("@0,0") @0,0表示最接近左上角的行信息.
        i = self.textwidget.index("@0,0")#找到0行0列的信息. ref: 参考文档:    https://tkdocs.com/shipman/text-index.html
        hang,lie=i.split('.')
        while True:
            dline = self.textwidget.dlineinfo(i)
            hang,lie=i.split('.')#计算上面i行的信息.    self.textwidget.get(i)
            debug222=self.textwidget.get(i) #这里面显示滚动之后的左上角第一个字.#这时候我们读入的是1.4
            if dline is None: break # Return tuple (x,y,width,height,baseline) giving the bounding box        and baseline position of the visible part of the line containing        the character at INDEX.
            if lie=='0':#===首列才画行号.
                y = dline[1]
                linenum = hang #行信息
                self.create_text(1, y, anchor="nw", text="{0:>4}".format(linenum),font=fon1) #创建行号. 2是x索引.
            # i = self.textwidget.index("%s+1line" % i) #然后计算下一行.
            i = self.textwidget.index(str(int(hang)+1)+'.'+'0') #然后计算下一行.







class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args): #发送自定义信号change
        # let the actual widget perform the requested action
        result=1
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)

            # generate an event if something was added or deleted,
            # or the cursor position changed
            if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
            ):  # //tkinter event_generate手册:http://tcl.tk/man/tcl8.5/TkCmd/event.htm#M34
                self.event_generate("<<Change>>", when="tail")#触发change信号.
        except:
            pass
        # return what the actual widget returned
        return result




class Example(tk.Frame):#=-==============最终我们把text类包装成了ecample这个类.
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self, width=30,height=20,font=fon1,wrap = 'char',background='#C7EDCC')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)#竖直方向的滑动杆.
        self.vsb.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=self.vsb.set)

        self.linenumbers = TextLineNumbers(self, width=50)#创建行号工具#最好让这个宽度跟整个页面长度配套.
        self.linenumbers.attach(self.text) # 绑定行号工具到text空间.
        self.linenumbers.pack(side="left", fill="y")



        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)#绑定修改到重新绘制linenumber
        self.text.bind("<Configure>", self._on_change)

        self.text.insert("end", "one\ntwo\nthree\n")
        self.text.insert("end", "five\n")

    def _on_change(self, event):
        self.linenumbers.redraw()
    def changgelinenum(self):
        print(111111)
        self.linenumbers=TextLineNumbers(self, width=150)
        self.linenumbers.attach(self.text)  # 绑定行号工具到text空间.
        self.linenumbers.pack(side="left", fill="y")


#==========================================================自定义编号结束.




# Example(root).pack(side="top", fill="both", expand=True)

aaa2=Example(root)

#=======reset 行号widget
if 0:
    aaa2.changgelinenum()#=====================这种动态生成无效???????????????????????当行号上W会发生看不见的情况.目前无法解决.


aaa2.pack(side="top", fill="both", expand=True)
text = aaa2.text#=======添加了护眼色.
# text.insert('1.0', '贴入你要处理的sdfsadf张某,李某,sdfsdfasfasd王某他们杀人了fas]\n sdfsadf张某,李某,sdfsdfasfasd王某他们杀人了文字 中文 English 都行\n贴入你要处理的文字')# 1.0 第一行0列.

colorlist=[i[0] for i in color_and_biaoqian]
labellist=[i[1] for i in color_and_biaoqian]

if 0:
    # ====滚动条竖直:
    scroll = tkinter.Scrollbar()
    # 放到窗口的右侧, 填充Y竖直方向
    scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)



#滚动条横向
s2 = Scrollbar(root, orient = HORIZONTAL)
s2.pack(side = BOTTOM, fill = X)

s2.config(command = text.xview)
text.config(xscrollcommand=s2.set)
# print( text.get('1.0', 'end'))
text.pack()
# frame.pack()



#第二层是frame 来放按钮的.
frame = Frame (root, relief=GROOVE, borderwidth=1)
frame.pack (side=TOP, fill=BOTH, ipadx=5, ipady=5, expand=1)
for i in colorlist:
    text.tag_config(i, background=i)  # 再为标签进行设置==类似html里面的div 里面class属性.
def helloCallBack(color):
   # print(1111111111111)
   try:
       # print(SEL_FIRST,SEL_LAST)
       # print(text.index("sel.first"),text.index("sel.last"))

       #===============注意要先删除其他的标签.



       if 1:
           for i in colorlist:
               text.tag_remove( i,text.index("sel.first"), text.index("sel.last"))  # =======变色
       if color !='white':#======white实际上是不进行背景色标注!这样效果最好!!!!!!a trick
            text.tag_add(color, text.index("sel.first"),text.index("sel.last")) #=======变色


       if 0:
           print('=================debug')
           for i in colorlist:
               print(i,text.tag_ranges(i))
       # print(text.tag_ranges(color))


       # print(11111111111)
   except:
       pass


def helloCallBack_read_bio(i,j,color):

   a=i
   b=j
   try:
       #这时候clor重置了,所以要重新跑config.
       text.tag_config(color,  background=color)  # 再为标签进行设置==类似html里面的div 里面class属性.
       #===============注意要先删除其他的标签.
       for i in colorlist:
           text.tag_remove( i,a, b)  # =======变色
       if color !='white':#======white实际上是不进行背景色标注!这样效果最好!!!!!!a trick
            text.tag_add(color, a,b) #=======变色




   except:
       pass

import kmp_for_array

def helloCallBack_quanbiaozhu(color):


   if 1:

       # text.tag_config(color,  background=color)  # 再为标签进行设置
       wenben=text.get(text.index("sel.first"),text.index("sel.last"))

       if 1:
          #=============调用python的搜索
          all_text=text.get('1.0',END)

          tmp= all_text.split('\n')
          out2=[]
          for i in range(len(tmp)):#=========这里面需要字符串的kmp算法
              kkk=kmp_for_array.kmp(tmp[i],wenben,return_all=True)
              if kkk!=-1:
                #================一个bug, 比如 aaa 然后我要把aa标注为红色.那么就会图2次.所以这里面我们强制让他只图最前面的aa,后的aa忽略#==============3.0版本修复了这个bug
                last_tail=0
                for j in kkk:
                    if j>=last_tail:
                        out2.append([f'{i+1}.{j}',f'{i+1}.{j+len(wenben)}' ])
                        last_tail=j+len(wenben)




       for weizhi in out2:
       #===============注意要先删除其他的标签.
           for i in colorlist:
               text.tag_remove( i,weizhi[0], weizhi[1])  # =======变色
           if color !='white':#======white实际上是不进行背景色标注!这样效果最好!!!!!!a trick
                text.tag_add(color,weizhi[0], weizhi[1]) #=======变色

           # print(text.tag_ranges(color))
# import  re
from keyword2 import KeywordProcessor#从https://github.com/Kashian/flashtext 做修改.因为他居然不支持中文!!!!!!!!
from tool_for_pipei import DFAFilter
import time
import  re
def zhengzehelloCallBack_quanbiaozhu(color):


            #======================2023-02-08,19点57出尝试用编辑器自己的search函数来看看速度.现在看没屁用.他不支持正则.







           a=e.get()


           zhengze=re.compile(a)
           aaa=text.get('1.0',"end").split('\n')
           # tmp=re.compile(a).findall(aaa)
           tmp=[]
           for i in aaa:
               tmp+=zhengze.findall(i)
           # tmp=re.findall(a,aaa) ########==========正则代码.






           tmp=list(set(tmp))
           if 1:
               # for i1 in tmp:
                   #找到每一个索引:

                       # a=time.time()
                       # text.tag_config(color, background=color)  # 再为标签进行设置
                       # wenben =i1


#===============改用https://github.com/Kashian/flashtext 这个库包. 比kmp快朵了!!!!!!!!!!!!

                       # keyword_processor = KeywordProcessor()
                       # # keyword_processor.add_keyword(<unclean name>, <standardised name>)
                       # print(tmp,'被查找的东西!!!!!!!')
                       # keyword_processor.add_keywords_from_list(tmp)

                       gfw = DFAFilter()

                       for jjj in tmp:
                           gfw.add(jjj)

                       all_text = text.get('1.0', END)

                       tmp2 = all_text.split('\n')
                       out2 = []
                       for i in range(len(tmp2)):
                            keywords_found = gfw.pipei_shortest(tmp2[i])
                            last_tail = 0
                            for j in keywords_found:
                                if j[0] >= last_tail:
                                    out2.append([f'{i + 1}.{j[0]}', f'{i + 1}.{j[1] }'])
                                    last_tail = j[1] + (j[1]-j[0])
                       print(1)



                       if 0:
                           # =============调用python的搜索

                           all_text = text.get('1.0', END)

                           tmp = all_text.split('\n')
                           out2 = []
                           for i in range(len(tmp)):  # =========这里面需要字符串的kmp算法
                               kkk = kmp_for_array.kmp(tmp[i], wenben, return_all=True)
                               if kkk != -1 and kkk!=0:
                                   # ================一个bug, 比如 aaa 然后我要把aa标注为红色.那么就会图2次.所以这里面我们强制让他只图最前面的aa,后的aa忽略#==============3.0版本修复了这个bug
                                   last_tail = 0
                                   for j in kkk:
                                       if j >= last_tail:
                                           out2.append([f'{i + 1}.{j}', f'{i + 1}.{j + len(wenben)}'])
                                           last_tail = j + len(wenben)






                       # print('kmp:',time.time()-a)

                       # a = time.time()
                       for weizhi in out2:
                           # ===============注意要先删除其他的标签.
                           for i in colorlist:
                               text.tag_remove(i, weizhi[0], weizhi[1])  # =======变色
                           if color != 'white':  # ======white实际上是不进行背景色标注!这样效果最好!!!!!!a trick

                               text.tag_add(color, weizhi[0], weizhi[1])  # =======变色
                       # print('tuse:', time.time() - a)
       # print(11111111111)

#https://blog.csdn.net/wjciayf/article/details/79261005  颜色表
# c0='black'
# c1='red'
# c2='yellow'
# c3='Blue'
# c4='Cyan'
# c5='Lime'
#=================command 这个函数不能用for实现.改用动态生成.可以避免共享变量.
#放按钮使用.
aa=[0,1,2,3,4,5,6,7,8,9,10]
save_all_button=[]
paddd=12
def setup_button():


    # b=tkinter.Button(frame,bg= 'white',text ="标注为空", command = lambda :helloCallBack('white'))
    fun4('white')
    # b.grid(row=0,column=1,padx=10)
    # button_grid_info = b.grid_info()
    # b.grid_forget()
    if 0: #########2023-02-01,18点46这个地方可以删除国企按钮,其实没啥必要删除.因为你扩充时候可能还需要.扩充时候可以自己改代码19行. 添加自己需要的类别.
        for i in save_all_button:#================这一步用来每次删除过期的按钮.
            button_grid_info = i.grid_info()
            i.grid_forget()
  # row column可以自己修改按钮放的位置!!!!!
    for i in range(len(color_and_biaoqian)):

#============callback函数里面不允许写变量..........  #参考https://www.cnpython.com/qa/68533
        if 1:           # lambda表达式.里面要写x=i, 然后再把x传入:右边的函数.这样可以脱离之前的变量控制.
            # fffff=('宋体',10,'bold')
            # b=tkinter.Button(frame, bg=colorlist[i],font=fffff,text =labellist[i], command = lambda x=i: helloCallBack(colorlist[x]))
            # b.grid(row=0,column=(i+1),padx=paddd)
            # save_all_button.append(b)#===============把变量存在全局变量里面,变量就不会跟着函数销毁了.
    #================下面一排是全标注===全文有这个词的直接全标注上.

            # b=tkinter.Button(frame, bg=colorlist[i], font=fffff,text =labellist[i]+'全标', command = lambda x=i:helloCallBack_quanbiaozhu(colorlist[x]))
            # b.grid(row=1,column=(i+1),padx=paddd)
            # save_all_button.append(b)
#==================================================
            # b = tkinter.Button(frame,  bg=colorlist[i],font=fffff,text=labellist[i] + '正则',
            #                    command=lambda x=i: zhengzehelloCallBack_quanbiaozhu(colorlist[x]))
            # b.grid(row=2, column=(i + 1), padx=paddd)
            # save_all_button.append(b)

#=====================第四排综合前3排.

            fun(i)

            # xxx=i
            # menubar.add_command(label=xxx, command=lambda x=xxx:helloCallBack_quanbiaozhu(colorlist[x]))


def fun4(i):
            menubar = tkinter.Menu(frame,tearoff=0)

            def helper1(x=i):
                x = i
                return helloCallBack_quanbiaozhu(x)
            def helper2(x=i):
                x = i
                return zhengzehelloCallBack_quanbiaozhu(x)
            xxx = '全标'
            menubar.add_command(label=xxx, command=helper1)
            xxx = '正则'
            menubar.add_command(label=xxx, command=helper2)
            # 事件处理函数一定要至少有一个参数，且第一个参数表示的是系统事件
            def pop(event,a):
                # 注意使用 event.x 和 event.x_root 的区别
                # menubar.post(event.x, event.y)
                # print(a)
                menubar.post(event.x_root, event.y_root)
            fffff=('宋体',10,'bold')
            b=tkinter.Button(frame, bg=i,font=fffff,text ='annotate to None', command = lambda x=i: helloCallBack(i))
            b.bind("<Button-3>", lambda event, a=3: pop(event, a))
            b.grid(row=0,column=1,padx=paddd)


def fun(i):
            menubar = tkinter.Menu(frame,tearoff=0)

            def helper1(x=i):
                x = i
                return helloCallBack_quanbiaozhu(colorlist[x])
            def helper2(x=i):
                x = i
                return zhengzehelloCallBack_quanbiaozhu(colorlist[x])
            xxx = '全标'
            menubar.add_command(label=xxx, command=helper1)
            xxx = '正则'
            menubar.add_command(label=xxx, command=helper2)
            # 事件处理函数一定要至少有一个参数，且第一个参数表示的是系统事件
            def pop(event,a):
                # 注意使用 event.x 和 event.x_root 的区别
                # menubar.post(event.x, event.y)
                # print(a)
                menubar.post(event.x_root, event.y_root)
            fffff=('宋体',10,'bold')
            b=tkinter.Button(frame, bg=colorlist[i],font=fffff,text =labellist[i], command = lambda x=i: helloCallBack(colorlist[x]))
            b.bind("<Button-3>", lambda event, a=3: pop(event, a))




def fun(i):
            menubar = tkinter.Menu(frame,tearoff=0)

            def helper1(x=i):
                x = i
                return helloCallBack_quanbiaozhu(colorlist[x])
            def helper2(x=i):
                x = i
                return zhengzehelloCallBack_quanbiaozhu(colorlist[x])
            xxx = '全标'
            menubar.add_command(label=xxx, command=helper1)
            xxx = '正则'
            menubar.add_command(label=xxx, command=helper2)
            # 事件处理函数一定要至少有一个参数，且第一个参数表示的是系统事件
            def pop(event,a):
                # 注意使用 event.x 和 event.x_root 的区别
                # menubar.post(event.x, event.y)
                # print(a)
                menubar.post(event.x_root, event.y_root)
            fffff=('宋体',10,'bold')
            b=tkinter.Button(frame, bg=colorlist[i],font=fffff,text =labellist[i], command = lambda x=i: helloCallBack(colorlist[x]))
            b.bind("<Button-3>", lambda event, a=3: pop(event, a))
            b.grid(row=i//yihangduoshaoniu,column=(i%yihangduoshaoniu+2),padx=paddd)
            # save_all_button.append(b)


            # b=tkinter.Button(frame, text ="test4", )
            # b.bind("<Button-3>", lambda event,a=3:pop(event,a))# https://blog.csdn.net/qq_34633194/article/details/120631709 传参方法.
            # b.grid(row=3,column=0,padx=10)




def save():

        global text666
        result=''
        zhengchagn=0
        savefor_rel={}
        save_triple=[]
        try:
            moshi=cmb.get()

            if 'es' in moshi:
                tool_type='bioes'
            else:
                tool_type = 'bio'

            result = text.get("1.0", "end")  # 获取文本输入框的内容


            with open('output.txt','w',encoding='utf-8') as f:
                f.writelines(result)
            result=result.replace('\r\n','\n')
            # result=result.split('\n')
        except:
            text666.set('output.txt写入失败')




        if 1:
            # for i in colorlist:
            #     aaa=text.tag_ranges(i)###=得到的aaa标里面每2个表示开头结尾索引.

            #=======下面都是简单的字符串处理而已
            yuanwen=result.split('\n')
            jieguo=[list('O'*len(i)) for i in yuanwen]
            #=====根据颜色标注即可:
            for dex,i in enumerate(colorlist):
                aaa = text.tag_ranges(i)  ###=得到的aaa标里面每2个表示开头结尾索引.
                for j in range(len(aaa)//2):




                    a11= int(aaa[2*j].string.split('.')[0])#首航
                    a12= int(aaa[2*j].string.split('.')[1])#首列
                    a21= int(aaa[2*j+1].string.split('.')[0])#尾行
                    a22= int(aaa[2*j+1].string.split('.')[1])# 尾列

                    if 1:
                        # ===============这里来处理每个颜色保存到rel里面.
                        # (<textindex object: '1.4'>, <textindex object: '1.9'>) =aaa
                        save_triple.append([yuanwen[a11-1][a12:a22],a11-1,str(labellist[dex]),a12,a22-1])

                        pass








                    if tool_type!='bio':
                        if a11!=a21:
                            pass

                        else:
                            if a22-a12==1:#标注S!
                                jieguo[a11-1][a12]="S-"+str(labellist[dex])
                            else:
                                jieguo[a11-1][a12:a22]=["B-"+str(labellist[dex])]+["I-"+str(labellist[dex])]*(a22-a12-2)+["E-"+str(labellist[dex])]
                    if tool_type=='bio':
                        if a11 != a21:
                            pass

                        else:

                                jieguo[a11 - 1][a12:a22] = ["B-" + str(labellist[dex])] + ["I-" + str(labellist[dex])] * (
                                            a22 - a12 - 1)


            jieguo=[' '.join(i)+'\n' for i in jieguo]

            with open('output.bio','w') as f:
                f.writelines(jieguo)
            zhengchagn=1


            #=====================加一个ner整体输出.
            #=========这个为了后续标注关系时候方便.
            #输出样式: ner1_text  ner1_label ner1_locationhead  ner1_locationtail ner2_text ner2_label ner2_locationhead ner2tail.....########正文的该行.

            #==================处理:



            #=============非锁紧版本
            if 0:
                from collections import defaultdict
                outfor_rel=defaultdict(list)
                for i in save_triple:


                    outfor_rel[i[1]].append([i[0],i[2],str(i[3]),str(i[4])])
                for i in outfor_rel:
                    outfor_rel[i].append(yuanwen[i])

                outlist=['']*(max(outfor_rel.keys())+1)
                sepp='  '
                for i in sorted(outfor_rel.keys()):
                    for jj in range(len(outfor_rel[i])-1):
                        outlist[i]+=sepp+sepp.join(outfor_rel[i][jj])
                    outlist[i]+='######'+outfor_rel[i][-1]
                    outlist[i]=str(i)+sepp+outlist[i][len(sepp):]+'\n'

                with open('output.ner','w',encoding='utf-8') as f:
                    f.writelines(outlist)

            #============我感觉太乱,所以下面改成缩进版本.空格符用/了.
            if 1:
                from collections import defaultdict
                outfor_rel = defaultdict(list)
                for i in save_triple:
                    outfor_rel[i[1]].append([i[0], i[2], str(i[3]), str(i[4])])
                for i in outfor_rel:
                    outfor_rel[i].append(yuanwen[i])
                outlist=[]
                if outfor_rel:
                    outlist = [''] * (max(outfor_rel.keys()) + 1)
                    sepp = '    '
                    suojin='\\'
                    for i in sorted(outfor_rel.keys()):
                        for jj in range(len(outfor_rel[i]) - 1):
                            outlist[i] += sepp + suojin.join(outfor_rel[i][jj])
                        outlist[i] += '######' + outfor_rel[i][-1]
                        outlist[i] = str(i) + sepp + outlist[i][len(sepp):] + '\n'

                with open('output.ner', 'w', encoding='utf-8') as f:
                    f.writelines(outlist)





















            # zhengchagn=1










        # except:
        #     text666.set('output.bio写入失败')


        if 1:
            pass
            # for i in range(len(result)):
            #
            #     savefor_rel[i+1]=result[i]






        if zhengchagn:
            text666.set('bio和txt都写入成功')















setup_button()
def chognzhi():
    global text666
    try:
        #============填入文本.
        with open('output.txt' ,encoding='utf-8') as f:
            tmp=f.readlines()
        text.delete('1.0','end')
        text.insert('1.0',''.join(tmp))






        with open('output.bio' ) as f:
            tmp=f.readlines()
        tmp3=tmp

        tmp=' '.join(tmp).replace('\n',' ').split(' ')
        tmp=[i[2:] for i in tmp if '-' in i]
        tmp2=[]
        for i in tmp:
            if i not in tmp2:
                tmp2.append(i)

        tmp=tmp2

        #=======进行配色.






    #我们的默认标签, 只有当新的跟这里面的不一样时候才做修改.
        global color_and_biaoqian
        global colorlist
        global labellist

        # color_and_biaoqian = [
        #     ['white', '标注为空'],
        # ['red','person'],
        # ['yellow','address'],
        # ['Blue','org'],
        # ['Cyan','telephone'],
        # ['orange','time'],
        # ['PeachPuff', 'nation'],
        # # ['Gray', 'time3'],
        # # ['Brown', 'time4'],
        # # ['Tan', 'time5'],
        # # ['Beige', 'time6']
        #
        # ]
        for i in range(len(tmp)):
            if tmp[i] not in labellist:
                color_and_biaoqian.append([clis[i+1],tmp[i]]) #替换就的按钮.
        colorlist = [i[0] for i in color_and_biaoqian]
        labellist = [i[1] for i in color_and_biaoqian]
        setup_button()
        #=============下面我们根据bio进行涂色.

        tmp3=[i1.replace('\n','').split(' ') for i1 in tmp3]
        for i in range(len(tmp3)):
            for j in range(len(tmp3[i])):

                if '-' in tmp3[i][j]:
                    aaa=tmp3[i][j][2:]
                    for jjj in color_and_biaoqian:
                        if jjj[1]==aaa:
                            color=jjj[0]
                            helloCallBack_read_bio(str(i+1)+'.'+str(j),str(i+1)+'.'+str(j+1),color)
        text666.set('读取成功')
    except:
        text666.set('读取失败')











#=============第三版我们来实现读取bio文件的功能.为了方便就不加对话框了.直接读取output.bio
b=tkinter.Button(frame, text ="load bio和txt", command = chognzhi)
b.grid(row=0,column=0,padx=10)







# entryExample = Entry(root)
# entryExample.place(x = -10,
#         y =-10,
#         width=2000,
#         height=100)
import tkinter
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中




# 创建下拉菜单
cmb = ttk.Combobox(frame,state="readonly")
cmb.grid(row=1, column=(1), padx=20)
# 设置下拉菜单中的值
cmb['value'] = ('标注模式bioes', '标注模式bio')

# 设置默认值，即默认下拉框中的内容
cmb.current(0)
# 默认值中的内容为索引，从0开始



import tkinter as tk

text666 = tk.StringVar()



aaa=tkinter.Label(frame,textvariable=text666, bg='yellow')
aaa.grid(row=2,column=0,padx=10)


text666.set("type regex to right")
b=tkinter.Button(frame, text ="save to BIO和txt", command = save)
b.grid(row=1,column=0,padx=10)





# b=tkinter.Button(root, text ="标注2", command = helloCallBack(c2))
# b.pack()
# b=tkinter.Button(root, text ="标注3", command = helloCallBack(c3))
# b.pack()
# b=tkinter.Button(root, text ="标注4", command = helloCallBack(c4))
# b.pack()
# b=tkinter.Button(root, text ="标注5", command = helloCallBack(c5))


# text.tag_add('highlightline', '5.0', '6.0')




E1 = Entry(frame, bd =5,)
E1.insert('0','.{1}某')

E1.grid(row=2, column=(1), padx=20)

e=E1


# b = tkinter.Button(frame, text='右边输入你要的正则再点我进行标注', command=lambda x=1:reg())
# b.grid(row=2, column=( 0), padx=10)



#按扭调用的函数，
def reg():
    a = e.get()









# import base64
uuid='[[sep]]'
# import flask
# import json
global_fuwenben=[]
# import klembord          #pip 一下.
waijie=0
# 参考:https://www.coder.work/article/7769372
# 2023-02-06,12点36  //加入样式复制功能.
def fun2(event):

    #========
    a= text.index(tk.INSERT)




    try:
        txt = text.get('sel.first', 'sel.last')

        content = text.dump('sel.first', 'sel.last', tag=True, text=True)

        global  global_fuwenben

        # content编码.




        global_fuwenben=content
        html_text = []

        tmp=eval(str(content))


        #我们往content里面加一个自己的id做校验. 因为如果有其他json会发生混淆.
        content=[uuid]+content
        tmp=json.dumps(content,ensure_ascii=True)
        # tmp=tmp.encode('utf-8')
        tttttttt=json.loads(tmp)



        # print(tmp,9999999999999999999999999999999999999999999999999999999999999999999999999999)
        # print(type(tmp))
        tmp=str(tmp)
        klembord.set_text(uuid)#===========剪贴板里面编解码有问题!!!!!!!!!!所以这里面用一个技巧只需要传递信号即可, 只需要对面校验uuid即可.
        #==========2023-02-06,20点24 目前方案还是用自编码, 不用json, 即使他能用, 也会慢,因为非编辑器数据如果用jsonfy会卡.不如自己做一个头来判断速度快.#但是目前还是jsonfy好实现.先用着.

        # [('tagon', 'sel', '1.0'), ('text', '贴入你要处', '1.0'), ('tagon', 'red', '1.5'), ('text', '理的sdfsadf张某,李某,sdfsdf', '1.5'), ('tagoff', 'red', '1.26'), ('text', 'asf', '1.26'), ('tagon', 'red', '1.29'), ('text', 'asd', '1.29'), ('tagoff', 'red', '1.32'), ('text', '王某他们杀人了fas]', '1.32')]
        #=整理一下 #编码是 sep  color1  sep text1   sep color2   sep text2
        # tmp2=[]
        #
        # for i in range(len(content)):
        #     if content[i][0] =='text' and content[i-1][0]!='tagon':
        #         tmp2.append(sep_for_clipborad)
        #         tmp2.append('white')
        #         tmp2.append(sep_for_clipborad)
        #         tmp2.append(content[i][1])
        #     if content[i][1]=='tagon':
        #         tmp2.append(sep_for_clipborad)
        #         tmp2.append(content[i][1])
        #     if content[i][0] =='text' and content[i-1][0]=='tagon':
        #         tmp2.append(sep_for_clipborad)
        #         tmp2.append(content[i][1])
        # print(tmp2,12341230947239047238947238947329847234234)
        # klembord.set_text(''.join(tmp2))







        #     print(content)
        # 下面我们获取sel.first到sel.last的样式.
        # print(txt)
        # print(event)
        # print(11111111111111)
    except:
        #这是说明从外面来的数据.
        global waijie
        waijie=1
        pass
    return 'break'  # 这种写法可以阻塞ctrlc 的原始使用.
# import copy
def fun3(event):
    neirong=klembord.get_text()
    print(neirong,'neirong999999999999')#=
    global global_fuwenben
    #=========判断一下当前是否有选中.
    try:
        text.delete('sel.first', 'sel.last')
    except:
        pass
    a= text.index(tk.INSERT)
    # neirong=klembord.get_with_rich_text()
    # tmp=json.loads(neirong)
    # print(tmp,'tttttttttttttttmmmmmmmmmmmmmmppppppppppppppppp')
#============原来我发现粘贴板贴过来的内容会多一个字符........还是空白字符................神奇???????????????????
    neirong2=neirong[:len(uuid)]
    # print(uuid,'uuid')
    # print(neirong2.replace(' ','')==uuid,'校验!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # neirong=str(neirong).encode('utf-8')

    try:
      if neirong2!=uuid:
          raise
      if neirong2==uuid:


        global_fuwenben2 = copy.deepcopy(global_fuwenben)
        for i in range(len(global_fuwenben)):
            if global_fuwenben[i][0] == 'tagon' and global_fuwenben[i][1] in colorlist:
                global_fuwenben2[i], global_fuwenben2[i + 1] = global_fuwenben2[i + 1], global_fuwenben2[i]
        global_fuwenben = global_fuwenben2

        a2 = a


        #=============================这个涂色逻辑是错误的!!!!!!!!!!
        for i in global_fuwenben:

            if i[0] == 'text':
                a = a2
                # print(a,'mmmmmmmmmmmmmmmmmmmm')
                text.insert(a, i[1])
                # print(len(i[1].replace('\n', '')), '文本偏移量!!!!!!!!')
                hang, lie = [int(i) for i in (a.split('.'))]
                hang += i[1].count('\n')
                if '\n' in i[1]:
                    lie = 0
                else:
                    lie += len(i[1].replace('\n', ''))
                a2 = str(hang) + '.' + str(lie)
            if 1:

                if i[1] in colorlist and i[0] == 'tagon' or i[0]=='tagoff':  # tuse ==========================注意content标签里面的设置情况, 有的时候你的选择部分on 和off 会不全, 所以我们要2种情况都进行涂色. 虽然会重复凸,但是会保证结果正确!!!!!!!!!

                    color = i[1]

                    text.tag_config(color, background=color)  # 再为标签进行设置==类似html里面的div 里面class属性.
                    # ===============注意要先删除其他的标签.
                    for i in colorlist:
                        text.tag_remove(i, a, a2)  # =======变色
                    if color != 'white':  # ======white实际上是不进行背景色标注!这样效果最好!!!!!!a trick

                        text.tag_add(color, a, a2)  # =======变色

    except:

        # print('...................',content)
        text.insert(a, neirong)

    return  'break'     # 这种写法可以阻塞ctrlv 的原始使用.
    #     pass  #如果解析失败说明他是其他数据不是编辑器里面的json.

    # global global_fuwenben

    # print(waijie,'外接吗??????????????')
    # print(global_fuwenben)


    # print(a,'??????????????????')#光标位置.

    #======== 直接插入就行.因为光标已经有了.


    #=========根据global_fuwenben这个进行插入和涂色.
    # print('接收到的文本是',global_fuwenben)
# [('tagon', 'sel', '1.0'), ('text', '贴入你要处', '1.0'), ('tagon', 'red', '1.5'), ('text', '理的sdfsadf张某,李某,sdfsdf', '1.5'), ('tagoff', 'red', '1.26'), ('text', 'asf', '1.26'), ('tagon', 'red', '1.29'), ('text', 'asd', '1.29'), ('tagoff', 'red', '1.32'), ('text', '王某他们杀人了fas]', '1.32')]
    #=========颜色和text顺序需要交换.







    # colorlist

    # text.insert(a,'ffffffffffffff')












    #==========根据global_fuwenben来在光标位置插入内容即可.



    # print(22222222222222)
    #==========下面我们实现我们的ctrl v






#我已经知道怎么做了, 这种带格式的复制,但是效率不够.所以先不写了.!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if 0:#============带格式的复制还没做好.先不开了.===========明白了还是应该往剪贴板里面写.才能跟原始功能通用.
    text.bind('<Control-c>', fun2)
    text.bind('<Control-v>', fun3) # 拦截ctrlv把

sep_for_clipborad='================[[[sep]]]=====================' #创建一个复杂字符,一般数据会有这个东西.来区分普通数据和编辑器的数据.
#ceshi
if 0:
    klembord.set_with_rich_text('plain text', '<i>plain text</i>')

if 1:
    def backout():
        text.edit_undo()
    def regain():
        text.edit_redo()
    # 定义撤销和恢复按钮
    Button(frame,text = '文本撤销',command = backout).grid(row=3, column=0, sticky="w", padx=10, pady=7)
    Button(frame,text = '文本恢复',command = regain).grid(row=3, column=0, sticky="e", padx=10, pady=7)










#===============================2023-02-15,10点59现在我们改成工具启动就开始重置读取bio和txt
chognzhi()

root.mainloop()













