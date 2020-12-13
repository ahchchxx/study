from multiprocessing import Process,Pipe

def f(conn):
    conn.send([42,None,'Hello from child'])
    conn.close()
	
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()#生成一个管道实例，会返回两个对象，相当于管道的两头
    p = Process(target=f,args=(child_conn,))
    p.start()
	
    print(parent_conn.recv())
    p.join()