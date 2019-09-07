#######################
# Global variables
filename_list = []
filename_list2 = []
method_tuple = None
#######################


def first_start_up(*args):
    global method_tuple
    method_tuple = args
    from apps.main import main_start
    main_start()


def second_start_up(*args):
    global filename_list
    filename_list.append(*args)


def second_start_up2(*args):
    global filename_list2
    filename_list2.append(*args)


