import multiprocessing as mp
import os
import threading


class Test2:

    def __init__(self,value,data):
        self.value = value
        self.data = data
   
    def to_dict(self):
        return {"value": self.value, "data": self.data}

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict["value"], data_dict["data"])


def update_value(shared_dict, lock):
    with lock:
        obj = Test2.from_dict(dict(shared_dict))  # Convert shared_dict to an object
        obj.value += 10
        shared_dict.update(obj.to_dict())  # Save changes


def print_values(shared_dict,lock):
    with lock:
        obj = Test2.from_dict(dict(shared_dict))
        print(obj.value)
        print(obj.data)
class Test:

    def __init__(self,manager):
        self.value = manager.Value('i',1)
        self.lock = mp.Lock()
        self.test2_instance = manager.dict(Test2(1,5).to_dict())


    def test(self,id):
        print(f'Old PID {os.getpid()}')
        print_values(self.test2_instance,lock=self.lock)
        update_value(shared_dict=self.test2_instance,lock=self.lock)
        print(f'New PID {os.getpid()}')
        print_values(self.test2_instance,lock=self.lock)
        
        

if __name__ == '__main__':
    with mp.Manager() as manager:
        # t2_shared_instance = manager.dict(Test2(1,5).to_dict())
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

