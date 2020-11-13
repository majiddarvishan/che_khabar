"""App entry point."""
from code.heroku import run_app

app = run_app()

# A welcome message to test our server
# @app.route('/')
# def index():
#     return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
