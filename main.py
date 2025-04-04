import multiprocessing as mp
import os
import threading


class Test2:

    def __init__(self,manager,lock):
        self.value = manager.Value('i',1)
        self.lock = lock
        self.data = manager.Value('i',5)


    def print_value(self):
        return self.value.value
    
    def update_value(self,value):
        self.lock.acquire()
        self.value.value = value
        self.lock.release()


    def print_data(self):
        return self.data.value
    
    def update_data(self,value):
        self.data.value = value

class Test:

    def __init__(self,manager):
        self.value = manager.Value('i',1)
        self.lock = mp.Lock()
        self.test2_instance = Test2(manager,self.lock)


    def test(self,id):
        print(f'Old value {os.getpid()}: {self.test2_instance.print_value()}')
        value = self.test2_instance.print_value()
        self.test2_instance.update_value(value + 10)
        print(f'New value {os.getpid()}: {self.test2_instance.print_value()}')
        print(f'Old Data {os.getpid()}: {self.test2_instance.print_data()}')
        data = self.test2_instance.print_data()
        self.test2_instance.update_data(data + 10)
        print(f'New value {os.getpid()}: {self.test2_instance.print_data()}')

if __name__ == '__main__':
    with mp.Manager() as manager:
        test = Test(manager)
        threads = []
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

