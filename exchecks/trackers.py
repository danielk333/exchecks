import psutil
import threading


class Tracker:
    def watch(self):
        raise NotImplementedError('Implement this')

    def check(self):
        raise NotImplementedError('Implement this')

    def success(self):
        raise NotImplementedError('Implement this')


def psutil_wait(proc, result):
    result['exit_code'] = proc.wait()


class PS(Tracker):

    def __init__(self, name):
        self.pid = None
        self.name = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                self.pid = proc.info['pid']
                self.name = proc.info['name']
                break
        if self.pid is None:
            raise ValueError(f'Could not find "{name}" process')
        self.p = psutil.Process(self.pid)
        self.watcher = None
        self.result = {}
        self.watch()

    def watch(self):
        self.watcher = threading.Thread(
            target=psutil_wait, 
            args=(self.p, self.result),
        )
        self.watcher.start()

    def check(self):
        return self.watcher.is_alive()

    def success(self):
        self.watcher.join(timeout=3)
        return self.result['exit_code']
