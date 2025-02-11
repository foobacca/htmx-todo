import time
from random import random
from threading import Thread




class Archiver:
    archive_status = "Waiting"
    archive_progress = 0
    thread = None
    _instance = None

    @property
    def status(self):
        return Archiver.archive_status

    def progress(self):
        return Archiver.archive_progress

    def progress_percent(self):
        return int(Archiver.archive_progress * 100)

    def run(self):
        if Archiver.archive_status == "Waiting":
            Archiver.archive_status = "Running"
            Archiver.archive_progress = 0
            Archiver.thread = Thread(target=self.run_impl)
            Archiver.thread.start()

    def run_impl(self):
        for i in range(10):
            time.sleep(1 * random())
            if Archiver.archive_status != "Running":
                return
            Archiver.archive_progress = (i + 1) / 10
            print("Here... " + str(Archiver.archive_progress))
        time.sleep(1)
        if Archiver.archive_status != "Running":
            return
        Archiver.archive_status = "Complete"

    def archive_file(self):
        return 'todos.json'

    def reset(self):
        Archiver.archive_status = "Waiting"

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = Archiver()
        return cls._instance

