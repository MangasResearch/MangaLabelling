import os

from flask import Flask
from flask import render_template
# from flask_socketio import SocketIO

# socketio = SocketIO()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "tool.sqlite"),
        #SEND_FILE_MAX_AGE_DEFAULT=0
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import db
    
    db.init_app(app)

    from . import site
    app.register_blueprint(site.bp)
    app.add_url_rule('/', endpoint='index')

    # socketio.init_app(app)
    #login_manager = LoginManager()
    #login_manager.init_app(app)
    return app
