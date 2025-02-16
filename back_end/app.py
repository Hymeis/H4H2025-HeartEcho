from flask import Flask
from flask_login import LoginManager
from config import Config
from database import init_db, Session, Base  # Import db and init_db from database.py

# # Initialize LoginManager
# login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    init_db(app)

    # # Initialize LoginManager
    # login_manager.init_app(app)

    # from routes.auth import auth_bp
    from routes.post import post_bp
    from routes.comment import comment_bp
    from routes.like import like_bp

    # app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    app.register_blueprint(like_bp, url_prefix='/likes')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, use_reloader=False)