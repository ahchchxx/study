from multiprocessing import Process
import os

def info(title):
    print(title)
    print("module name:",__name__)
    print("parent process:", os.getppid())
    print("process id:", os.getpid())
    print("\n\n")

def f(name):
    info('called from child process function f')
    print("hello ", name)

if __name__ == '__main__':
    info('main process line')
    p = Process(target=f, args=('bob',))
    p.start()
    # p.join()