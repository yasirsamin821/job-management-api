import requests
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzk1MTg1MjMwfQ.30TTxN8OP5pEA5ewXWD8uF_58HbaIliWLdRwII37OHI"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

def upload_file(number):
    with open("predictions.csv", "rb") as file:
        response = requests.post(
            f"{API_URL}/files/upload",
            headers=headers,
            files={"file": (f"test_{number}.csv", file, "text/csv")}
        )

    print(f"Upload {number}: {response.status_code}")

    return response.json()


with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(upload_file, range(10)))

print("\nSubmitted jobs:")

for result in results:
    print(result)