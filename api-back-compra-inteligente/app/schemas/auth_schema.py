from pydantic import BaseModel
from typing import Optional, List

class AuthSchema(BaseModel):
    cpf: str = "12345678900"
    senha: str = "senha123"

class TokenSchema(BaseModel):
    access_token: str