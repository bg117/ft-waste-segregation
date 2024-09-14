import time
import threading
from .EventWorker import EventWorker


class EventLoop(object):
    
    __instance = None

    @staticmethod   
    def getInstance():
        """ Static access method. """
        if EventLoop.__instance == None:
            EventLoop()
        return EventLoop.__instance


    def __init__(self):
        """ Virtually private constructor. """
        if EventLoop.__instance != None:
            raise Exception("This class is a Singleton!")
        else:
            EventLoop.__instance = self
            self.__lock = threading.Lock()
            self.__workers = []
            self.__running = True
            self.__thread = threading.Thread(target=self.__run_loop, daemon=True)
            self.__thread.start()


    def __del__(self):
        self.__running = False
        if self.__thread is not None:
            self.__thread.join()
        self.__workers = None

            
    def __run_loop(self): 
        while self.__running == True:
            time.sleep(0.01)
            with self.__lock:
                for worker in self.__workers:
                    worker.run()


    def __get_worker(self, target, property_name):
        for worker in self.__workers:
            if worker.target == target and worker.property_name == property_name:
                return worker
        return None

    
    def __has_worker(self, target, property_name):
        if self.__get_worker(target, property_name) is not None:
            return True
        return False


    def add_change_listener(self, target, property_name, callback):
        with self.__lock:
            worker = self.__get_worker(target, property_name)
            if worker is not None:
                if worker.callback == callback:
                    return 
            
            # create new worker instance for property of target
            worker = EventWorker(target, property_name, callback)
            self.__workers.append(worker)


    def remove_change_listener(self, target, property_name, callback):   
        with self.__lock:   
            worker = self.__get_worker(target, property_name)
            if worker is None:
                return
            if worker.callback != callback:
                return  
            # remove worker if no listeners available
            self.__workers.remove(worker)
