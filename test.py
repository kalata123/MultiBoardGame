import threading
import time

def run():
    while True:
        print('thread running')
        global stop_threads
        if stop_threads:
            break

stop_threads = False
t1 = threading.Thread(target = run)
t1.start()
# Button(25).wait_for_press()
stop_threads = True
t1.join()
print('thread killed')
