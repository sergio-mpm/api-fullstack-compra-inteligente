from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ..extensions import db
from ..models import base


class Cliente(db.Model):
    __tablename__ = 'cliente'

    client_id = db.Column(db.Integer, primary_key=True, nullable=False)
    age = db.Column(db.Float, nullable=True)
    gender = db.Column(db.String(15), nullable=True)
    device_type = db.Column(db.String(20), nullable=True)
    previous_purchases = db.Column(db.Float, nullable=True)
    cart_items = db.Column(db.Float, nullable=True)
    discount_seen = db.Column(db.Float, nullable=True)
    ad_clicked = db.Column(db.Float, nullable=True)
    returning_user = db.Column(db.Float, nullable=True)
    
    usuario_responsavel = Column(
        db.String(11),
        ForeignKey("usuarios.cpf"),
        nullable=False
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="clientes"
    )

    def __init__(self, age:float, gender:str, device_type:str, previous_purchases:float, cart_items:float, discount_seen:float, ad_clicked:float, returning_user:float, usuario_responsavel:str):
        """
            Insere o registro de um cliente consultado
        """

        self.age = age
        self.gender = gender
        self.device_type = device_type
        self.previous_purchases = previous_purchases
        self.cart_items = cart_items
        self.discount_seen = discount_seen
        self.ad_clicked = ad_clicked
        self.returning_user = returning_user
        self.usuario_responsavel = usuario_responsavel

    def to_dict(self):
        return {
            "cliente_id": self.client_id,
            "age": self.age,
            "gender": self.gender,
            "device_type": self.device_type,
            "previous_purchases": self.previous_purchases,
            "cart_items": self.cart_items,
            "discount_seen": self.discount_seen,
            "ad_clicked": self.ad_clicked,
            "returning_user": self.returning_user,
            "usuario_responsavel": self.usuario_responsavel
        }