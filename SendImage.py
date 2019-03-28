import requests
import os
os.environ['no_proxy'] = '127.0.0.1,localhost'

proxies = {
    'http': 'http://dbt1241a:dbt1241@proxy14.bancogalicia.com.ar:80',
    'https': 'http://dbt1241a:dbt1241@proxy14.bancogalicia.com.ar:80',
}
NO_PROXY = {
    'no': 'pass',
}

s = requests.Session()
s.proxies = NO_PROXY

URL_BASE = 'http://localhost:5000/'
auth = ('L0274860', 'dante0405')
""" 
# API v1.2 - Get Authentication Token
print('Retrieving authentication token...')
url = URL_BASE + 'imagen'
r = s.get(url, auth=auth)
print(r.status_code)
print(r.headers)
auth_request = r.json()
token_auth = (auth_request['token'], 'unused')
""" 
# API v1.2 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE  + 'imagen'
#r = requests.get(url, auth=token_auth)
r = s.get(url)
print(r.status_code)
print(r.text)
 
# API v1.2 - PUT (Add image)
print('Updating recipe #2 with recipe image...')
url = URL_BASE + 'imagen'
#r = requests.put(url, auth=token_auth, files={'recipe_image': open('IMG_6127.JPG', 'rb')})
r = s.put(url, files={'recipe_image': open('C:/Desarrollo/Ejemplos/Python ejemplos/201903/FaceRecognition2-master/FaceRecognition2-master/reconocido.png', 'rb')})
print(r.status_code)
print(r.text)