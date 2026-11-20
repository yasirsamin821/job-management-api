from app.tasks.csv_tasks import concurrency_demo

result = concurrency_demo.apply_async(args=[999])

print("Task ID:", result.id)

input("Press Enter to revoke the task...")

result.revoke()

print("Task revoked!")