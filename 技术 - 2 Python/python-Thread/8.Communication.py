from multiprocessing import Process,Queue

def f(q2):
    q2.put([42, None, 'Hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())