from multiprocessing import Process,Manager
import os

def f(d,l):
    d[os.getpid()] = os.getpid()
    l.append(os.getpid())
    print(l)

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()#生成一个字典，生成一个可在多个进程之间传递和共享的字典
        l = manager.list(range(5))
        p_list = []
        for i in range(5):
            p = Process(target=f,args=(d,l))
            p.start()
            p_list.append(p)
        for res in p_list:#等待结果
            res.join()

        print(d)
        print(l)