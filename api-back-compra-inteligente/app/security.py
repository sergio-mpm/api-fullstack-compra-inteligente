from flask_openapi3.models import SecurityScheme

bearer_auth = SecurityScheme(
    type="http",
    scheme="bearer",
    bearerFormat="JWT"
)