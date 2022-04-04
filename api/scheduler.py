import logging
import os

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('DB_HOST')
name = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

db_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"

# Настройки планировщика
jobstores = {
    "default": SQLAlchemyJobStore(db_url)
    }
executors = {
    "threadpool": ThreadPoolExecutor(max_workers=20)
    }
job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'replace_existing': True
}


def add_job(job, date, *args):
    sched = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
        )
    job_id = sched.add_job(job, 'date', run_date=date, args=args).id
    logging.warning(f'create job {job_id}', timezone.now())
    sched.start()
    return job_id


def modify_job(date, job_id, *args):
    sched = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
        )
    logging.warning(f'edit job {job_id}', timezone.now())
    sched.modify_job(job_id=job_id, run_date=date, args=args)
    sched.start()


def remove_job(job_id):
    sched = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
        )
    logging.warning(f'remove job {job_id}', timezone.now())
    sched.remove_job(job_id=job_id)


def get_job(job_id):
    sched = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
        )
    return sched.get_job(job_id)


def pause_job(job_id):
    sched = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
        )
    return sched.pause_job(job_id)


def resume_job(job_id):
    sched = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
        )
    return sched.pause_job(job_id)
