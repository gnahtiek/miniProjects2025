from alpaca_trade_api.rest import REST

# Replace with your keys
API_KEY = 'PK9NDQLB30HO4HKCUJH8'
SECRET_KEY = 'gD6uF7Rt6hs0bI0EHyXk9Qs00QwmghWc7yNvJFF1'
BASE_URL = 'https://paper-api.alpaca.markets/'  # Paper trading endpoint

api = REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

# Get account info
account = api.get_account()
print("Account Status:", account.status)

