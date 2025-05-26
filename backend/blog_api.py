# CRUD: Create, Read, Update, Delete
# For the blog aspect of the page

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# in memory database - for now
blogs = []
next_id = 1

# Create a Blog Post
@app.route('/blog', methods=['POST'])
def add_blog():
    global next_id

    data = request.json
    title = request.json['title']
    content = request.json['content']
    author = request.json['author']
    time_str = request.json['time']
    time = datetime.fromisoformat(time_str)

    new_blog = {
        'id': next_id,
        'title': title,
        'content': content,
        'author': author,
        'time': time
    }

    blogs.append(new_blog)
    next_id += 1

    response = new_blog.copy()
    response['time'] = time.isoformat()

    return jsonify(response)

# Get All Blog Posts
@app.route('/blog', methods=['GET'])
def get_blogs():
    result = []
    for blog in blogs:
        blog_copy = blog.copy()
        blog_copy['time'] = blog_copy['time'].isoformat()
        result.append(blog_copy)

    return jsonify(result)

# Get Single Blog Post
@app.route('/blog/<int:id>', methods=['GET'])
def get_blog(id):
    for blog in blogs:
        if blog['id'] == id:
            blog_copy = blog.copy()
            blog_copy['time'] = blog_copy['time'].isoformat()
            return jsonify(blog_copy)

    return jsonify({'message': 'Blog post not found'})

# Update a Blog Post
@app.route('/blog/<int:id>', methods=['PUT'])
def update_blog(id):
    for blog in blogs:
        if blog['id'] == id:
            data = request.json
            blog['title'] = data['title']
            blog['content'] = data['content']
            blog['author'] = data['author']
            blog['time'] = datetime.fromisoformat(data['time'])

            blog_copy = blog.copy()
            blog_copy['time'] = blog_copy['time'].isoformat()
            return jsonify(blog_copy)
        
        return jsonify({'message': 'Blog post not found'})


# Delete Blog Post
@app.route('/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    for i, blog in enumerate(blogs):
        if blog['id'] == id:
            deleted_blog = blogs.pop(i)
            response = deleted_blog.copy()
            response['time'] = response['time'].isoformat()
            return jsonify(response)

    return jsonify({'message': 'Blog post not found'})

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
