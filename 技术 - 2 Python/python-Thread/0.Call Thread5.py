import threading
import time

# Semaphore(信号量)
# 互斥锁同时只允许一个线程更改数据，而Semaphore是同时允许一定数量的线程更改数据，
# 如有3个座位，最多允许3个人同时在座位上，后面的人只能等到有人起来才能够坐进去

def run(n):
    global num
    semaphore.acquire()
    num +=1
    print("task running ", n, num,  time.time())
    time.sleep(1)
    print("task finished ", n, num, time.time())
    semaphore.release()

# 直接调用
start_time = time.time()
if __name__ == '__main__':
	num = 0
	semaphore = threading.BoundedSemaphore(5)
	for i in range(30):
		t1 = threading.Thread(target = run, args = ("t-%s"%i,))
		t1.start()

while threading.active_count() > 1:
	pass
else:
	print('all finished', num)
	print('time cost:', time.time() - start_time)

# 一次性执行 5 个线程