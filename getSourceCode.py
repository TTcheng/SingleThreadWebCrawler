import requests
html = requests.get('http://tieba.baidu.com/f?ie=utf-8&kw=python')
print(html.text)

# # 伪装成浏览器访问
# requestHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
# html = requests.get('http://jp.tingroom.com/',headers = requestHeader)
# print(html.text)