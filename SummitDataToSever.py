# requests.post()
# 构造表单-->提交表单-->获取返回信息
# 获取网页上https://www.crowdfunder.com/的公司名
import requests
import re

url = 'https://www.crowdfunder.com/'  # 该网页异步加载
html = requests.get(url)

data = {
    'entities_only':'true',
    'page':'2'
}
html_post = requests.post(url,data=data)
title = re.findall('"card-title">(.*?)</div>',html_post.text,re.S)
for each in title:
    print(each)  # print company name

