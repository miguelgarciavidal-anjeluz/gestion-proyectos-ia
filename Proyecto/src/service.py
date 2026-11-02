import joblib as jl
import pandas as pd
from fastapi import FastAPI

app = FastAPI()
# Cargar modelo
with open('../models/pld_model_RandomForest.pkl', "rb") as f:
    model = jl.load(f)


@app.get("/")
def home():
    return {"mensaje": "API de modelo funcionando"}


@app.post("/predict")
def predict(initial_balance: float, tx_amount: float, client_income: float, historical_amount: float,
            incorparation_days: float):
    data = [initial_balance, tx_amount, client_income, historical_amount, incorparation_days]
    transacciones = pd.DataFrame([data],
                                 columns=["INIT_BALANCE", "TX_AMOUNT", "CLIENT_INCOMES", "HIST_AMOUNT",
                                          "INCORPORATION"])
    prediction = model.predict(transacciones)
    return {"fraud": prediction.tolist()[0]}
