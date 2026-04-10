from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_openapi3 import APIBlueprint, Tag
from flask_openapi3 import openapi

from app.schemas.predicao_schema import PredicaoSchema
from app.schemas.error_schema import ErrorSchema
from app.services.purchase_model_service import PurchaseModelService

predicao_tag = Tag(
    name="Predicao",
    description="Operação de predição de conversão de compra por clientes"
)

predicao_bp = APIBlueprint(
    "predicao",
    __name__,
    url_prefix="/predicao",
    abp_tags=[predicao_tag]
)

service_predicao = PurchaseModelService()

@predicao_bp.post(
    "/predizer",
    responses={200: PredicaoSchema, 400: ErrorSchema}
)
def predizer_compra(body: PredicaoSchema):
    """
        Avalia uma predição de compra baseado no modelo existente
    """

    try:
        return"OK"
    except ValueError as e:
        return {"message": str(e)}, 400