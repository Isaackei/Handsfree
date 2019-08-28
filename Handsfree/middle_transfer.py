#######################
# Global variables
filename_list = []
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


