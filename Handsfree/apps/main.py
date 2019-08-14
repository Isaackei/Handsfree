from apps.main_dispatch import Dispatch
from apps.main_process import web_driver_startup, file_data_startup
from gui.middle_transfer import method_tuple


def main_start():
    """主启动程序"""
    carrier = web_driver_startup()
    data_obj = file_data_startup()
    dispatcher = Dispatch(*method_tuple)
    while data_obj.finish_flag:
        dispatcher.overall_process(obj=dispatcher, carrier=carrier, data_obj=data_obj)


