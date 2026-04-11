import joblib
import pandas as pd
import numpy as np
import os

class PurchaseModelService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "..", "models", "modelo_final_ecommerce.pkl")
        self.model = joblib.load(model_path)
        self.highest_threshold = 0.87 # limiar decisivo
        self.high_threshold = 0.72 # limiar alto de decisão
        self.medium_threshold = 0.5 # limiar mediano de decisão
        self.low_threshold = 0.36 # limiar baixo de decisão
    
    ### Os threshold foram definidos para criar faixas progressivas de propensão de compra
    ### Permite-se assim que hajam interações diferenciadas no frontend
    ### Em um caso de decisão de compra, isso permite avaliar opções dependendo da interpretação

    def predict(self, data: dict) -> dict:

        # Transformando em dataframe
        df = pd.DataFrame([data])

        prob = self.model.predict_proba(df)[0][1]
        prediction = int(prob >= self.threshold)

        return {
            "probabilidade_compra": round(prob, 4),
            "faixa_conversao": self._interpretar(prob)
        }
    
    def _interpretar(self, prob: float) -> str:
        if prob >= self.highest_threshold:
            return "Chance extremamente alta de conversão"
        elif prob >= self.high_threshold:
            return "Alta chance de conversão"
        elif prob >= self.medium_threshold:
            return "Chance moderada de conversão"
        elif prob >= self.low_threshold:
            return "Baixa chance de conversão"
        else:
            return "Chance muito baixa ou nula de conversão"