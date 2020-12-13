from multiprocessing import Process,Lock

def f(l,i):
    l.acquire()
    try:
        print("hello world ",i)
    finally:
        l.release()

def f1(i):
    print('hi ', i)

if __name__ == '__main__':
    lock = Lock()
    for num in range(10):
        p = Process(target=f, args=(lock, num))
        p.start()
        p.join()

        p1 = Process(target=f1, args=(num,))
        p1.start()
        #p1.join()
