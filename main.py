import multiprocessing as mp
import os
import threading


class Test:

    def __init__(self):
        self.value = mp.Value('i',1)
        self.lock = mp.Lock()
        self.queue = mp.Queue()

    def update_value(self,value):
        self.value.value = value

    def print_value(self):
        return self.value.value


    def test(self,id):
        self.lock.acquire()
        print(f'Old value {os.getpid()}: {self.print_value()}')
        value = self.queue.get() + 10
        self.update_value(value)
        print(f'New value {os.getpid()}: {self.print_value()}')
        self.queue.put(self.print_value())
        self.lock.release()


if __name__ == '__main__':
    test = Test()

    threads = []
    test.queue.put(10)
    print(mp.cpu_count())
    for _ in range(5):  # Limit the number of threads
        t1 = mp.Process(target=test.test, args=(50,))
        t2 = mp.Process(target=test.test, args=(100,))
        threads.append(t1)
        threads.append(t2)

    for t in threads:
        t.start()

    for t in threads:
        t.join() 

