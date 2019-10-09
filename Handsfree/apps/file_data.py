from datetime import datetime
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
import pandas as pd

from settings.settings import SAVE_FILE_NAME, OPEN_FILE_NAME


class FilesData(object):
    """
    文件数据读写
    """
    def __init__(self):
        self.file_name = OPEN_FILE_NAME
        self.path_of_file = pd.ExcelFile(self.file_name)
        self.new_file_name_format = SAVE_FILE_NAME
        self.df = None
        self.user_account = None
        self.data_index = None
        self.data_length = None
        self.stock_R_pin = None
        self.method_mark = None
        self.old_file_mark_flag = True
        self.finish_flag = True
        self.dt = None

    def create_new_file_name(self):
        """格式化新文件名"""
        dt = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.file_name = self.new_file_name_format.format(dt)

    def read_file_data(self):
        """
        读取文件数据
        """
        # Read file
        df_prepare = pd.read_excel(self.path_of_file, dtype=str, header=0)
        # Find headers
        header_name = df_prepare.columns.values.tolist()

        # format all data
        if header_name[0] != "No.":
            print("new file")
            # rename the file
            self.create_new_file_name()
            # 重订数据格式并打开
            df_prepare.index.names = ["No."]
            df_prepare.columns = ["Username", "Password", "Password2"]
            # 新增空列表
            df_prepare['R-stocks'] = ""
            df_prepare['XJF-stocks'] = ""
            df_prepare['account-mark'] = ""
            df_prepare['TaiZhi-phone'] = ""
            df_prepare['UserInfo'] = ""
            df_prepare['Sale-stock'] = ""

            df_prepare.to_excel(self.file_name, index=True)
            # 重新打开文件
            self.path_of_file = pd.ExcelFile(self.file_name)
            self.df = pd.read_excel(self.path_of_file, dtype=str, header=0, index_col=0)
        elif header_name[0] == "No.":
            # 重新打开数据
            self.df = pd.read_excel(self.path_of_file, dtype=str, header=0, index_col=0)
        else:
            # 备用
            pass

    def find_data_marks(self):
        """
        传入数据，找出数据标记
        标记为：
        Username 对应 数据个数
        Password 对应 当前索引
        Password2 对应 时间戳
        """
        self.old_file_mark_flag = True
        try:
            print(self.df.loc["config"])
        except:
            print("no mark")
            self.old_file_mark_flag = False
            self.data_length = len(self.df)
            self.dt = datetime.now().strftime('%Y-%m-%d:%H:%M:%S')
            self.data_index = 0
            config = {
                "Username": self.data_length,
                "Password": self.data_index,
                "Password2": self.dt,
                "R-stocks": self.method_mark,
                "XJF-stocks": "",
                "account-mark": "",
                "TaiZhi-phone": "",
                "UserInfo": "",
                "Sale-stock": "",
            }
            self.df.loc["config"] = config
            self.df.to_excel(self.file_name)
        finally:
            self.data_index = int(self.df.loc["config", "Password"])
            self.data_length = int(self.df.loc["config", "Username"])
            self.method_mark = str(self.df.loc["config", "R-stocks"])

    def get_user_info(self):
        """把用户信息以类实例化属性储存，元祖"""
        self.data_index = int(self.df.loc["config", "Password"])
        self.method_mark = str(self.df.loc["config", "R-stocks"])
        self.user_account = (
            self.df.loc[self.data_index, "Username"],
            self.df.loc[self.data_index, "Password"],
            self.df.loc[self.data_index, "Password2"]
        )

    def record_data(self):
        """保存信息，注意，当前方法没有对索引递增"""
        """这里需要考量浮点问题"""
        self.df.loc[self.data_index, 'R-stocks'] = self.stock_R_pin
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def final_record_data(self):
        """最终的标记保存，其实就是递增一个索引"""
        self.finish_flag = True
        if self.data_index < self.data_length - 1:
            self.data_index += 1
            self.df.loc["config", 'Password'] = self.data_index
            self.df.to_excel(self.file_name)
        else:
            self.finish_flag = False

    def progress_point_save(self):
        """对当前进行的用户进度标记"""
        self.df.loc["config", 'R-stocks'] = self.method_mark
        self.df.to_excel(self.file_name)

    # def progress_point_save_2(self):
    #     """对当前进行的用户进度标记"""
    #     self.df.loc["config", 'R-stocks'] = self.method_mark_str
    #     self.df.to_excel(self.file_name)


class SaveData(FilesData):

    def __init__(self):
        super().__init__()
        self.R_stock_value = None
        self.XJF_value = None

    def save_r_stock(self):
        """保存信息，注意，当前方法没有对索引递增"""
        """这里需要考量浮点问题"""
        self.df.loc[self.data_index, 'R-stocks'] = self.stock_R_pin
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def save_xjf_value(self):
        """现金分"""
        self.df.loc[self.data_index, 'XJF-stocks'] = self.XJF_value
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def save_account_error_mark(self):
        """账号有误"""
        self.df.loc[self.data_index, 'account-mark'] = "Error"
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def save_secondary_password_error(self):
        """二级密码有误"""
        self.df.loc[self.data_index, 'account-mark'] = "Error2"
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def save_phone_number(self, phone_num=None):
        """太子支付手机号码记录"""
        self.df.loc[self.data_index, 'TaiZhi-phone'] = phone_num
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def save_information_data(self, info_data=None):
        self.df.loc[self.data_index, 'UserInfo'] = info_data
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def save_sell_stock(self, stock_data=None):
        """卖股"""
        self.df.loc[self.data_index, 'Sale-stock'] = stock_data
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def save_chongxiao_stock(self, chongxiao_stock=None):
        """买重消股"""
        self.df.loc[self.data_index, 'R-stocks'] = chongxiao_stock
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)
