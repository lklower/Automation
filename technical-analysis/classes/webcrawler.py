import threading
import time
from threading import Thread, Lock
from queue import Queue


class Crawler(Thread):

    def __init__(self, data: Queue, lock: Lock, report: dict[str, list], *args, **kwargs):
        self.url = None
        self.lock = lock
        self.queue = data
        self.report = report

        Thread.__init__(self, *args, **kwargs)

    def run(self):
        while self.queue.empty() is False:

            self.lock.acquire()
            url = self.queue.get()
            self.lock.release()

            if url is None:
                break

            self.url = url
            # print(f'{threading.current_thread().name} - {self.url}')
            self.queue.task_done()
