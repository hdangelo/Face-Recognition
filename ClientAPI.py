import requests
import os

os.environ['no_proxy'] = '127.0.0.1,localhost'
#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

url = "http://10.1.6.31:5000/"
fin = open('C:/Desarrollo/Ejemplos/Python ejemplos/201903/FaceRecognition2-master/FaceRecognition2-master/att_faces/arqemp/Arquitecturaempresarial/5.jpg', 'rb')
files = {'file': fin}
NO_PROXY = {
    'no': 'pass',
}
s = requests.Session()
s.proxies = NO_PROXY

try:
    r = s.post(url, files=files, json=True)
    print(r.text)
    
finally:
	fin.close()