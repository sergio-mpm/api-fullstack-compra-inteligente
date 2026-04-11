from app.services.purchase_model_service import PurchaseModelService
from app.services.usuario_service import UsuarioService
from flask_jwt_extended import create_access_token
from datetime import timedelta

service_predicao = PurchaseModelService()
service_usuario = UsuarioService()


class AuthService:
    def authenticate(self, cpf: str, senha: str) -> str:
        """
        Autentica o usuário e retorna um JWT
        """

        # MOCK (para projeto)
        if cpf != "admin" or senha != "123456":
            raise ValueError("Credenciais inválidas")

        access_token = create_access_token(
            identity=cpf,
            expires_delta=timedelta(hours=2)
        )

        return access_token
    
    