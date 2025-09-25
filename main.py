import os
import yaml
from flask import Flask
from flasgger import Swagger

from config.mongodb import init_db
from routes import employees_bp, position_bp, seed_bp

API_V1_PREFIX = "/api/v1"

app = Flask(__name__)

init_db()


@app.route("/")
def health_check():
    return "Ok"


app.register_blueprint(seed_bp, url_prefix=API_V1_PREFIX)
app.register_blueprint(employees_bp, url_prefix=API_V1_PREFIX)
app.register_blueprint(position_bp, url_prefix=API_V1_PREFIX)

base_path = os.path.join(os.path.dirname(__file__), "docs", "base.yml")
with open(base_path) as f:
    template = yaml.safe_load(f)

Swagger(app, template=template)
