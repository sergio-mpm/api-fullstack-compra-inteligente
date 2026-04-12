from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ..extensions import db
from ..models import base


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    cpf = db.Column(db.String(11), primary_key=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    senha = db.Column(db.String(15), nullable=False)

    clientes = db.relationship(
        "Cliente",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    def __init__(self, cpf:str, nome:str, email:str, senha:str):
        """
            Instancia um usuário no sistema

            Args:
                cpf: cpf da pessoa e identificador único no sistema
                nome: nome do usuário
                email: email do usuario no sistema
                senha: senha do usuario, a ser criptografada para proteção
        """
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.senha = senha

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "clientes": self.clientes
        }