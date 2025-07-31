import numpy as np
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return {"message": "Hello from Flask API!"}
    
    @app.route("/health")
    def health():
        return {"status": "healthy"}
    
    @app.route("/random")
    def random_number():
        random_value = np.random.randint(1, 100)
        return {"random_number": int(random_value)}

    return app
