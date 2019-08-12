
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging


def logout(driver):
    """退出账号"""
    url_check = None
    try:
        url_check = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "退出")))
    except Exception as e:
        logging.exception(e)

    url_check.click()

    url_check_2 = None
    try:
        url_check_2 = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "是")))
    except Exception as e:
        logging.exception(e)

    url_check_2.click()
