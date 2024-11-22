from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import auth
from routes.todo_routes import todos
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

# Инициализация приложения и базы данных
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Регистрация Blueprint для аутентификации и задач
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(todos, url_prefix='/api')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Перенаправление на страницу логина для неавторизованных пользователей


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Simple password check (add hashing in production)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    tasks = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=tasks)

# Добавление новой задачи через форму
@app.route('/add_todo', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title')  # Используем get для безопасного доступа к данным
    description = request.form.get('description')
    
    if title and description:  # Проверяем, что поля не пустые
        new_task = Todo(title=title, description=description, user_id=current_user.id)  # Если есть авторизация
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

# Удаление задачи по ID
@app.route('/delete_todo/<int:id>')
@login_required
def delete_todo(id):
    task = Todo.query.get(id)
    if task:  # Проверяем, что задача существует
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_todo/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    task = Todo.query.get(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_todo.html', task=task)


# Запуск приложения с инициализацией базы данных
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Инициализация таблиц базы данных
    app.run(debug=True)
