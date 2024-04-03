from flask import Flask, send_from_directory


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def get_map():
        return send_from_directory('./data', 'map.html')

    return app


if __name__ == "__main__":
    create_app()
