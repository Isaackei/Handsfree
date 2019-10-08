from tkinter import messagebox

from apps.main_dispatch import Dispatch
from apps.main_process import web_driver_startup, file_data_startup
from middle_transfer import method_tuple


def main_start():
    """主启动程序"""
    carrier = web_driver_startup()
    data_obj = file_data_startup()
    dispatcher = Dispatch(*method_tuple)
    while data_obj.finish_flag:
        dispatcher.overall_process(obj=dispatcher, carrier=carrier, data_obj=data_obj)
    messagebox.showinfo(title="结束", message="完成，共计 {} 个账号.".format(data_obj.data_length))


