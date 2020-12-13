import queue
#class queue.Queue(maxsize = 0)先入先出
#class queue.LifoQuene(maxsize = 0)last in first out
#class queue.PriorityQueue(maxsize = 0)存储数据时可设置优先级的队列

#q = queue.Queue()
q = queue.LifoQueue()
q.put(1)
q.put(10)
q.put(100)
q.put("1000")

print(q.get(), q.get(), q.get(), q.get())
#print(q.get())


q = queue.PriorityQueue()
q.put((-1, 1))
q.put((1, 10))
q.put((100, 100))
q.put((2, "1000"))

print(q.get(), q.get(), q.get(), type(q.get()))
