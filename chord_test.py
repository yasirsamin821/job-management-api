from celery import chord
from app.tasks.csv_tasks import process_file, combine_results

workflow = chord(
    [
        process_file.s("file_a.csv"),
        process_file.s("file_b.csv"),
        process_file.s("file_c.csv")
    ],
    combine_results.s()
)

result = workflow.apply_async()

print("Chord ID:", result.id)