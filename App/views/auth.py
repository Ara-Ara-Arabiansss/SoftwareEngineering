from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    get_all_users,
    login,
    create_competitor 
    
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''




# @auth_views.route('/users', methods=['GET'])
# def get_user_page():
#     users = get_all_users()
#     return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


# @auth_views.route('/login', methods=['POST'])
# def login_action():
#     data = request.form
#     user = login(data['username'], data['password'])
#     if user:
#         login_user(user)
#         return 'user logged in!'
#     return 'bad username or password given', 401

# @auth_views.route('/logout', methods=['GET'])
# def logout_action():
#     data = request.form
#     user = login(data['username'], data['password'])
#     return 'logged out!'

'''
API Routes
'''

# @auth_views.route('/api/users', methods=['GET'])
# def get_users_action():
#     users = get_all_users_json()
#     return jsonify(users)

# @auth_views.route('/api/users', methods=['POST'])
# def create_user_endpoint():
#     data = request.json
#     response = create_competitor(data['username'],data['email'], data['password'])
#     if response:
#         return jsonify({'message': f"Competitor created"}), 201
#     return jsonify(error='error creating Competitor'), 401

@auth_views.route('/api/admin/login', methods=['POST'])
def admin_login_api():
  data = request.form
  token = jwt_authenticate(data['username'], data['password'],True)
  if not token:
    return jsonify(error='bad username or password given'), 401
  return jsonify(access_token=token)

@auth_views.route('/api/competitor/login', methods=['POST'])
def competitor_login_api():
  data = request.form
  token = jwt_authenticate(data['username'], data['password'])
  if not token:
    return jsonify(error='bad username or password given'), 401
  return jsonify(access_token=token)

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {jwt_current_user.username}, id : {jwt_current_user.id}"})


