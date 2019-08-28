from tkinter import *
from PIL import Image, ImageTk
import tkinter.filedialog


def method_for_dispatch():
    """记录客户选择模式"""
    # global method_tuple
    get_var_1 = var_1.get()
    get_var_2 = var_2.get()
    get_var_3 = var_3.get()
    get_var_4 = var_4.get()
    from middle_transfer import first_start_up
    first_start_up(get_var_1, get_var_2, get_var_3, get_var_4)


def file_path():
    """记录数据文件路径"""
    global filename_list
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        text_show.insert('end', filename)
        from middle_transfer import second_start_up
        filename_tuple = (filename,)
        second_start_up(*filename_tuple)
    else:
        pass


# main
window = Tk()
window.title("Witcher: Wild Hunt")
window.configure(background="black")

# photo image for background
img = Image.open("D:/testing/parts/blood_and_wine2.jpg")
img_size = img.size
w_img = int(img_size[0] * 0.45)
h_img = int(img_size[1] * 0.45)
img = img.resize((w_img, h_img), Image.ANTIALIAS)
bg_img = ImageTk.PhotoImage(img)
w_window = bg_img.width() + 4
h_window = bg_img.height() + 4
window.geometry("%dx%d" % (w_window, h_window))
window.resizable(width=False, height=False)
Label(window, background="grey", image=bg_img, justify=CENTER).pack()

# frame
x_frame = int(w_window * 0.4)
y_frame = int(h_window * 0.05)
frame_main = Frame(window)
frame_main.place(x=x_frame, y=y_frame)

# logo
logo = Image.open("D:/testing/parts/logo1.png")
logo_size = logo.size
w_logo = logo_size[0]
h_logo = logo_size[1]
logo_b = ImageTk.PhotoImage(logo)

# canvas
w_canvas = (w_window - x_frame)-20
h_canvas = (h_window * 0.9)
# flat, groove, raised, ridge, solid, or sunken
canvas = Canvas(frame_main, width=w_canvas, height=h_canvas, background="#D2B48C", relief="solid")
# logo
x_anchor = int((w_canvas - w_logo) / 2)
canvas.create_image(x_anchor, 40, anchor='w', image=logo_b)
canvas.pack()

# 文件路径显示
text_show = Text(canvas, background="#8B4513", height=2, width=27, fg="white",
                     font=("Calibri", 12, "bold"))
text_show.place(x=15, y=120)

# lb = Label(canvas, text='')
# lb.place(x=30, y=130)
open_file_btn = Button(
    canvas,
    text="打开文件",
    command=file_path,
    font=("Calibri", 12, "bold"),
    relief="raised",
    activebackground="#696969   ",
    activeforeground="#F5F5F5"
)

# btn.pack()
open_file_btn.place(x=15, y=175)

# check box1
var_1 = IntVar()
mode_1_cb = Checkbutton(canvas, text="重消",
                        background="#D2B48C",
                        font=("Calibri", 12),
                        variable=var_1)
mode_1_cb.place(x=15, y=220)

# check box 2
var_2 = IntVar()
mode_2_cb = Checkbutton(canvas, text="现金分",
                        background="#D2B48C",
                        font=("Calibri", 12),
                        variable=var_2)
mode_2_cb.place(x=15, y=250)

#check box 3
var_3 = IntVar()
mode_3_cb = Checkbutton(canvas, text="mode_3",
                        background="#D2B48C",
                        font=("Calibri", 12),
                        variable=var_3)
mode_3_cb.place(x=15, y=280)

#check box 4
var_4 = IntVar()
mode_4_cb = Checkbutton(canvas, text="mode_4",
                        background="#D2B48C",
                        font=("Calibri", 12),
                        variable=var_4)
mode_4_cb.place(x=15, y=310)

# button
show_btn = Button(canvas, text="开始",
                  command=method_for_dispatch)
show_btn.place(x=15, y=350)

window.mainloop()
