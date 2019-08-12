from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

from apps.basic import Basic
from apps.login import Login
from parts.data_read_write import record_data

logging.basicConfig(level=logging.WARN,
                    filename='output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class BuyStock():

    def find_trade_tag(self):
        """登录后找交易点击"""
        url_check = None
        try:
            trade_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "交易")))
        except Exception as e:
            logging.exception(e)

        url_check.click()

    def buy_load_stocks(self, df, index):
        url_check = None
        try:
            url_check = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "买 (重消贷款)")))
        except Exception as e:
            logging.exception(e)

        url_check.click()

        # 抓取数值
        elements = self.driver.find_element_by_xpath("//input[@name='Amount'][@type='TEXT']")

        # 重消股数量
        stock_value = elements.get_attribute('value')
        record_data(df=df, index=index, stocks=stock_value)

        # 判断是否为数值
        try:
            stock_value = float(stock_value)
        except:
            stock_value = 0
        finally:

            if stock_value > 2:
                self.driver.find_element_by_xpath("//input[@class='button'][@type='SUBMIT']").click()
                # 点击完毕
                url_check_2 = None
                try:
                    url_check_2 = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@class='button'][@type='BUTTON'][@value=' 完毕 ']")))
                except Exception as e:
                    logging.exception(e)

                # 执行完后，跳转页面既是完成交易页面
                url_check_2.click()






