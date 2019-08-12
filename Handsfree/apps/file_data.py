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
        :param df: 传入的DataFrame数据
        :return: {
            total count: 有效数据个数
            current index: 当前进行到的数据索引
        }
        """
        try:
            print(self.df.loc["config"])
        except:
            total_count = len(self.df)
            dt = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
            current_index = 0
            config = {
                "Username": total_count,
                "Password": current_index,
                "Password2": dt,
                "B-stocks": ""
            }
            self.df.loc["config"] = config
            self.df.to_excel(self.file_name)
        return {
            "total count": int(self.df.loc["config", "Username"]),
            "current index": int(self.df.loc["config", "Password"])
        }

    @staticmethod
    def get_user_info(df, index):

        username = df.loc[index, "Username"]
        password = df.loc[index, "Password"]
        password2 = df.loc[index, "Password2"]

        return username, password, password2

    def record_data(self, index=0, stocks=None):
        self.df.loc[index, 'B-stocks'] = stocks
        self.df.loc["config", 'Password'] = index
        self.df.to_excel(self.file_name)