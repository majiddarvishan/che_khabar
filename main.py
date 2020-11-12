"""App entry point."""
from code.heroku import run_app

app = run_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
