import joblib
import pandas as pd
import numpy as np

class PurchaseModelService:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, data: dict):
        df = pd.DataFrame([data])

        prob = self.model.predict_proba(df)[0][1]
        prediction = int(prob >= 0.5)

        return {
            "probabilidade_compra": round(prob, 4),
            "classe_predita": prediction,
            "mensagem": (
                "Alta chance de conversão"
                if prediction == 1
                else "Baixa chance de conversão"
            )
        }