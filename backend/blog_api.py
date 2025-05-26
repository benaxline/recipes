# CRUD: Create, Read, Update, Delete
# For the blog aspect of the page

from flask import Blueprint, request, jsonify
from datetime import datetime

blog_bp = Blueprint('blog_bp', __name__)

# In-memory stores
blogs = []
comments = []
next_blog_id = 1
next_comment_id = 1

@blog_bp.route('/blogs', methods=['GET'])
def get_blogs():
    """Get all blog posts"""
    result = []
    for blog in blogs:
        blog_copy = blog.copy()
        blog_copy['time'] = blog['time'].isoformat()
        result.append(blog_copy)
    
    return jsonify(result)

@blog_bp.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    """Get a specific blog post with its comments"""
    for blog in blogs:
        if blog['id'] == blog_id:
            # Get comments for this blog
            blog_comments = [c for c in comments if c['blog_id'] == blog_id]
            
            # Format for JSON response
            response = blog.copy()
            response['time'] = blog['time'].isoformat()
            
            # Format comments
            formatted_comments = []
            for comment in blog_comments:
                comment_copy = comment.copy()
                comment_copy['time'] = comment['time'].isoformat()
                formatted_comments.append(comment_copy)
                
            response['comments'] = formatted_comments
            return jsonify(response)
    
    return jsonify({'message': 'Blog not found'}), 404

@blog_bp.route('/blogs', methods=['POST'])
def add_blog():
    """Create a new blog post"""
    global next_blog_id
    
    data = request.json
    new_blog = {
        'id': next_blog_id,
        'title': data['title'],
        'content': data['content'],
        'author': data['author'],
        'recipe_title': data.get('recipe_title', ''),  # Optional link to recipe
        'time': datetime.now()
    }
    
    blogs.append(new_blog)
    next_blog_id += 1
    
    # Format for JSON response
    response = new_blog.copy()
    response['time'] = new_blog['time'].isoformat()
    
    return jsonify(response), 201

@blog_bp.route('/blogs/<int:blog_id>/comments', methods=['POST'])
def add_comment(blog_id):
    """Add a comment to a blog post"""
    global next_comment_id
    
    # Check if blog exists
    blog_exists = any(blog['id'] == blog_id for blog in blogs)
    if not blog_exists:
        return jsonify({'message': 'Blog not found'}), 404
    
    data = request.json
    new_comment = {
        'id': next_comment_id,
        'blog_id': blog_id,
        'content': data['content'],
        'author': data['author'],
        'parent_id': data.get('parent_id'),  # For replies to comments
        'time': datetime.now()
    }
    
    comments.append(new_comment)
    next_comment_id += 1
    
    # Format for JSON response
    response = new_comment.copy()
    response['time'] = new_comment['time'].isoformat()
    
    return jsonify(response), 201
