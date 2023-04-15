import psutil
import datetime
import logging

from .configuration import get_datafile

logger = logging.getLogger(__name__)


class Tracker:
    def __init__(self, pid, name):
        logger.debug('Tracker.__init__')

        self.name = name
        self.pid = pid
        self.proc = psutil.Process(self.pid)
        self.term = self.proc.parent()
        self.procs = {}
        logger.debug(f'Tracker.pid ={self.pid}')
        logger.debug(f'Tracker.proc={self.proc}')
        logger.info(f'Tracker.term={self.term}')
        logger.debug('Tracker.__init__ done')

    def get_procs(self):
        children = self.term.children()
        logger.debug(f'Tracker.get_procs: {len(children)} procs found')

        for proc in children:
            if proc.pid == self.pid:
                continue
            if proc.pid not in self.procs:
                self.procs[proc.pid] = proc

        logger.debug('Tracker.get_procs: done')

    def report(self):
        now = datetime.datetime.now()
        logger.debug(f'Tracker.report: {now}')

        data_file = get_datafile(self.name)
        if not data_file.is_file():
            data_file.touch()
    
        with open(data_file, 'a') as df:
            for pid, proc in self.procs.items():
                status = 'alive' if proc.is_running() else 'dead'
                df.write(f'{pid} {now} {status}\n')

        self.procs = {
            pid: proc 
            for pid, proc in self.procs.items() 
            if proc.is_running()
        }

        logger.debug('Tracker.report: done')

    def finish(self, exit_code):
        now = datetime.datetime.now()
        data_file = get_datafile(self.name)
        if not data_file.is_file():
            data_file.touch()
    
        with open(data_file, 'a') as df:
            df.write(f'exit {now} {exit_code}\n')
