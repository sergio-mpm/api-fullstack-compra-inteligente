from app.services.purchase_model_service import PurchaseModelService
from app.services.usuario_service import UsuarioService

service_predicao = PurchaseModelService()
service_usuario = UsuarioService()


class AuthService:
    def autorizar_login(self, cpf:str, senha:str) -> bool:
        return True
    
    