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
    from routes.tag import tag_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    app.register_blueprint(like_bp, url_prefix='/likes')
    app.register_blueprint(tag_bp, url_prefix='/tags')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
