

from apps.main_process import web_driver_startup, file_data_startup, login_process


def overall_process(carrier=None, data_obj=None):
    """通过账户总数、数据标记等，整体操控流程"""
    from apps.main_process import login_process
    # 当程序第一次执行，寻找标记并按规定执行流程
    if data_obj.old_file_mark_flag:  # 不是新文档
        login_process(carrier=carrier, data_obj=data_obj)


carrier = web_driver_startup()
data_obj = file_data_startup()
overall_process()