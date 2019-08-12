import datetime
import pandas as pd

from parts.constances import RAW_FILE_NAME, REFORMAT_FILE_NAME


def read_file_data():
    """
    打开文件并返回数据对象
    :return: df object
    """
    global new_file_name
    path_of_file = pd.ExcelFile(RAW_FILE_NAME)
    df_prepare = pd.read_excel(path_of_file, dtype=str, header=0)
    # 找出列名
    header_name = df_prepare.columns.values.tolist()
    # 固定新文件名字
    new_file_name = str(REFORMAT_FILE_NAME)

    if header_name[0] != "No.":
        # 重订数据格式并打开
        df_prepare.index.names = ["No."]
        df_prepare.columns = ["Username", "Password", "Password2"]
        # 新增空列表
        df_prepare['B-stocks'] = ""
        df_prepare.to_excel(new_file_name, index=True)
        df = pd.read_excel(new_file_name, dtype=str, header=0, index_col=0)
    elif header_name[0] == "No.":
        # 重新打开数据
        df = pd.read_excel(path_of_file, dtype=str, header=0, index_col=0)
    else:
        # 备用
        print("data wrong")
    return df


def find_data_marks(df):
    """
    传入数据，找出数据标记
    :param df: 传入的DataFrame数据
    :return: {
        total count: 有效数据个数
        current index: 当前进行到的数据索引
    }
    """
    total_count = len(df)
    current_index = ""
    dt = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')

    try:
        print(df.loc["config"])
    except:
        config = {
            "Username": total_count,
            "Password": current_index,
            "Password2": dt,
            "B-stocks": ""
        }
        df.loc["config"] = config
        df.to_excel(new_file_name)

    return {
        "total count": df.loc["config", "Username"],
        "current index": current_index
    }


def get_user_info(df, index):

    username = df.loc[index, "Username"]
    password = df.loc[index, "Password"]
    password2 = df.loc[index, "Password2"]

    return username, password, password2


def record_data(df, index, stocks):
    df.loc[index, 'B-stocks'] = stocks
    df.loc["config", 'Password'] = index
    df.to_excel(new_file_name)






























# df1 = pd.DataFrame({"D": [120021, "", 3013]})
#
# res = pd.concat([df, df1], axis=1, ignore_index=False)
#
# df.index.names = ["No."]
# list_name = df.columns.values.tolist()

#
# list_test = []
# for i in range(0, 3):
#     username = res.iloc[i, 0]
#     password = res.iloc[i, 1]
#     list_test.append([username, password])

# res.iloc[1, 0] = 'ironman'

# df.to_excel('WBS2.xls', index=True)

# print(df)
# print(len(df))
# memory_info = df.info(memory_usage='deep')


# print(index_count)
# print(df.loc[305])
# config = {
#     "Username": index_count,
#     "Password": "123",
#     "Password2": "321"
# }
# df.loc["config"] = config