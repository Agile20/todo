# Placeholder for Python file

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ToDo

todos = Blueprint('todos', __name__)

@todos.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    tasks = ToDo.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_done": task.is_done
    } for task in tasks])

@todos.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.json
    new_todo = ToDo(title=data['title'], description=data.get('description'), user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Task created"})

@todos.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()
    task = ToDo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"})

    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.is_done = data.get('is_done', task.is_done)
    db.session.commit()
    return jsonify({"message": "Task updated"})

@todos.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    task = ToDo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"})

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
