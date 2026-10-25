import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url, timeout=10)

    response.raise_for_status()

    data = response.json()

    print("SUCCESS: API data received")
    print("Status code:", response.status_code)
    print("Post ID:", data["id"])
    print("Title:", data["title"])

except requests.exceptions.Timeout:
    print("FAILURE: API request timed out")

except requests.exceptions.HTTPError as error:
    print("FAILURE: HTTP error:", error)

except requests.exceptions.RequestException as error:
    print("FAILURE: Network or request error:", error)