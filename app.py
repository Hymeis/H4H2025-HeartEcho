from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.post import post_bp
    from routes.comment import comment_bp
    from routes.like import like_bp
    from routes.tag import tag_bp # assuming you will create tag_bp in routes/tag.py
    from routes.chat import chat_bp # assuming you will create chat_bp in routes/chat.py
    from routes.user import user_bp # assuming you will create user_bp in routes/user.py
    from routes.task import task_bp # assuming you will create task_bp in routes/task.py


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    app.register_blueprint(like_bp, url_prefix='/likes')
    app.register_blueprint(tag_bp, url_prefix='/tags')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(task_bp, url_prefix='/tasks')


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)