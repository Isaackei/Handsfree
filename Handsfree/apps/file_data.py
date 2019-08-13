import datetime

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

    def create_new_file_name(self):
        """格式化新文件名"""
        dt = datetime.datetime.now().strftime('%m_%d%H_%M_%S')
        self.file_name = self.new_file_name_format.format(dt)

    def read_file_data(self):
        """
        读取文件数据
        :return: df 数据对象
        """
        # Read file
        df_prepare = pd.read_excel(self.path_of_file, dtype=str, header=0)
        # Find headers
        header_name = df_prepare.columns.values.tolist()

        # format all data
        if header_name[0] != "No.":
            # rename the file
            self.create_new_file_name()
            # 重订数据格式并打开
            df_prepare.index.names = ["No."]
            df_prepare.columns = ["Username", "Password", "Password2"]
            # 新增空列表
            df_prepare['B-stocks'] = ""

            df_prepare.to_excel(self.file_name, index=True)
            # 重新打开文件
            self.path_of_file = pd.ExcelFile(self.file_name)
            self.df = pd.read_excel(self.path_of_file, dtype=str, header=0, index_col=0)
        elif header_name[0] == "No.":
            # 重新打开数据
            self.df = pd.read_excel(self.path_of_file, dtype=str, header=0, index_col=0)
        else:
            # 备用
            print("data wrong")

    def find_data_marks(self):
        """
        传入数据，找出数据标记
        标记为：
        Username 对应 数据个数
        Password 对应 当前索引
        Password2 对应 时间戳
        """
        try:
            print(self.df.loc["config"])
        except:
            self.data_length = len(self.df)
            dt = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
            self.data_index = 0
            config = {
                "Username": self.data_length,
                "Password": self.data_index,
                "Password2": dt,
                "B-stocks": ""
            }
            self.df.loc["config"] = config
            self.df.to_excel(self.file_name)
        finally:
            self.data_index = int(self.df.loc["config", "Password"])
            self.data_length = int(self.df.loc["config", "Username"])

    def get_user_info(self):
        """把用户信息以类实例化属性储存，元祖"""
        self.user_account = (
            self.df.loc[self.data_index, "Username"],
            self.df.loc[self.data_index, "Password"],
            self.df.loc[self.data_index, "Password2"]
        )

    def record_data(self):
        """保存信息，注意，当前方法没有对索引递增"""
        """这里需要考量浮点问题"""
        self.df.loc[self.data_index, 'B-stocks'] = self.stock_R_pin
        self.df.loc["config", 'Password'] = self.data_index
        self.df.to_excel(self.file_name)

    def final_redord_data(self):
        """最终的标记保存，其实就是递增一个索引"""
        if self.data_index < self.data_length - 1:
            self.data_index += 1
            self.df.loc["config", 'Password'] = self.data_index
            self.df.to_excel(self.file_name)
        else:
            print("complete")
