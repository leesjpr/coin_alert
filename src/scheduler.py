from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgoundScheduler
import time

class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''

    def __del__(self):
        self.sched.shutdown()


    def kill_scheduler(slef, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print "fail to stop scheduler: %s" % err
            return

    def scheduler(self, type, job_id, func):
        print "%s Scheduler Start" % type
        if type == 'interval':
            self.sched.add_job(func, type, seconds=10, id=job_id, args=(type, job_id))
        elif type == 'cron':
            pass
