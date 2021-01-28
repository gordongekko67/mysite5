import os
from flask import Flask
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask import Flask, render_template, request, jsonify
from flask_restful import fields, marshal_with, Resource, Api, reqparse
#import simplejson
import requests
import cgi
import time, json
import sqlite3
from sqlite3 import Error


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    print(os.path.join(app.instance_path))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import altri
    app.register_blueprint(altri.bp)

    from . import form
    app.register_blueprint(form.bp)

    app.add_url_rule('/', endpoint='index')

    return app


