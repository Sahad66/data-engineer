
def transform_posts(posts):
    clean_posts = []
    rejected_posts = []

    for record in posts:
        try:
            post_id = record["id"]
            user_id = record["userId"]
            title = record["title"]
            body = record["body"]

            # bool is a subclass of int in Python,
            # so reject booleans explicitly.
            if (
                isinstance(post_id, bool)
                or not isinstance(post_id, int)
                or post_id <= 0
            ):
                raise ValueError("Invalid post ID")

            if (
                isinstance(user_id, bool)
                or not isinstance(user_id, int)
                or user_id <= 0
            ):
                raise ValueError("Invalid user ID")

            if not isinstance(title, str) or not title.strip():
                raise ValueError("Missing title")

            if not isinstance(body, str) or not body.strip():
                raise ValueError("Missing body")

            clean_posts.append({
                "post_id": post_id,
                "user_id": user_id,
                "title": title.strip(),
                "body": body.strip(),
            })

        except (KeyError, TypeError, ValueError) as error:
            rejected_posts.append({
                "record": record,
                "reason": str(error),
            })

    print("Valid records:", len(clean_posts))
    print("Rejected records:", len(rejected_posts))

    return clean_posts, rejected_posts
