import threading, queue
import time, random

class counter:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0

    def increment(self):
        self.lock.acquire() # critical 
        self.value = value = self.value + 1
        self.lock.release()
        return value
    
_counter = counter()

class Worker(threading.Thread):
    def run(self): # inherit the function from threading.Thread class
         for i in range(10):
            value = _counter.increment()
            time.sleep(random.randint(10, 100) / 1000)
            print(self.getName(), "-- task", i, "finished", value)

"""for i in range(10):
    Worker.start()
"""

q = queue.Queue()
def consumer():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()
# threads are running back
threading.Thread(target=consumer, daemon=True).start()

for item in range(30):
    q.put(item)

print('All task requests sent\n', end='')
# block(wait) till all items were done
q.join()
print("all items are succesufly done")



