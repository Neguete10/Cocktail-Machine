import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class Watcher:
    DIRECTORY_TO_WATCH = "./"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        if event.src_path.endswith(".py"):
            print(f"File modified: {event.src_path}")
            os.system(f"python {event.src_path}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
