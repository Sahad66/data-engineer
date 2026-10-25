import requests

URL = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    posts = response.json()

    clean_posts = []
    rejected_posts = []

    for post in posts:
        post_id = post.get("id")
        user_id = post.get("userId")
        title = post.get("title")
        body = post.get("body")

        valid_id = (
            isinstance(post_id, int)
            and not isinstance(post_id, bool)
            and post_id > 0
        )

        valid_user = (
            isinstance(user_id, int)
            and not isinstance(user_id, bool)
            and user_id > 0
        )

        valid_title = (
            isinstance(title, str)
            and bool(title.strip())
        )

        valid_body = (
            isinstance(body, str)
            and bool(body.strip())
        )

        if valid_id and valid_user and valid_title and valid_body:
            clean_posts.append(post)
        else:
            rejected_posts.append(post)

    print("Raw records:", len(posts))
    print("Clean records:", len(clean_posts))
    print("Rejected records:", len(rejected_posts))

except (requests.exceptions.RequestException, ValueError) as error:
    print("Cleaning failed:", error)