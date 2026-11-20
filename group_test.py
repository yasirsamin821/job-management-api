from celery import group
from app.tasks.csv_tasks import process_file

workflow = group(
    process_file.s("file_a.csv"),
    process_file.s("file_b.csv"),
    process_file.s("file_c.csv")
)

result = workflow.apply_async()

print("Group ID:", result.id)