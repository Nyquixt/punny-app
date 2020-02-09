# app.py is the main controller for the flask application.
# Using flask blueprints we create sub apps for different modules (user, lab)
# Then those sub apps are added to the main flask 'app'
# during the creation of the main app configurations for the app are called from setting.py
# On this file the db connection is initiated using app configuration from setting.py

from flask import Flask, render_template
from flask_mongoengine import MongoEngine

#  Creating an mongo engine for database
db = MongoEngine()

def page_not_found(e):
    return render_template('error_pages/404.html'), 404

def unauthorized(e):
    return render_template('error_pages/unauthorized.html'), 403

def create_app(**config_overrides):
    # main app
    app = Flask(__name__)
    # app configuration settings, including database connection
    app.config.from_pyfile('settings.py')
    app.config.update(config_overrides)
    # calling mongo engine and creating connection with the application
    db.init_app(app)

    from user.routes import user_app
    app.register_blueprint(user_app)

    from post.routes import post_app
    app.register_blueprint(post_app)

    from general.routes import general_app
    app.register_blueprint(general_app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, unauthorized)

    return app

if __name__ == '__main__': 
    app = create_app()
    app.run(host='0.0.0.0', debug=False, port=5000, ssl_context=None)
