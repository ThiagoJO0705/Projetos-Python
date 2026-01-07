import requests

headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY4MzkyNTMxfQ.ISsft7F-PaOsv_lratahw_vZY56qR7_0d89AGHzrTLE'}

request = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)
print(request)
print(request.json())