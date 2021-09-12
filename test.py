import finnhub
from config import API_KEY


finnhub_client = finnhub.Client(api_key=API_KEY)

print(finnhub_client.quote('AMC'))

