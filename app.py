from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

flask_secret_key = os.environ.get('FLASK_KEY')

def create_app() : 
    app = Flask(__name__)
    
    from views import main_views

    app.register_blueprint(main_views.bp)
    app.secret_key = flask_secret_key

    if __name__ == "__main__" : 
        app.run(host='0.0.0.0', port=8000, debug=True)

create_app()