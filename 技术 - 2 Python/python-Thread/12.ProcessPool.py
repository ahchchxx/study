from multiprocessing import Process,Pool
import time,os

def Foo(i):
    time.sleep(0.1)
    print('in the process ', os.getpid())
    return i+100  # 作为回调函数的入参

def Bar(arg):
    print('--->exec done:', arg)

if __name__ == '__main__':
    pool = Pool(5)

    for i in range(10):
        pool.apply_async(func=Foo, args=(i,), callback=Bar)
        #pool.apply(func=Foo, args=(i,))
    print("end")
    pool.close()
	
	# 异步情况下
	# 在进程池中进程执行完毕后，再关闭。如果注释，那么程序直接关闭
    pool.join()
