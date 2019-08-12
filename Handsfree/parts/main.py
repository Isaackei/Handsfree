import os

from parts import setting
from parts.data_read_write import read_file_data, get_user_info, find_data_marks
from parts.login import get_url_page, web_ready, user_input, verify_code_input
from parts.logout import logout
from parts.trade_page import find_trade_tag, buy_load_stocks

# 获取文件数据
data = read_file_data()
data_mark = find_data_marks(data)
# 获取上次标记点
current_marks = data_mark['current index']
if not current_marks.isdigit():
    current_marks = 0

total_count = data_mark["total count"]
# 准备开启浏览器
driver = setting.DRIVER
# 前往页面
driver = get_url_page(driver)

for i in range(current_marks, total_count):
    element = web_ready(driver)
    if element is False:
        os._exit()
    else:
        username, password, password2 = get_user_info(df=data, index=i)

        user_input(driver=driver, username=username, password=password)
        verify_code_input(driver=driver)

        element.click()

        find_trade_tag(driver=driver)
        buy_load_stocks(driver=driver, df=data, index=i)
        logout(driver)
