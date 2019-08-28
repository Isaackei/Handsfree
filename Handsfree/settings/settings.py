

from gui.middle_transfer import filename_list

DRIVER = 'D:/testing/chromedriver_win32/chromedriver.exe'

URL = 'http://e-wbs.biz/'
# URL = 'http://www.google.com/'
# URL = "http://www.baidu.com"

WEB_WAIT_TIME = 12

TOTAL_NUMBER_OF_REFRESH = 5


# OPEN_FILE_NAME = "WBS.xls"
# OPEN_FILE_NAME = "D:/testing/apps/WBS208_1020_53_16.xls"

OPEN_FILE_NAME = filename_list[0]
# OPEN_FILE_NAME = "D:/testing/Handsfree/Handsfree/apps/WBS.xls"
# OPEN_FILE_NAME = "D:/WBSxls"

SAVE_FILE_NAME = ":/WBS2{}.xls"