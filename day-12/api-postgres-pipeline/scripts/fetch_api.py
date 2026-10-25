
import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_posts():
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()

        posts = response.json()

        if not isinstance(posts, list):
            raise ValueError("Expected a list of posts")

        print("API fetch successful!")
        print("Total records:", len(posts))
        print("First record:", posts[0] if posts else "No records")

        return posts

    except requests.RequestException as error:
        print("API request failed:", error)
        raise

    except ValueError as error:
        print("Invalid JSON response:", error)
        raise


if __name__ == "__main__":
    fetch_posts()
