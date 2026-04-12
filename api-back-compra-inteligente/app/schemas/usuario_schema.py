from pydantic import BaseModel
from typing import Optional, List

from ..models.usuario import Usuario


class UsuarioSchema(BaseModel):
    cpf: str = "12345678900"
    nome: str = "João da Silva"
    email: str = "seuemail@email.com.br"
    senha: str = "senha123"
    
    model_config = {
        "from_attributes": True
    }


class UsuarioBuscaSchema(BaseModel):
    cpf: str = "12345678900"


class UsuarioViewSchema(BaseModel):
    cpf: str = "12345678900"
    nome: str = "João da Silva"
    email: str = "seuemail@email.com.br"
    senha: str
    
    model_config = {
        "from_attributes": True
    }


class ListagemUsuariosSchema(BaseModel):
    usuarios: List[UsuarioViewSchema]


def apresenta_usuario(usuarios: List[Usuario]):
    result = []
    for usuario in usuarios:
        result.append({
            "cpf": usuario.cpf,
            "nome": usuario.nome
        })

    return {"usuarios": result}


class UsuarioDeleteSchema(BaseModel):
    cpf: str = "12345678900"
    nome: str = "João da Silva"

