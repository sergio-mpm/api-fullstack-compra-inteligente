import os
from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from .security import bearer_auth
from .services import purchase_model_service
from app.controllers.predicao_controller import predicao_bp


def create_app():
    info = Info(
        title="CompraInteligenteAPI",
        version="1.0.0",
        description="API para uso do modelo preditivo de compras via e-commerce"
    )
    app = OpenAPI(__name__, info=info, doc_prefix="/v1", security_schemes=bearer_auth)

    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    #Carga do Modelo
    model_path = os.path.join(
        os.path.dirname(__file__),
        "model",
        "modelo_final_ecommerce.pkl"
    )

    app.ml_model = purchase_model_service(model_path)

    # importacao de rotas para realização do migrate
    # TO DO

    # registro de rotas
    app.register_blueprint(predicao_bp, url_prefix="/v1")
    # TO DO

    app.security = [{"bearerAuth": []}]


    return app