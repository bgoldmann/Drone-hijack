# simulator/mgmt/app.py
import os
import logging
from flask import Flask
from flask_cors import CORS
from extensions import db
from models import create_initial_stages
from routes import main

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # ---- Config ----
    # SQLite in the container (persists to /Simulator/mgmt/instance)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stages.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Lite mode flag used by templates to switch the viewer
    # (e.g., show Leaflet map instead of the old gzweb iframe)
    app.config['LITE'] = os.getenv('LITE', '').lower() in ('1', 'true', 'yes')

    # Optional: keep around for future use / UI display
    app.config['MAV2REST_URL'] = os.getenv('MAV2REST_URL', '')
    app.config['MAV2REST_POS_PATH'] = os.getenv(
        'MAV2REST_POS_PATH',
        '/mavlink/2/messages/GLOBAL_POSITION_INT'
    )

    app.config['COMPANION_WS_URL'] = os.getenv('COMPANION_WS_URL', '')

    # ---- DB init & seed ----
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_initial_stages()

    # ---- Logging to console ----
    app.logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    # avoid duplicate handlers if the app reloads
    if not any(isinstance(h, logging.StreamHandler) for h in app.logger.handlers):
        app.logger.addHandler(stream_handler)

    # ---- Make flags available in ALL templates ----
    @app.context_processor
    def inject_feature_flags():
        return {
            'LITE': app.config['LITE'],
            'MAV2REST_URL': app.config['MAV2REST_URL'],
            'MAV2REST_POS_PATH': app.config['MAV2REST_POS_PATH'],
            'COMPANION_WS_URL': app.config['COMPANION_WS_URL'],
        }

    # ---- Routes ----
    app.register_blueprint(main)

    return app

# WSGI entrypoint (gunicorn) and dev runner
app = create_app()

if __name__ == '__main__':
    # Dev run: python app.py
    app.run(host='0.0.0.0', port=8000, debug=True)
