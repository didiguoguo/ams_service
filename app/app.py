from flask import Flask
from flask_cors import CORS
from api import api

from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(api, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8999, debug=True, threaded=True)
