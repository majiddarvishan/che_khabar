"""App entry point."""
from flask_app import create_app
from flasgger import Swagger, swag_from

app = create_app()

if __name__ == "__main__":
    # Create an APISpec
    template = {
    "swagger": "2.0",
    "info": {
        "title": "Che khabar",
        "description": "This is Swagger of Che Khabar Restful API's description",
        "version": "0.0.1",
        "contact": {
        "name": "Majid Darvishan",
        "url": "https://majiddarvishan.org",
        }
    },
    "securityDefinitions": {
        "Bearer": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
        "Bearer": [ ]
        }
    ]

    }

    app.config['SWAGGER'] = {
        'title': 'Che Khabar API',
        'uiversion': 3,
        "specs_route": "/swagger/"
    }

    swagger = Swagger(app, template= template)
    
    app.run(host="0.0.0.0", port=5000, debug=True)
