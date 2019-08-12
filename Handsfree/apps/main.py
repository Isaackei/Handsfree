from selenium.webdriver.common.by import By

from apps.basic import DemoSum

# def start():
#     file_data = FilesData()  # 获取文件数据
#     file_data.read_file_data()
#     data = file_data.df
#     data_marks = file_data.find_data_marks()
#
#     data_index = data_marks["current index"]
#     data_length = data_marks["total count"]
#
#     for i in range(data_index, data_length):
#
#         username, password, password2 = FilesData.get_user_info(df=data, index=i)
#         print(username)
#         ii = i + 1
#         file_data.record_data(index=ii)

# load data
from apps.file_data import FilesData

data_obj = FilesData()
data_obj.read_file_data()
data_walker = data_obj.df
data_marks = data_obj.find_data_marks()
data_index = data_marks['current index']
data_length = data_marks['total count']

# login
walker = DemoSum()
walker.get_url()
login_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT'][@value=' Login ']")
login_btn = walker.target_button_ready(login_btn_locate)
walker.login_process(username=u, password=p)
login_btn.click()

# stock mode A
walker.common_refresh()
trade_btn_locate = (By.XPATH, "//a[@class='GLink'][text()='交易']")
trade_btn = walker.target_button_ready(trade_btn_locate)
trade_btn.click()
# stock mode A step two
R_pin_btn_locate = (By.XPATH, "//a[contains(text(),'重消贷款')][contains(text(),'重消') or text()='买 (重消贷款)']")
R_pin_btn = walker.target_button_ready(R_pin_btn_locate)
R_pin_btn.click()
# 进入交易流程，当前位置为交易数值输入
walker.common_refresh()

