
import requests
import pandas as pd

url = "http://127.0.0.1:8000/predict"

data = [
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3545.44,"tx_amount":1181.75,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 408},
{"initial_balance":5800.00,"tx_amount":1000,"historical_amount": 798,"client_income": 0,"incorparation_days": 890},
{"initial_balance":0.0,"tx_amount":1000,"historical_amount": 890,"client_income": 999,"incorparation_days": 1132},
{"initial_balance":3545.44,"tx_amount":0.0,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 408},
{"initial_balance":5800.0,"tx_amount":1000,"historical_amount": 0.0,"client_income": 999,"incorparation_days": 490},
{"initial_balance":5800.0,"tx_amount":1000,"historical_amount": 890,"client_income": 0.0,"incorparation_days": 890},
{"initial_balance":5800.0,"tx_amount":1000,"historical_amount": 890,"client_income": 999,"incorparation_days": 0},
{"initial_balance":3545.44,"tx_amount":0.01,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 408},
{"initial_balance":9999999999999.99,"tx_amount":1181.75,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 408},
{"initial_balance":3545.44,"tx_amount":9999999999999.99,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 408},
{"initial_balance":999.99,"tx_amount":1181.75,"historical_amount": 9999999999999.99,"client_income": 10636.32,"incorparation_days": 408},
{"initial_balance":3545.44,"tx_amount":0.01,"historical_amount": 354.52,"client_income": 9999999999999.99,"incorparation_days": 408},
{"initial_balance":3545.44,"tx_amount":1181.75,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 999999999999999},
{"initial_balance":3545.44,"tx_amount":1181.75,"historical_amount": 354.52,"client_income": 10636.32,"incorparation_days": 1},
{"initial_balance":-10000.00,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":-10000,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": -10000,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3545.44,"tx_amount":1181.75,"historical_amount": 354.52,"client_income": -10000.00,"incorparation_days": 408},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": -10000},
{"initial_balance":0,"tx_amount":0,"historical_amount": 0,"client_income": 0,"incorparation_days": 0},
{"initial_balance":"ABC","tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":"ABC","historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": "ABC","client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": "ABC","incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": "ABC"},
{"initial_balance":[],"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":[],"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": [],"client_income": 15839.6,"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": [],"incorparation_days": 1852},
{"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": []},
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

df100_res = pd.DataFrame()
i = 0
p = {"initial_balance":3167.92,"tx_amount":3167.92,"historical_amount": 3801.5,"client_income": 15839.6,"incorparation_days": 1852}
while i < 1000:
    response = requests.post(url, params=p)
    json = response.json()
    new_row = pd.DataFrame({"Response": [json.get('fraud')]})
    df100_res = pd.concat([df100_res, new_row], ignore_index=True)
    i+=1

print(df100_res.describe())
