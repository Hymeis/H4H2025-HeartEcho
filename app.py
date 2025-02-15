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
    from back_end.routes.auth import auth_bp
    from back_end.routes.post import post_bp
    from back_end.routes.comment import comment_bp
    from back_end.routes.like import like_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    app.register_blueprint(like_bp, url_prefix='/likes')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
