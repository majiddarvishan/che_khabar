"""App entry point."""

def run_app():
    from .flask_app import create_app

    app = create_app()

    return app
