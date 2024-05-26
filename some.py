import requests

url = 'http://localhost:8000/api/users/'  # Полный адрес эндпоинта
response = requests.get(url)
print(response.json())