import threading
import time

def run(n):
    print("task ", n,  time.time())
    time.sleep(1)
    print("task finished ", n, time.time())

# 直接调用
start_time = time.time()
for i in range(50):
	t1 = threading.Thread(target = run, args = ("t-%s"%i,))
	# 守护进程
	t1.setDaemon(True)
	t1.start()

print('all finished')
print('time cost:', time.time() - start_time)

# 运行结果：子线程task finished都没有运行，主线程结束之后，所有子线程都强制结束