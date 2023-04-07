import psutil
import datetime

from .configuration import CHECKS
from .configuration import get_logger


class Tracker:
    def __init__(self, pid):
        self.logger, fh = get_logger(pid, __name__)

        self.logger.debug('Tracker.__init__')
        self.pid = pid
        self.proc = psutil.Process(self.pid)
        self.term = self.proc.parent()
        self.procs = {}
        self.logger.debug(f'Tracker.proc={self.proc}')
        self.logger.debug(f'Tracker.term={self.term}')
        self.logger.debug('Tracker.__init__ done')

    def get_procs(self):
        children = self.term.children()
        self.logger.debug(f'Tracker.get_procs: {len(children)} procs found')

        for proc in children:
            if proc.pid == self.pid:
                continue
            if proc.pid not in self.procs:
                self.procs[proc.pid] = proc

        self.procs = {
            pid: proc 
            for pid, proc in self.procs.items() 
            if proc.is_running()
        }

        self.logger.debug('Tracker.get_procs: done')

    def report(self):
        now = datetime.datetime.now()
        self.logger.debug(f'Tracker.report: {now}')

        for pid in self.procs:
            data_file = CHECKS / f'{pid}.data'
            if not data_file.is_file():
                data_file.touch()
            with open(data_file, 'a') as df:
                df.write(f'{now} {self.procs[pid].name()} alive\n')

        data_files = CHECKS.glob('*.data')
        for file in data_files:
            pid = int(file.name.split('.')[0])
            if pid in self.procs:
                continue
            with open(file, 'a') as df:
                df.write(f'{now} dead\n')

        self.logger.debug('Tracker.report: done')
