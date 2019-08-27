def test():

    print("start")
    return
    print("end")


def run():
    for i in range(5):
        print(i)
        test()
        print("="*10)

run()