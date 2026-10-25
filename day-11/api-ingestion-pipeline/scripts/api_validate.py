import requests

URL = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Expected a list of posts")

    if not data:
        raise ValueError("API returned an empty list")

    required_fields = {"userId", "id", "title", "body"}

    for index, post in enumerate(data):
        if not isinstance(post, dict):
            raise ValueError(f"Record {index} is not an object")

        missing_fields = required_fields - post.keys()

        if missing_fields:
            raise ValueError(
                f"Record {index} missing fields: {missing_fields}"
            )

    print("API status:", response.status_code)
    print("Validation: SUCCESS")
    print("Total records:", len(data))

except (requests.exceptions.RequestException, ValueError) as error:
    print("Validation failed:", error)