import ddt
import  unittest
test_data1 = [{"username": "zhangsan", "pwd": "zhangsan"},
              {"username": "lisi", "pwd": "lisi"},
              {"username": "wangwu", "pwd": "wangwu"},
              ]
@ddt.ddt
class Test1(unittest.TestCase):

    @staticmethod
    def func():
        @ddt.data(*test_data1)
        def f(self,data):
            print(data)
        return f

def gen_case():
    setattr(Test1,"test_ddt",Test1.func())

print(dir(Test1))

if __name__ == "__main__":
    unittest.main()

