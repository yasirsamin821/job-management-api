import csv
import os
from datetime import datetime, timezone

from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.processing_job import ProcessingJob

@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def process_csv(self, file_path):
    db = SessionLocal()

    job = db.query(ProcessingJob).filter(
        ProcessingJob.task_id == self.request.id
    ).first()

    try:
        if job and job.status == "SUCCESS":
            print('Task already completed. Skipping execution')
            return job.result
        if job:
            job.status = "STARTED"
            job.error = None
            db.commit()
        if not os.path.exists(file_path):
            raise FileNotFoundError("CSV file not found")

        if os.path.getsize(file_path) == 0:
            raise ValueError("CSV file is empty")

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV file has no headers")

            if any(not column.strip() for column in reader.fieldnames):
                raise ValueError("CSV contains empty column names")

            records = list(reader)

        result = {
            "filename": os.path.basename(file_path),
            "total_records": len(records),
            "columns": reader.fieldnames
        }

        if job:
            job.status = "SUCCESS"
            job.result = result
            job.error = None
            job.completed_at = datetime.now(timezone.utc)
            db.commit()

        return result

    except (ConnectionError, TimeoutError) as exc:
        if self.request.retries < self.max_retries:
            if job:
                job.status = "RETRY"
                job.error = str(exc)
                db.commit()

            raise self.retry(exc=exc)

        if job:
            job.status = "FAILURE"
            job.error = str(exc)
            job.completed_at = datetime.now(timezone.utc)
            db.commit()

        raise

    except Exception as exc:
        if job:
            job.status = "FAILURE"
            job.error = str(exc)
            job.completed_at = datetime.now(timezone.utc)
            db.commit()

        raise

    finally:
        db.close()


import time

@celery_app.task
def concurrency_demo(task_number):
    start = datetime.now(timezone.utc)

    print(f"Task {task_number} started at {start}")

    time.sleep(10)

    end = datetime.now(timezone.utc)

    return {
        "task_number": task_number,
        "worker_pid": os.getpid(),
        "started_at": start.isoformat(),
        "finished_at": end.isoformat()
    }

import time

@celery_app.task(bind=True)
def crash_demo(self):
    print(f"Task started: {self.request.id}")
    print(f"Delivery information: {self.request.delivery_info}")

    time.sleep(60)

    print("Task finished successfully")

    return {"message": "Task completed"}

from celery.exceptions import SoftTimeLimitExceeded

@celery_app.task(soft_time_limit=5, time_limit=10)
def time_limit_demo():
    try:
        time.sleep(15)
        return "Completed"
    except SoftTimeLimitExceeded:
        print("Soft time limit exceeded!")
        raise

@celery_app.task(bind=True, max_retries=3, default_retry_delay=3)
def permanent_failure_demo(self):
    print(f"Attempt: {self.request.retries + 1}")

    raise self.retry(
        exc=ConnectionError("Database unavailable")
    )

@celery_app.task(
    bind=True,
    max_retries=4,
    autoretry_for=(ConnectionError,),
    retry_backoff=2,
    retry_backoff_max=30,
    retry_jitter=True
)
def exponential_backoff_demo(self):
    print(f"Attempt: {self.request.retries + 1}")
    raise ConnectionError("Service unavailable")


@celery_app.task
def validate_csv_task(filename):
    print("Validating CSV...")
    return filename


@celery_app.task
def extract_records_task(filename):
    print("Extracting records...")
    return {"filename": filename, "records": 100}


@celery_app.task
def generate_report_task(data):
    print("Generating report...")
    return {
        "filename": data["filename"],
        "total_records": data["records"],
        "status": "Report generated"
    }

@celery_app.task
def process_file(filename):
    print(f"Processing {filename}")

    return {
        "filename": filename,
        "status": "completed"
    }

@celery_app.task
def combine_results(results):
    print("Combining results...")

    return {
        "total_files": len(results),
        "files": results
    }