import sys
import time

from app.tasks.csv_tasks import concurrency_demo

total_tasks = int(sys.argv[1]) if len(sys.argv) > 1 else 10

start = time.perf_counter()

tasks = [
    concurrency_demo.delay(i)
    for i in range(1, total_tasks + 1)
]

results = [
    task.get(timeout=600)
    for task in tasks
]

end = time.perf_counter()

print(f"\nTotal tasks: {total_tasks}")
print(f"Total execution time: {end - start:.2f} seconds")

processes = set(result["worker_pid"] for result in results)

print(f"Different worker processes: {len(processes)}")