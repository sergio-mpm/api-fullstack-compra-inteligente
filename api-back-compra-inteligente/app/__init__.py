import os
import werkzeug
from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from .security import bearer_auth



def create_app():
    info = Info(
        title="CompraInteligenteAPI",
        version="1.0.0",
        description="API para uso do modelo preditivo de compras via e-commerce"
    )
    security_schemes = {"bearerAuth": bearer_auth}
    app = OpenAPI(__name__, info=info, doc_prefix="/v1", security_schemes=security_schemes)

    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    #Carga do Modelo
    from app.services.purchase_model_service import PurchaseModelService
    app.ml_model = PurchaseModelService()

    from app.models import usuario, cliente

    # registro de rotas
    from app.controllers.predicao_controller import predicao_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.usuario_controller import usuario_bp
    app.register_api(usuario_bp)
    app.register_api(predicao_bp)
    app.register_api(auth_bp)

    app.security = [{"bearerAuth": []}]


    return app