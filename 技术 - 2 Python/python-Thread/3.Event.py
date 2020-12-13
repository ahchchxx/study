import threading
import time

event = threading.Event()
def lighter():
    count = 0
    event.set()#一开始先设成绿灯
    while True:
        if count > 5 and count <=10 :#改成红灯
            event.clear()#清空标志位
            # print("\033[41;1mred light is on ...\033[0m")
            print("xxxxxx -- red light is on ...", count)
        elif count > 10:  # =11
            event.set()#变绿灯
            # print("\033[42;1mgreen light is on ...\033[0m")
            print("√√√ -- green light is on ...", count)
            count = 0
        else:
            # print("\033[42;1mgreen light is on ...\033[0m")
            print("green light is on ...", count)
        time.sleep(1)
        count += 1
		
def car(name):
    while True:
        if event.is_set():#代表绿灯
            print("[%s] running..." %name)
            time.sleep(1)
        else:
            print("[%s] sees red light,waiting..." %name)
            event.wait()
            print("[%s] green light is on, start going ..." %name)

light = threading.Thread(target = lighter,)
light.start()

car1 = threading.Thread(target = car,args=("Tesla",))
car1.start()
