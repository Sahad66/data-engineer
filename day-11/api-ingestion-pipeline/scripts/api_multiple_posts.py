import requests

url = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    posts = response.json()

    print("Total posts:", len(posts))

    for post in posts[:5]:
        print(
            "ID:", post["id"],
            "| User ID:", post["userId"],
            "| Title:", post["title"]
        )

except requests.exceptions.RequestException as error:
    print("API request failed:", error)