class A(object):

    def test1(self, tar):
        tar.test2()


class B(object):

    def test2(self):
        print("B")

a = A()
b = B()
a.test1(tar=b)