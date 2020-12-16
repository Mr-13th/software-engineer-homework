from tkinter import *
from tkinter.filedialog import *
import tkinter.messagebox
from tkinter import scrolledtext
import os
import time                                                                                                                                                                  
import tkinter.font as tkFont
import datetime


filename = ''


def power():   # 定义版权函数
    showinfo(title="Copyright information", message="版权软工作业小组所有")


def edition():
    showinfo(title="Version", message="version 1.0")


def new_file(*args):  # 新建文件   可变长参数
    global top, filename, textPad  # 全局变量
    top.title("NewText")   # 界面标题由记事本改为 未命名文件
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
    f = asksaveasfilename(initialfile="NewText.txt", defaultextension=".txt")
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
    t.title('Save As')
    frame = Frame(t)
    frame.pack(fill=X)
    lable = Label(frame, text="Filename")
    lable.pack(side=LEFT, padx=5)
    var = StringVar()
    e1 = Entry(frame, textvariable=var)
    e1.pack(expand=YES, fill=X, side=RIGHT)
    botton = Button(t, text="Confirm", command=lambda: rename(var.get()))
    botton.pack(side=BOTTOM, pady=10)


def delete(*args):  # 删除
    global filename, top
    choice = askokcancel('Reminder', 'Do you want to do this?')
    if choice:
        if os.path.exists(filename):
            os.remove(filename)
            textPad.delete(1.0, END)
            top.title("Notepad")
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
    t.title("Find")
    t.geometry("260x60+200+250")   # 图形用户界面的大小
    t.transient(top)
    Label(t, text="Find:").grid(row=0, column=0, sticky="e")
    v = StringVar()
    e = Entry(t, width=20, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=2, sticky="we")
    e.focus_set()
    c = IntVar()
    Checkbutton(t, text="Case insensitive", variable=c).grid(row=1, column=1, sticky='e')
    Button(t, text="Find All", command=lambda: search(v.get(), c.get(), textPad, t, e)).grid\
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
        t.title(str(count) + " matched")   #


def refresh():  # 刷新函数
    global top, filename
    if filename:
        top.title(os.path.basename(filename))
    else:
        top.title("Text")


def python_run():
    global filename
    f = asksaveasfilename(initialfile="pycode.py", defaultextension=".py")
    filename = f
    fh = open(f, 'w', encoding="utf-8")
    msg = textPad.get(1.0, END)
    fh.write(msg)
    fh.close()
    top.title("" + os.path.basename(f))
    os.system("python %s" % f)
    return

def cpp_run():
    global filename
    f = asksaveasfilename(initialfile="cppcode.cpp", defaultextension=".cpp")
    filename = f
    fh = open(f, 'w', encoding="utf-8")
    msg = textPad.get(1.0, END)
    fh.write(msg)
    fh.close()
    top.title("" + os.path.basename(f))
    os.system("g++ %s" % f)
    os.system("./a.out")
    return

