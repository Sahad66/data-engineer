import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url, timeout=10)

    response.raise_for_status()

    data = response.json()

    print("Status code:", response.status_code)
    print("User ID:", data["userId"])
    print("Post ID:", data["id"])
    print("Title:", data["title"])
    print("Body:", data["body"])

except requests.exceptions.Timeout:
    print("ERROR: Request timed out")

except requests.exceptions.HTTPError as error:
    print("HTTP ERROR:", error)

except requests.exceptions.RequestException as error:
    print("REQUEST ERROR:", error)