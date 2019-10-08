#######################
# Global variables
filename_list = []
filename_list2 = []
method_tuple = None
phone_number = None  # 太子支付手机号码
#######################


def first_start_up(*args, **kwargs):
    global method_tuple
    global phone_number
    method_tuple = args
    phone_number = kwargs["phone_number"]
    from tkinter import messagebox
    from sys import exit
    if (method_tuple[2] == 1) and (phone_number == ""):
        messagebox.showinfo("报错", "请重新打开软件，因为您忘记输入太子支付手机号码")
        exit()
    if (method_tuple[3] == 1) and (phone_number == ""):
        messagebox.showinfo("报错", "请重新打开软件，因为您忘记输入太子支付手机号码")
        exit()

    from apps.main import main_start
    main_start()


def second_start_up(*args):
    global filename_list
    filename_list.append(*args)


def second_start_up2(*args):
    global filename_list2
    filename_list2.append(*args)


