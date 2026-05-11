from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "A", "content": "This is the first post."},
    {"id": 2, "title": "D", "content": "This is the second post."},
    {"id": 3, "title": "B", "content": "This is the third post."},
]



SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/posts', methods=['GET'])
def get_sorted_posts():
    """
    Return a list of posts.
    list can be sorted by title or content
    ascending or descending.
    """
    sort = request.args.get('sort')          # "title" or "content"
    direction = request.args.get('direction') # "asc" or "desc"

    result = POSTS.copy()

    if sort in ["title", "content"]:
        reverse = False

        if direction == "desc":
            reverse = True

        result = sorted(result, key=lambda x: x[sort].lower(), reverse=reverse)

    return jsonify(result)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete existing post.
    Return an error message if post not found.
    """

    post_to_delete = None
    for post in POSTS:
        if post["id"] == post_id:
            post_to_delete = post
            break

    if post_to_delete is None:
        return jsonify({
            "error": "Post not found",
            "id": post_id
        }), 404

    POSTS.remove(post_to_delete)

    return jsonify({
        "message": f"Post with id {post_id} has been deleted successfully."
    }), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Upddate existing posts.
    Return an error message if post not found.
    """
    data = request.get_json()

    post_to_update = None
    for post in POSTS:
        if post["id"] == post_id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({
            "error": "Post not found",
            "id": post_id
        }), 404

    if data:
        if "title" in data:
            post_to_update["title"] = data["title"]
        if "content" in data:
            post_to_update["content"] = data["content"]

    return jsonify({
        "id": post_to_update["id"],
        "title": post_to_update["title"],
        "content": post_to_update["content"]
    }), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Return all found posts.
    one can search by title or by content.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    results = []

    for post in POSTS:
        title_match = title_query in post["title"].lower()
        content_match = content_query in post["content"].lower()

        if title_query and title_match:
            results.append(post)
        elif content_query and content_match:
            results.append(post)
        elif not title_query and not content_query:
            results = POSTS
            break

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
