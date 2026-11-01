import requests

url = "http://127.0.0.1:8000/predict"

initial_balance = float(input("Initial Balance:"))
tx_amount = float(input("Tx Amount:"))
client_income = float(input("Client Income:"))
historical_amount = float(input("Historical Amount:"))
incorparation_days = float(input("Incorporation Days:"))

params = {
    "initial_balance":initial_balance,
    "tx_amount":tx_amount,
    "client_income": client_income,
    "historical_amount": historical_amount,
    "incorparation_days": incorparation_days
}
response = requests.post(url, params=params)
print(response.json())