from flask_app import create_app
from utils.environment import get_config


flask_app = create_app(get_config())

if __name__ == "__main__":
    flask_app.run()
