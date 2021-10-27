from urllib import request
from bs4 import BeautifulSoup


URL = 'http://yjzq.online/userprofile/login'

response = request.Request(URL)

res = request.urlopen(response).read().decode('utf-8')
print(type(res))
with open('login1.html', 'w', encoding='utf-8') as f:
    f.write(res)

# res = request.urlopen(response).read()
# with open('login.html', 'wb') as f:
#     f.write(res)

