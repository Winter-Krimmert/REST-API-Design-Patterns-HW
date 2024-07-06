from flask import jsonify, request, current_app as app
from . import db
from .models import User, Post

def init_app(app):
    """
    Initialize routes with the Flask app.
    """
    @app.route('/')
    def index():
        """
        Root endpoint to verify if the API is running.
        """
        return "Welcome to the Blog API!"

    # Route to get a single user by ID
    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_single_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email
            }), 200
        else:
            return jsonify({'error': f'User with ID {user_id} does not exist'}), 404
        
    # Route to fetch all users
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        result = [{
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email
        } for user in users]
        return jsonify(result), 200

    # Route to get a single post by ID
    @app.route('/posts/<int:post_id>', methods=['GET'])
    def get_single_post(post_id):
        post = Post.query.get(post_id)
        if post:
            return jsonify({
                'id': post.id,
                'title': post.title,
                'body': post.body,
                'user_id': post.user_id
            }), 200
        else:
            return jsonify({'error': f'Post with ID {post_id} does not exist'}), 404

    # Route to create a new user
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        try:
            new_user = User(
                name=data['name'],
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create user', 'message': str(e)}), 400

    # Route to update an existing user by ID
    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'User with ID {user_id} does not exist'}), 404

        data = request.get_json()
        try:
            user.name = data.get('name', user.name)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)
            db.session.commit()
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update user', 'message': str(e)}), 400

    # Route to delete a user by ID
    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'User with ID {user_id} does not exist'}), 404

        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to delete user', 'message': str(e)}), 400

    # Route to create a new post
    @app.route('/posts', methods=['POST'])
    def create_post():
        data = request.get_json()
        try:
            new_post = Post(
                title=data['title'],
                body=data['body'],
                user_id=data['user_id']
            )
            db.session.add(new_post)
            db.session.commit()
            return jsonify({'message': 'Post created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create post', 'message': str(e)}), 400

    @app.route('/posts', methods=['GET'])
    def get_posts():
        try:
            posts = Post.query.all()
            result = [{'id': post.id, 'title': post.title, 'body': post.body, 'user_id': post.user_id} for post in posts]
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': 'Failed to fetch posts', 'message': str(e)}), 500
