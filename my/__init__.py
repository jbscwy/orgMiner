from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_session import Session
import os

from my.orgMiner import new_index
from my.orgMiner.org_model_mining import org_model_mining, visual_org_model
from my.orgMiner.process_model_mining import bpmn_model_mining
from my.orgMiner.resource_log import get_resource_log
from my.orgMiner.xes_to_csv import xes_csv

app = Flask(__name__)

app.secrect = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, app.static_folder)

def create_app(demo=False):
    app.demo = demo
    app.debug = True
    app.config['SECRET_KEY'] = 'orgminer-my'
    app.config['TEMP'] = os.path.join(os.path.dirname(APP_ROOT), '.tmp/')
    app.config['ID_DELIMITER'] = '|::|'

    bootstrap = Bootstrap(app)
    CORS(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(
        app.config['TEMP'], '.flask_session/'
    )
    Session(app)
    app.register_blueprint(xes_csv.bp)

    app.register_blueprint(get_resource_log.bp)

    app.register_blueprint(org_model_mining.bp)

    app.register_blueprint(visual_org_model.bp)

    app.register_blueprint(new_index.bp)

    app.register_blueprint(bpmn_model_mining.bp)

    app.url_build_error_handlers.append(url_build_error_handler_null)



    return app


# extra application configuration
def url_build_error_handler_null(error, endpoint, values):
    return '#'


# HTTP error pages
from flask import render_template
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500
