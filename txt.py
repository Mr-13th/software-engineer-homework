# -*- coding: utf-8 -*-
# @Time    : 2020/10/13
# @Author  : aurora
# @Site    :
# @File    : note.py
# @Version : 1.0
# @Python Version : 3.7
# @Software: PyCharm


from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import scrolledtext
import os

filename = ''


def author():  # 定义作者函数
    showinfo(title="作者", message="aurora")   # tkinter.messagebox 模块中的showinfo()函数   展示一个小的图形用户界面（弹窗） 展示文本message信息


def power():   # 定义版权函数
    showinfo(title="版权信息", message="版权归aurora所有")


def edition():
    showinfo(title="版本号", message="version 1.0")


def new_file(*args):  # 新建文件   可变长参数
    global top, filename, textPad  # 全局变量
    top.title("未命名文件")   # 界面标题由记事本改为 未命名文件
    filename = None   # 文件名
    textPad.delete(1.0, END)   #  ？？？


def open_file(*args):  # 打开文件
    global filename    # 全局变量 文件名
    filename = askopenfilename(defaultextension=".txt")   #
    if filename == "":
        filename = None
    else:
        top.title("" + os.path.basename(filename))   # 系统路径文件名
        textPad.delete(1.0, END)
        f = open(filename, 'r', encoding="utf-8")    # 打开文件 新建文件对象f  利用open函数 指定文件名 操作模式r（默认） 写入  编码方式 utf—8
        textPad.insert(1.0, f.read())
        f.close()     # 关闭文件对象


def click_open(event):   # 点击打开
    global filename
    top.title("" + os.path.basename(filename))  # 调用系统的方法
    textPad.delete(1.0, END)
    f = open(filename, 'r', encoding="utf-8")
    textPad.insert(1.0, f.read())  # 读入
    f.close()


def save(*args):   # 保存
    global filename
    try:
        f = open(filename, 'w', encoding="utf-8")
        msg = textPad.get(1.0, 'end')
        f.write(msg)
        f.close()
    except:
        save_as()  # 如果不能保存，就执行另存为的函数save_as


def save_as(*args):   # 另存为
    global filename
    f = asksaveasfilename(initialfile="未命名.txt", defaultextension=".txt")
    filename = f
    fh = open(f, 'w', encoding="utf-8")
    msg = textPad.get(1.0, END)
    fh.write(msg)
    fh.close()
    top.title("" + os.path.basename(f))


def rename(newname):  # 系统重命名函数
    global filename
    name = os.path.basename(os.path.splitext(filename)[0])
    oldpath = filename
    newpath = os.path.dirname(oldpath) + '/' + newname + '.txt'
    os.rename(oldpath, newpath)
    filename = newpath
    refresh()  # 调用刷新函数


def rename_file(*args):  # 重命名
    global filename
    t = Toplevel()
    t.geometry("260x80+200+250")
    t.title('重命名')
    frame = Frame(t)
    frame.pack(fill=X)
    lable = Label(frame, text="文件名")
    lable.pack(side=LEFT, padx=5)
    var = StringVar()
    e1 = Entry(frame, textvariable=var)
    e1.pack(expand=YES, fill=X, side=RIGHT)
    botton = Button(t, text="确定", command=lambda: rename(var.get()))
    botton.pack(side=BOTTOM, pady=10)


def delete(*args):  # 删除
    global filename, top
    choice = askokcancel('提示', '要执行此操作吗')
    if choice:
        if os.path.exists(filename):
            os.remove(filename)
            textPad.delete(1.0, END)
            top.title("记事本")
            filename = ''


def cut():  # 剪切函数
    global textPad
    textPad.event_generate("<<Cut>>")


def copy():  # 复制函数
    global textPad
    textPad.event_generate("<<Copy>>")


def paste():  # 粘贴函数
    global textPad
    textPad.event_generate("<<Paste>>")


def undo():  # 撤销
    global textPad
    textPad.event_generate("<<Undo>>")


def redo():  # 重做
    global textPad
    textPad.event_generate("<<Redo>>")


def select_all():  # 全选
    global textPad
    textPad.tag_add("sel", "1.0", "end")


