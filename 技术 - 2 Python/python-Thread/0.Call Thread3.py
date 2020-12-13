import threading
import time

def run(n):
    print("task ", n,  time.time())
    time.sleep(1)
    print("task finished ", n, time.time())

# 直接调用
start_time = time.time()
t_objs = []
for i in range(50):
	t1 = threading.Thread(target = run, args = ("t-%s"%i,))
	t1.start()
	t_objs.append(t1)

for t in t_objs:
	t.join()

print('all finished')
print('time cost:', time.time() - start_time)
