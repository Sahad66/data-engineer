import requests

URL = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    posts = response.json()

    transformed_posts = []

    for post in posts:
        post_id = post.get("id")
        user_id = post.get("userId")
        title = post.get("title")
        body = post.get("body")

        if not isinstance(post_id, int) or post_id <= 0:
            continue

        if not isinstance(user_id, int) or user_id <= 0:
            continue

        if not isinstance(title, str) or not title.strip():
            continue

        if not isinstance(body, str) or not body.strip():
            continue

        transformed_record = {
            "post_id": post_id,
            "user_id": user_id,
            "title": title.strip(),
            "title_length": len(title.strip()),
            "body_length": len(body.strip()),
        }

        transformed_posts.append(transformed_record)

    print("Transformed records:", len(transformed_posts))
    print("First transformed record:")
    print(transformed_posts[0] if transformed_posts else "No records")

except (requests.exceptions.RequestException, ValueError) as error:
    print("Transformation failed:", error)