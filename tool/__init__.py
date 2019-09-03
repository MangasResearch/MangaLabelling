import os

from flask import Flask
from flask import render_template
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "tool.sqlite")#,
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

    from . import db
    
    db.init_app(app)

    from . import site
    app.register_blueprint(site.bp)
    app.add_url_rule('/', endpoint='index')

    return app
