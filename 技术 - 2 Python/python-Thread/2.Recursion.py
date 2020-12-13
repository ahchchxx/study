import threading,time

# 相当于先进入run3这个大门，然后在进入run1和run2这个两个小门，
# 然后进行num1和num2的加1，保证了每个线程的执行都是串行的

def run1():
    print("grab the first part data")
    lock.acquire()
    global num
    num += 1
    lock.release()
    return num

def run2():
    print("grab the second part data")
    lock.acquire()
    global num2
    num2 += 1
    lock.release()
    return num2

def run3():
    lock.acquire()
    res = run1()
    print('------between run1 and run2')
    res2 = run2()
    lock.release()
    print(res, res2)

num,num2 = 0,0
lock = threading.RLock()
print("\n\n--threading.active_count: " + str(threading.active_count()) + '\n')
for i in range(5):
    t = threading.Thread(target=run3)
    t.start()

# while threading.active_count() != 1:
while threading.active_count() > 1:
    print("\n\n--threading.active_count: " + str(threading.active_count()) + '\n')
else:
    print("----all threads done---")
    print(num, num2)
