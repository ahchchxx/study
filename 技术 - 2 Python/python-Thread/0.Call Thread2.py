import threading
import time

def run(n):
    global num
    num += 1
    print("task running ", n, num,  time.time())
    #time.sleep(1)
    #print("task finished", n, time.time())

# 直接调用
start_time = time.time()
num = 0
for i in range(100):
	t1 = threading.Thread(target = run, args = ("t-%s"%i,))
	t1.start()

print('time cost:', time.time() - start_time, num)
