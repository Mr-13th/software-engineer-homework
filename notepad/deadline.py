import time
import tkinter.font as tkFont
import datetime
from tkinter import *

import tkinter.messagebox


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
    # content = '剩余时间：{}月{}天{}小时{}分钟{}秒'.format(str(dead_month), str(dead_days), str(dead_hours), str(dead_minutes),
    #                                           str(dead_seconds))
    content = '剩余时间:%s月%s天%02d小时%02d分钟%02d秒' % (dead_month, dead_days, dead_hours, dead_minutes,
                                                dead_seconds)
    return content


window = Tk()
window.title("Count Down")  ##窗体标题
window.overrideredirect(False)  ##隐藏窗体任务栏

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = str((screen_width - 888) // 2)
y = str(screen_height - 75)

window.geometry("1080x250")

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


def now():
    timestring = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    timestring = "当前时间:%s" % timestring
    return timestring


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



