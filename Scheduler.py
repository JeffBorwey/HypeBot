import time
from time import mktime
import parsedatetime
from threading import Thread
from datetime import datetime


class Scheduler(Thread):

    def __init__(self):
        super(Scheduler, self).__init__()
        self.cal = parsedatetime.Calendar()
        self.jobs = set()

    def run(self):
        print('Scheduler enabled')
        while 1:
            finished_jobs = list()
            for job in self.jobs:
                if job.run():
                    finished_jobs.append(job)
            for job in finished_jobs:
                self.jobs.remove(job)
            time.sleep(5)

    def schedule_job(self, schedule_string, job):
        time_struct, parse_status = self.cal.parse(schedule_string)
        dt = datetime.fromtimestamp(mktime(time_struct))
        self.jobs.add(SchedulerJob(dt, job))
        print('Job Scheduled with string ' + schedule_string)


class SchedulerJob:

    def __init__(self, dt, job):
        self.fire_date_time = dt
        self.run_job = job

    def run(self):
        if self.fire_date_time <= datetime.now():
            self.run_job()
            return True
        return False
