from multiprocessing import Process,Pipe

def f(connSon, receiver):
    print(receiver.recv())
    connSon.send([42,None,'Hello from child'])
    connSon.close()
	
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()#生成一个管道实例，会返回两个对象，相当于管道的两头
    receiver, sender = Pipe()
    #parent_conn.send([42, None, 'Hello from Parent'])
    sender.send([42, None, 'Hello from Parent'])
    p = Process(target=f,args=(child_conn, receiver))
    p.start()
	
    print(parent_conn.recv())
    p.join()