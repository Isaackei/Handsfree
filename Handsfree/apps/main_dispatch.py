from apps.main_process import login_process, method_cash_point, method_r_pin_stock


class Dispatch(object):

    def __init__(self, *args):
        self.method_mark = args
        self.method_mark_tmp = None
        self.method_mark_str = ""

    def transfer_method_status(self):
        """将客户选用模式 转换成 字符串 string 模式"""
        self.method_mark_str = ""
        for i in self.method_mark:
            self.method_mark_str += str(i)

    def dispatcher_process(self, obj=None, carrier=None, data_obj=None):
        """判断客户选择的模式，并执行对应功能"""
        self.transfer_method_status()
        for index in range(len(self.method_mark)):
            method = 'method_{}'.format(index)
            if self.method_mark[index]:
                globals()[method](obj, carrier, data_obj)
        last_step(carrier=carrier, data_obj=data_obj)

    def dispatcher_process_for_last_time(self, obj=None, carrier=None, data_obj=None):
        """判断客户选择的模式，并执行对应功能"""
        self.transfer_method_status()
        self.method_mark_tmp = data_obj.method_mark
        for index in range(len(self.method_mark_tmp)):
            method = 'method_{}'.format(index)
            if self.method_mark_tmp[index] in ["1"]:
                globals()[method](obj, carrier, data_obj)
        last_step(carrier=carrier, data_obj=data_obj)
        data_obj.old_file_mark_flag = False

    def overall_process(self, obj=None, carrier=None, data_obj=None):
        """通过账户总数、数据标记等，整体操控流程"""
        # 当程序第一次执行，寻找标记并按规定执行流程
        if data_obj.old_file_mark_flag:  # 不是新文档
            check_statue = login_process(carrier=carrier, data_obj=data_obj)
            if check_statue is False:
                # 登录失败，结束本次，记录后去下一个账号
                data_obj.final_record_data()
                data_obj.old_file_mark_flag = False
                return
            self.dispatcher_process_for_last_time(obj=obj, carrier=carrier, data_obj=data_obj)

        check_statue = login_process(carrier=carrier, data_obj=data_obj)
        if check_statue is False:
            data_obj.final_record_data()
            return
        self.dispatcher_process(obj=obj, carrier=carrier, data_obj=data_obj)


def method_0(obj, carrier, data_obj):
    """买重消股模式"""

    method_r_pin_stock(carrier, data_obj)
    obj.method_mark_str = "0" + obj.method_mark_str[1:]
    data_obj.method_mark = obj.method_mark_str
    data_obj.progress_point_save()


def method_1(obj, carrier, data_obj):
    method_cash_point(carrier=carrier, data_obj=data_obj)
    obj.method_mark_str = "00" + obj.method_mark_str[2:]
    data_obj.method_mark = obj.method_mark_str
    data_obj.progress_point_save()


def method_2(obj, carrier, data_obj):
    print(obj.method_mark)
    obj.method_mark_str = "000" + obj.method_mark_str[3:]
    print(obj.method_mark_str)
    print("==================")


def method_3(obj, carrier, data_obj):
    print(obj.method_mark)
    obj.method_mark_str = "0000"
    print(obj.method_mark_str)
    print("==================")


def last_step(carrier=None, data_obj=None):
    from apps.main_process import logout_process
    logout_process(carrier=carrier, data_obj=data_obj)
