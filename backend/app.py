from flask import Flask
from flask_cors import CORS
from backend.routes.soal_routes import soal_bp
from backend.ai_engine.nlp.nltk_setup import setup_nltk

app = Flask(__name__)
CORS(app)

app.register_blueprint(soal_bp, url_prefix="/api/soal")


if __name__ == "__main__":
    app.run(debug=True)

setup_nltk()