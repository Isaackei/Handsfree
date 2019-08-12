# import logging
#
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# from apps.basic import Basic
# from parts.data_read_write import record_data
#
#
# class LoginMixin(Basic):
#     """针对页面登录"""
#
#     def account_input(self, username=None, password=None):
#         """账号密码输入"""
#         self.driver.find_element_by_css_selector("td>input").send_keys(username)
#         self.driver.find_element_by_css_selector("[type='password']").send_keys(password)
#
#     def verify_code_input(self):
#         """验证码输入"""
#         while True:
#             verify_code_list = []
#             compare_number = "123456"
#             count_diff = 0
#             for index in range(1, 7):
#                 num_n = self.driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
#                 verify_code_list.append(num_n)
#                 if num_n != compare_number[index - 1]:
#                     count_diff += 1
#
#             if count_diff > 0:
#                 break
#         # 第二次获取验证码，预防延迟
#         verify_code_real = ""
#         for index in range(1, 7):
#             verify_code_real += self.driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
#         self.driver.find_element_by_css_selector("[name='SKey']").send_keys(verify_code_real)
#
#
# class StockModeAMixin(Basic):
#     """重消股"""
#     def buy_load_stocks(self, df, index):
#         # 数值定位
#         elements = self.driver.find_element_by_xpath("//input[@name='Amount'][@type='TEXT']")
#
#         # 重消股数量
#         stock_value = elements.get_attribute('value')
#         record_data(df=df, index=index, stocks=stock_value)
#
#         # 判断是否为数值
#         try:
#             stock_value = float(stock_value)
#         except:
#             stock_value = 0
#         finally:
#             if stock_value > 2:
#                 self.driver.find_element_by_xpath("//input[@class='button'][@type='SUBMIT']").click()
#                 # 点击完毕
#                 url_check_2 = None
#                 try:
#                     url_check_2 = WebDriverWait(self.driver, 5).until(
#                         EC.element_to_be_clickable((By.XPATH, "//input[@class='button'][@type='BUTTON'][@value=' 完毕 ']")))
#                 except Exception as e:
#                     logging.exception(e)
#
#                 # 执行完后，跳转页面既是完成交易页面
#                 url_check_2.click()
