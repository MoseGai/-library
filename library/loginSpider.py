import random
from django.shortcuts import HttpResponse, render, redirect
import requests
from lxml.html import etree
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=1633a80bb95339-096e7ba2edcff7-444a022e-144000-1633a80bb9644f; safedog-flow-item=3A4EB19447C00C8E30CF1A58FF340D86; yunsuo_session_verify=a0515ac15580a40410a7ee5bd4dc594d',
    'Host': 'opac.szpt.edu.cn:8991',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

def getRandomAlphet():
    result = ''
    for i in range(1,20):
        result += (chr(random.randint(0,24)+65))
    return result
# 获取秘钥
def getSecretKey():
    keyUrl = 'http://opac.szpt.edu.cn:8991/F/'+getRandomAlphet()
    # print('loginUrl:',keyUrl)
    response = requests.get(url=keyUrl,headers=headers)
    response.encoding = 'utf-8'
    print(response.text)
    selector = etree.HTML(response.text)
    secretKey = selector.xpath('//a[contains(text(),"检索首页")]/@href')[0]

    startIndex = secretKey.find('/F/') + 3
    endIndex = secretKey.find('?')
    secretKey = secretKey[startIndex:endIndex]
    return secretKey

data = {
    'func': 'login-session',
    'login_source': 'bor-info',
    'bor_id': '{user}',
    'bor_verification': '{password}',
    'bor_library': 'SZY50',
}
def login(user,password):
    url = 'http://opac.szpt.edu.cn:8991/F/{key}?func=file&file_name=login-session'.format(key=getSecretKey())

    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'

    # print(response.text)

    selector = etree.HTML(response.text)

    href = selector.xpath('//form/@action')[0]

    data['bor_id'] = data['bor_id'].format(user=user)
    data['bor_verification'] = data['bor_verification'].format(password=password)

    response = requests.post(url=href,headers=headers,data=data)
    response.encoding = 'utf-8'

    selector = etree.HTML(response.text)

    judge = selector.xpath('//td[contains(text(),"借阅历史列表")]//text()')

    data['bor_id'] =  '{user}'
    data['bor_verification'] = '{password}'
    if judge != []:
        return True,response
    else:
        return False,None

if __name__ == "__main__":
    pass
