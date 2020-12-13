import threading
import time

# 用类的方式启动线程。继承Thread
class MyThread(threading.Thread):
    def __init__(self,n):
        super(MyThread, self).__init__()
        self.n = n
    def run(self):
        print("running task ", self.n)

t1 = MyThread("t1")
t2 = MyThread("t2")
t1.start()
t2.start()