def find(*agrs):  # 查找栏上面的查找界面
    global textPad
    t = Toplevel(top)
    t.title("查找")
    t.geometry("260x60+200+250")   # 图形用户界面的大小
    t.transient(top)
    Label(t, text="查找：").grid(row=0, column=0, sticky="e")
    v = StringVar()
    e = Entry(t, width=20, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=2, sticky="we")
    e.focus_set()
    c = IntVar()
    Checkbutton(t, text="不区分大小写", variable=c).grid(row=1, column=1, sticky='e')
    Button(t, text="查找所有", command=lambda: search(v.get(), c.get(), textPad, t, e)).grid\
        (row=0, column=2, sticky="e" + "w", padx=2, pady=2)   # 图形界面中的按钮

    def close_search():   # 函数内部定义函数 关闭查找
        textPad.tag_remove("match", "1.0", END)
        t.destroy()

    t.protocol("WM_DELETE_WINDOW", close_search)


def mypopup(event):  # 弹出菜单
    global editmenu
    editmenu.tk_popup(event.x_root, event.y_root)


def search(needle, cssnstv, textPad, t, e):   # 文章内部进行查找 匹配的函数
    textPad.tag_remove("match", "1.0", END)
    count = 0
    if needle:
        start = 1.0
        while True:
            pos = textPad.search(needle, start, nocase=cssnstv, stopindex=END)
            if not pos:
                break
            strlist = pos.split('.')  # 分割字符串
            left = strlist[0]
            right = str(int(strlist[1]) + len(needle))
            lastpos = left + '.' + right
            textPad.tag_add("match", pos, lastpos)
            count += 1
            start = lastpos
            textPad.tag_config('match', background="yellow")  # 查找到的元素变为高亮的黄色  突出显示
        e.focus_set()
        t.title(str(count) + "个被匹配")   #


def refresh():  # 刷新函数
    global top, filename
    if filename:
        top.title(os.path.basename(filename))
    else:
        top.title("记事本")


top = Tk()   # 新建图形用户界面（主界面）
top.title("记事本")  # 顶层标题
top.geometry("640x480+500+200")  # 界面大小

menubar = Menu(top)

# 文件功能
# Menu类控件用来实现顶层/下拉/弹出菜单
filemenu = Menu(top)  # 创建一个顶级菜单
# 通过add_command函数添加一个下拉的子菜单
filemenu.add_command(label="新建", accelerator="Ctrl+N", command=new_file)   # 创建一个下拉菜单“新建”，然后将它添加到顶级菜单中 command绑定点击后调用的函数
filemenu.add_command(label="打开", accelerator="Ctrl+O", command=open_file)
filemenu.add_command(label="保存", accelerator="Ctrl+S", command=save)
filemenu.add_command(label="另存为", accelerator="Ctrl+shift+s", command=save_as)
filemenu.add_command(label="重命名", accelerator="Ctrl+R", command=rename_file)
filemenu.add_command(label="删除", accelerator="Ctrl+D", command=delete)
menubar.add_cascade(label="文件(F)", menu=filemenu)  # 文件

# 编辑功能
editmenu = Menu(top)
editmenu.add_command(label="撤销", accelerator="Ctrl+Z", command=undo)
editmenu.add_command(label="重做", accelerator="Ctrl+Y", command=redo)
editmenu.add_separator()  # 分割线
editmenu.add_command(label="剪切", accelerator="Ctrl+X", command=cut)
editmenu.add_command(label="复制", accelerator="Ctrl+C", command=copy)
editmenu.add_command(label="粘贴", accelerator="Ctrl+V", command=paste)
editmenu.add_separator()
editmenu.add_command(label="查找", accelerator="Ctrl+F", command=find)
editmenu.add_command(label="全选", accelerator="Ctrl+A", command=select_all)
menubar.add_cascade(label="编辑(E)", menu=editmenu)  # 编辑

# 关于 功能
aboutmenu = Menu(top)
aboutmenu.add_command(label="作者", command=author)
aboutmenu.add_command(label="版权", command=power)
aboutmenu.add_command(label="版本", command=edition)  #
menubar.add_cascade(label="关于(A)", menu=aboutmenu)  # 关于

top['menu'] = menubar

shortcutbar = Frame(top, height=25, bg='Silver')
shortcutbar.pack(expand=NO, fill=X)

textPad = Text(top, undo=True)
textPad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)


textPad.bind("<Button-3>", mypopup)  #
top.mainloop()   # 进入主循环

