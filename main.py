import multiprocessing as mp
import threading


class Test:

    def __init__(self):
        self.value = 1
        self.lock = mp.Lock()

    def update_value(self,value):
        self.value = value

    def print_value(self):
        return self.value


    def test(self,id):
        # self.lock.acquire()
        print(f'Old value {id}: {self.print_value()}')
        self.update_value(id)
        print(f'New value {id}: {self.print_value()}')
        # self.lock.release()


if __name__ == '__main__':
    test = Test()

    threads = []
    for _ in range(5):  # Limit the number of threads
        t1 = mp.Process(target=test.test, args=(50,))
        t2 = mp.Process(target=test.test, args=(100,))
        threads.append(t1)
        threads.append(t2)

    for t in threads:
        t.start()

    for t in threads:
        t.join() 

