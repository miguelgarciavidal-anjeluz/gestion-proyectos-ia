import requests
import pandas as pd

url = "http://127.0.0.1:8000/predict"

data = [
            {"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
            {"initial_balance":3545.44,"tx_amount":1181.75,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 408},
            {"initial_balance":5800.00,"tx_amount":1000,"historical_amount": 798,"client_income": 1200,"incorparation_days": 890},
            {"initial_balance":5800.00,"tx_amount":1000,"historical_amount": 890,"client_income": 999,"incorparation_days": 1132}
        ]

df = pd.DataFrame(data)
df_res = pd.DataFrame()
for param in data:
    response = requests.post(url, params=param)
    json = response.json()
    new_row = pd.DataFrame({"Response": [json.get('fraud')]})
    df_res = pd.concat([df_res, new_row], ignore_index=True)
df['FRAUD'] = df_res['Response'].values

print(df)