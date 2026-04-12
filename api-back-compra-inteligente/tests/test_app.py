from app import create_app
from app.services.purchase_model_service import PurchaseModelService
import pytest
import json
import pandas as pd
import numpy as np


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    """Um cliente de teste para simular requisições HTTP."""
    return app.test_client()

def test_predicao_endpoint_sucesso(client):
    """Verifica se o fluxo completo do endpoint está funcionando."""
    payload = {
        "age": 25,
        "gender": "Female",
        "device_type": "Mobile",
        "previous_purchases": 2,
        "returning_user": 0,
        "discount_seen": 1,
        "ad_clicked": 1,
        "cart_items": 1
    }
    
    response = client.post('/predicao/predizer', 
                            data=json.dumps(payload),
                            content_type='application/json',
                            headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTk1MDMzMiwianRpIjoiMWY3NDAwMzEtM2MzNy00NTU5LThhMjItYWU5ZTk4Mzk5N2ExIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEzOTgzNTUyNzU3IiwibmJmIjoxNzc1OTUwMzMyLCJjc3JmIjoiODRmZDA3NTUtZWM1Mi00NmQ4LWIwZjgtMjE1MjYzOTU2NzdlIiwiZXhwIjoxNzc1OTU3NTMyfQ.fvO211pYVLcbwpWDcl9gF_9iYG9MRvwNf1nemDHmiOU"})
    
    assert response.status_code == 200
    data = response.get_json()
    assert "faixa_conversao" in data
    assert "probabilidade_compra" in data

def test_validacao_schema_invalido(client):
    """Garante que a API barra dados malformados (Segurança/Qualidade)"""
    payload = {
        "age": "Idade Invalida",
        "cart_items": 3
    }
    
    response = client.post('/predicao/predizer', 
                            data=json.dumps(payload),
                            content_type='application/json',
                            headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTk1MDMzMiwianRpIjoiMWY3NDAwMzEtM2MzNy00NTU5LThhMjItYWU5ZTk4Mzk5N2ExIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEzOTgzNTUyNzU3IiwibmJmIjoxNzc1OTUwMzMyLCJjc3JmIjoiODRmZDA3NTUtZWM1Mi00NmQ4LWIwZjgtMjE1MjYzOTU2NzdlIiwiZXhwIjoxNzc1OTU3NTMyfQ.fvO211pYVLcbwpWDcl9gF_9iYG9MRvwNf1nemDHmiOU"})
    
    assert response.status_code in [400, 422]

def test_service_model_loading():
    """Teste unitário: Verifica se o PurchaseModelService carrega o modelo SVM."""
    service = PurchaseModelService()
    
    assert hasattr(service, 'model'), "O serviço não possui o atributo do modelo."
    assert service.model is not None, "O modelo SVM não foi carregado no serviço."
    
    # Verifica se o modelo carregado tem o método predict
    assert hasattr(service.model, 'predict'), "O objeto carregado não parece ser um modelo válido."

def test_predicao_logica_negocio():
    """Verifica se o método de predição do serviço retorna valores coerentes."""
    service = PurchaseModelService()
    # Mock de dados para testar diretamente o método do serviço
    dados_teste_dict = {
        'age': 25.0,
        'gender': 'Female',
        'device_type': 'Mobile',
        'previous_purchases': 2.0,
        'returning_user': 0.0,
        'discount_seen': 1.0,
        'ad_clicked': 1.0,
        'cart_items': 1.0
    }
    
    resultado = service.predict(dados_teste_dict)
    probabilidade = resultado["probabilidade_compra"]

    if isinstance(probabilidade, (list, np.ndarray)):
        probabilidade = np.array(probabilidade).flatten()[0]
    
    assert 0 <= probabilidade <= 1, "A probabilidade deve estar entre 0 e 1."

def test_predica_very_low_threshold():
    service = PurchaseModelService()
    dados_teste_dict = {
        'age': 37.0,
        'gender': 'Female',
        'device_type': 'Mobile',
        'previous_purchases': 0.0,
        'returning_user': 1.0,
        'discount_seen': 1.0,
        'ad_clicked': 0.0,
        'cart_items': 0.0
    }

    resultado = service.predict(dados_teste_dict)
    probabilidade = resultado["probabilidade_compra"]

    if isinstance(probabilidade, (list, np.ndarray)):
        probabilidade = np.array(probabilidade).flatten()[0]
    
    assert 0.0 <= probabilidade <= 0.9399, "A probabilidade deve estar contida nessa faixa."

def test_predicao_low_threshold():
    service = PurchaseModelService()
    dados_teste_dict = {
        'age': 39.0,
        'gender': 'Female',
        'device_type': 'Desktop',
        'previous_purchases': 0.0,
        'returning_user': 1.0,
        'discount_seen': 1.0,
        'ad_clicked': 0.0,
        'cart_items': 0.0
    }

    resultado = service.predict(dados_teste_dict)
    probabilidade = resultado["probabilidade_compra"]

    if isinstance(probabilidade, (list, np.ndarray)):
        probabilidade = np.array(probabilidade).flatten()[0]
    
    assert 0.94 <= probabilidade <= 0.9599, "A probabilidade deve estar contida nessa faixa."

def test_predicao_medium_threshold():
    service = PurchaseModelService()
    dados_teste_dict = {
        'age': 39.0,
        'gender': 'Male',
        'device_type': 'Mobile',
        'previous_purchases': 0.0,
        'returning_user': 1.0,
        'discount_seen': 1.0,
        'ad_clicked': 0.0,
        'cart_items': 0.0
    }

    resultado = service.predict(dados_teste_dict)
    probabilidade = resultado["probabilidade_compra"]

    if isinstance(probabilidade, (list, np.ndarray)):
        probabilidade = np.array(probabilidade).flatten()[0]
    
    assert 0.96 <= probabilidade <= 0.9799, "A probabilidade deve estar contida nessa faixa."

def test_predicao_high_threshold():
    service = PurchaseModelService()
    dados_teste_dict = {
        'age': 39.0,
        'gender': 'Male',
        'device_type': 'Desktop',
        'previous_purchases': 0.0,
        'returning_user': 1.0,
        'discount_seen': 1.0,
        'ad_clicked': 0.0,
        'cart_items': 0.0
    }

    resultado = service.predict(dados_teste_dict)
    probabilidade = resultado["probabilidade_compra"]

    if isinstance(probabilidade, (list, np.ndarray)):
        probabilidade = np.array(probabilidade).flatten()[0]
    
    assert 0.98 <= probabilidade <= 0.9899, "A probabilidade deve estar contida nessa faixa."

def test_predicao_very_high_threshold():
    service = PurchaseModelService()
    dados_teste_dict = {
        'age': 22.0,
        'gender': 'Male',
        'device_type': 'Desktop',
        'previous_purchases': 0.0,
        'returning_user': 1.0,
        'discount_seen': 1.0,
        'ad_clicked': 0.0,
        'cart_items': 0.0
    }

    resultado = service.predict(dados_teste_dict)
    probabilidade = resultado["probabilidade_compra"]

    if isinstance(probabilidade, (list, np.ndarray)):
        probabilidade = np.array(probabilidade).flatten()[0]
    
    assert 0.99 <= probabilidade <= 1, "A probabilidade deve estar contida nessa faixa."