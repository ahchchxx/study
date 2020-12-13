import threading,time
import queue

q = queue.Queue(maxsize = 10)
def Producer(name):
    count = 1
    while True:
        q.put("骨头:%s" %count)
        print("生产了骨头:", count)
        count += 1
        #time.sleep(0.5) # 供需平衡
        time.sleep(1)

def Consumer(name):
    while True:
        if q.qsize() > 0:
            print("\t[%s] 取到吃的 [%s]" %(name, q.get()))
        else:
            #print("\t" + name, " 没有吃的~")
            print("\t[%s] 没有吃的 ~" %name)
        time.sleep(1)

p = threading.Thread(target = Producer, args=("Producer",))
c = threading.Thread(target = Consumer, args=("Consumer1",))
c1 = threading.Thread(target = Consumer,args=("Consumer2",))
p.start()
c.start()
c1.start()