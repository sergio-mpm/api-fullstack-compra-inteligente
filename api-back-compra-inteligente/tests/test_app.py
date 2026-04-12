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

@pytest.fixture
def get_token_valido(client):
    dados_login = {
        "cpf": "13983552757",
        "senha": "Senha123"
    }
    response = client.post('/auth/login', json=dados_login)
    assert response.status_code == 200, f"Erro no login: {response.status_code}"
    data = response.get_json()
    return data['access_token']

def test_predicao_endpoint_sucesso(client, get_token_valido):
    """Verifica se o fluxo completo do endpoint está funcionando."""
    token = get_token_valido
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
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    data = response.get_json()
    assert "faixa_conversao" in data
    assert "probabilidade_compra" in data

def test_validacao_schema_invalido(client, get_token_valido):
    """Garante que a API barra dados malformados (Segurança/Qualidade)"""
    token = get_token_valido
    payload = {
        "age": "Idade Invalida",
        "cart_items": 3
    }
    
    response = client.post('/predicao/predizer', 
                            data=json.dumps(payload),
                            content_type='application/json',
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code in [400, 422]

def test_service_model_loading():
    """Teste unitário: Verifica se o PurchaseModelService carrega o modelo SVM."""
    service = PurchaseModelService()
    
    assert hasattr(service, 'model'), "O serviço não possui o atributo do modelo."
    assert service.model is not None, "O modelo SVM não foi carregado no serviço."
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

@pytest.fixture
def cpf_teste():
    import random
    return "".join([str(random.randint(0, 9)) for _ in range(11)])

def test_cadastrar_usuario_sucesso(client, cpf_teste):
    """Verifica se a criação de um novo usuário via POST está funcionando."""
    payload = {
        "cpf": cpf_teste,
        "nome": "Usuario Teste",
        "email": f"teste_{cpf_teste}@email.com",
        "senha": "Senha123",
    }
    
    response = client.post('/usuarios/cadastrar', json=payload)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['cpf'] == cpf_teste
    assert data["nome"] == "Usuario Teste"
    assert "senha" in data

def test_consultar_usuario_sucesso(client, get_token_valido):
    """Verifica se a consulta de usuário (GET) com JWT está funcionando."""
    cpf_existente = "13983552757" 
    token = get_token_valido
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f'/usuarios/{cpf_existente}', headers=headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['cpf'] == cpf_existente

def test_consultar_usuario_nao_encontrado(client, get_token_valido):
    """Verifica o erro 404 ao buscar um CPF inexistente."""
    token = get_token_valido
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get('/usuarios/00000000000', headers=headers)
    
    assert response.status_code == 404
    assert "message" in response.get_json()