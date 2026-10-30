import pickle

import pandas as pd

model_paths = '../models/'

with open(model_paths + 'pld_model_RandomForest.pkl', "rb") as f:
    model = pickle.load(f)

s1 = [6335.83, 3167.92, 23976047.89, 6335.84, 2402.0]
s2 = [17727.18, 1181.75, 51111005.38, 5908.75, 385.0]
s3 = [3545.44, 1181.75, 4855550.99, 1181.75, 752.0]

transacciones = pd.DataFrame([s1, s2, s3],
                             columns=["INIT_BALANCE", "TX_AMOUNT", "CLIENT_INCOMES", "HIST_AMOUNT", "INCORPORATION"])
print(transacciones)

# Predecir todas las transacciones de un solo golpe
predicciones = model.predict(transacciones)

# Recorrer los resultados para mostrarlos
for i, pred in enumerate(predicciones):
    es_fraude = "Positivo" if pred == 1 else "Negative"
    print(f"Transacción {i + 1} es fraude: {es_fraude}")