#start setddl
def setddl():
    window = Tk()
    window.title("Count Down")  ##窗体标题
    window.overrideredirect(False)  ##隐藏窗体任务栏
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = str((screen_width - 888) // 2)
    y = str(screen_height - 75)
    window.geometry("1080x250")
    
    def deadline():
        s = entry.get() # 获取输入框的值
        now_time = time.time()
        aid_date = datetime.datetime.strptime(s, "%Y-%m-%d")
        aid_time = int(time.mktime(aid_date.timetuple()))  # 转化为时间戳
        dead_line = int(aid_time - now_time)  # 时间差
        dead_month = dead_line // (60 * 60 * 24 * 30)
        dead_days = dead_line // (60 * 60 * 24) % 30
        dead_hours = dead_line // (60 * 60) % 24 % 30
        dead_minutes = dead_line // 60 % 60
        dead_seconds = dead_line % 60
        # content = '剩余时间：{}月{}天{}小时{}分钟{}秒'.format(str(dead_month), str(dead_
        #                                           str(dead_seconds))
        content = '剩余时间:%s月%s天%02d小时%02d分钟%02d秒' % (dead_month, dead_days, dead_hours, dead_minutes,dead_seconds)
        return content

    def closewindow():
        if tkinter.messagebox.askokcancel("Quit", "Do you want to exit?"):
            window.destroy()

    label = Label(window, text="Please deadtime:")
    label.config(bg='#ce3366', fg='yellow', font=("华为行楷", 20))
    label.config(relief=RAISED, bd=8, )
    label.grid(row=0, sticky=W)
    ft = tkFont.Font(family="Buxton Sketch", size=36, weight=tkFont.BOLD)
    entry = Entry(window, font=("Hwlvetica", 20, "bold italic"))
    entry.config(bd=2)
    entry.grid(row=0, column=1, sticky=E)
    cutdown_label = Label(window, font=ft, fg="#ce3366")
    cutdown_label.grid(row=1, column=0)  ##放置label
    
    def run():
        timestring = now()
        lab["text"] = timestring
        window.after(1000, run)

    timestring = now()
    lab = Label(window, text=timestring, font=ft, fg="#ce3366")
    lab.grid(row=2, column=0, sticky=W)
    def Refresh():
        try:
            content = deadline()  ##获取倒计时时间
            cutdown_label["text"] = content  ##更新label内容
            window.after(1000, Refresh)  # 1秒刷新
        except ValueError as e:
            print(e)
    # 开始到计时

    botton = Button(window, text='starttime', command=Refresh)
    botton.grid(row=3, sticky=W)
    botton.config(bd=8, relief=RAISED, bg='#ce3366', fg='yellow')
    botton.config(font=("Hwlvetica", 20, "bold italic"))
    # 退出按钮
    btn = Button(window, text="Quit", command=window.quit)
    btn.grid(row=3, column=1, sticky=E)
    btn.config(bd=8, relief=RAISED, bg='#ce3366', fg='yellow')
    btn.config(font=("Hwlvetica", 20, "bold italic"))
    window.protocol('WM_DELETE_WINDOW', closewindow)

    window.after(1000, run)
    window.mainloop()
    return



def now():
    timestring = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    timestring = "当前时间:%s" % timestring
    return timestring



#end setddl

top = Tk()   # 新建图形用户界面（主界面）
top.title("Text")  # 顶层标题
#l = Label(top, text='Hello! this is Tkinter', bg='green', font=('Arial', 12), width=30, height=2)
#l.pack()
top.geometry("640x480+500+200")  # 界面大小
menubar = Menu(top)

# 文件功能
# Menu类控件用来实现顶层/下拉/弹出菜单
filemenu = Menu(top)  # 创建一个顶级菜单
# 通过add_command函数添加一个下拉的子菜单
filemenu.add_command(label="New Document", accelerator="Ctrl+N", command=new_file)   # 创建一个下拉菜单“新建”，然后将它添加到顶级菜单中 command绑定点击后调用的函数
filemenu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save)
filemenu.add_command(label="Save As", accelerator="Ctrl+shift+s", command=save_as)
filemenu.add_command(label="Rename", accelerator="Ctrl+R", command=rename_file)
filemenu.add_command(label="Delete", accelerator="Ctrl+D", command=delete)
menubar.add_cascade(label="File(F)", menu=filemenu)  # 文件

# 编辑功能
editmenu = Menu(top)
editmenu.add_command(label="Backout", accelerator="Ctrl+Z", command=undo)
editmenu.add_command(label="Reform", accelerator="Ctrl+Y", command=redo)
editmenu.add_separator()  # 分割线
editmenu.add_command(label="Shear", accelerator="Ctrl+X", command=cut)
editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=copy)
editmenu.add_command(label="Stick", accelerator="Ctrl+V", command=paste)
editmenu.add_separator()
editmenu.add_command(label="Find", accelerator="Ctrl+F", command=find)
editmenu.add_command(label="Check All", accelerator="Ctrl+A", command=select_all)
menubar.add_cascade(label="Edit(E)", menu=editmenu)  # 编辑

# 关于 功能
aboutmenu = Menu(top)
aboutmenu.add_command(label="Copyright", command=power)
aboutmenu.add_command(label="Setclock", command=setddl)
aboutmenu.add_command(label="Version", command=edition)  #
menubar.add_cascade(label="About(A)", menu=aboutmenu)  # 关于

#编程 功能
codemenu = Menu(top)
codemenu.add_command(label="Run python", command=python_run)
codemenu.add_command(label="Run C++", command=cpp_run)
menubar.add_cascade(label="Code(C)", menu=codemenu)

top['menu'] = menubar

shortcutbar = Frame(top, height=25, bg='Silver')
shortcutbar.pack(expand=NO, fill=X)

textPad = Text(top, undo=True)
textPad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)

textPad.bind("<Control-N>", new_file)
textPad.bind("<Control-n>", new_file)
textPad.bind("<Control-O>", open_file)
textPad.bind("<Control-o>", open_file)
textPad.bind("<Control-S>", save)
textPad.bind("<Control-s>", save)
textPad.bind("<Control-D>", delete)
textPad.bind("<Control-d>", delete)
textPad.bind("<Control-R>", rename_file)
textPad.bind("<Control-r>", rename_file)
textPad.bind("<Control-A>", select_all)
textPad.bind("<Control-a>", select_all)
textPad.bind("<Control-F>", find)
textPad.bind("<Control-f>", find)
textPad.bind("<Button-3>", mypopup)  #
top.mainloop()   # 进入主循环

