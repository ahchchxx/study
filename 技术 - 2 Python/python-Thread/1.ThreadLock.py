import threading
import time

def run(n):
    lock.acquire()
    global num
    num += 1
    #time.sleep(1)在上锁的情况不要使用sleep，不然会等50s才会完成
    lock.release()
	
lock = threading.Lock()
num = 0
start_time = time.time()
t_objs = []
for i in range(50):
    t = threading.Thread(target = run,args = ("t-%s" %i,))
    t.start()
    t_objs.append(t)
	
for t in t_objs:
    t.join()
	
print("-----all threads has finished....",threading.current_thread(),threading.active_count())

print("num = ", num)
