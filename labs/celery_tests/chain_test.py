from celery import chain
from app.tasks.csv_tasks import (
    validate_csv_task,
    extract_records_task,
    generate_report_task
)

workflow = chain(
    validate_csv_task.s("sample.csv"),
    extract_records_task.s(),
    generate_report_task.s()
)

result = workflow.apply_async()

print("Workflow ID:", result.id)