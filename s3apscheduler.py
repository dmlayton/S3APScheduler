from boto.provider import Provider
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore
from shove import Shove
import logging
SHOVE_BUCKET = 'my-bucket'

class ShoveJobStore(ShelveJobStore):

    def __init__(self, path):
        self.jobs = []
        self.path = path
        self.store = Shove(path, optimize=False)


class S3JobStore(ShoveJobStore):

    def __init__(self, access_key, secret_key, bucket, prefix='job_'):
        self.prefix = prefix if prefix[-1] == '/' else (prefix + '/')
        path = 's3://{}:{}@{}'.format(access_key, secret_key, bucket)
        super(S3JobStore, self).__init__(path)


logging.basicConfig()
PROVIDER = Provider('aws')
JOB_STORE = S3JobStore(PROVIDER.get_access_key(), PROVIDER.get_secret_key(), SHOVE_BUCKET)
SCHEDULER = Scheduler(misfire_grace_time=1000)
SCHEDULER.add_jobstore(JOB_STORE, 's3')
