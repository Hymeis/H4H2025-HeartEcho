from flask import Flask
from back_end.dao.db_client import init_db, db_session
from back_end.routes.comment import comment_bp
from back_end.routes.post import post_bp
from back_end.routes.auth import register_bp



app = Flask(__name__)

app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(post_bp, url_prefix='/posts')
app.register_blueprint(comment_bp, url_prefix='/comments')


# Initialize Flask-SQLAlchemy with the app
init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



if __name__ == "__main__":
    app.run(debug=True)