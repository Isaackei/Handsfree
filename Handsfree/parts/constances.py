import datetime
import os

dt = datetime.datetime.now().strftime('%m_%d%H_%M_%S')

RAW_FILE_NAME = "WBS.xls"

REFORMAT_FILE_NAME = "WBS2{}.xls".format(dt)
