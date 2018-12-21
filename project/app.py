from flask import Flask, render_template, request
import os
from pprint import pprint as pp
import requests
import random

app = Flask(__name__)

token  = os.getenv('TELEGRAM_TOKEN')
naver_id = os.getenv('NAVER_ID')
naver_secret = os.getenv('NAVER_SECRET')


base_url = "https://api.hphk.io/telegram" # https://api.telegram.org
my_url = "https://webhook-s3ung.c9users.io"

# 웹훅을 통해 정보가 들어올 route
@app.route('/{}'.format(token), methods=['POST'])
def telegram():
    doc = request.get_json() # 요청을 받았을 때 요청을 보낸 사람의 정보가 담김
    pp(doc)
    # 어떤 메세지가 들어오던 '닥쳐'라고 하는 챗봇
    chat_id = doc['message']['chat']['id']
    text = doc.get('message').get('text') # 없으면 에러처리가 아닌, 동적으로 넘어감
    
    # if msg == "로또" :
    #     reply = str(random.sample(range(1,46), 6))
    #     url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(base_url,token,chat_id,reply)
    #     requests.get(url)
    # else :
    #     url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(base_url,token,chat_id,msg)
    #     requests.get(url)
    
    img = False
    
    if doc.get('message').get('photo') is not None:
        img = True
    
    if img:
        file_id = doc.get('message').get('photo')[-1].get('file_id')
        file = requests.get("{}/bot{}/getFile?file_id={}".format(base_url, token, file_id))
        file_url = "{}/file/bot{}/{}".format(base_url, token, file.json().get('result').get('file_path'))
        
        # 네이버로 요청
        res = requests.get(file_url, stream=True)
        clova_res = requests.post('https://openapi.naver.com/v1/vision/celebrity',
            headers={
                'X-Naver-Client-Id':naver_id,
                'X-Naver-Client-Secret':naver_secret
            },
            files={
                'image':res.raw.read()
            })
        if clova_res.json().get('info').get('faceCount'):
            print(clova_res.json().get('faces'))
            text = "{}".format(clova_res.json().get('faces')[0].get('celebrity').get('value'))
        else:
            text = "인식된 사람이 없습니다."
    else:
    	# text 처리
    	text = doc['message']['text']
        
    requests.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(base_url, token, chat_id, text))
    return '', 200
    

# 웹훅 설정(set webhook) == 텔레그램에게 알리미를 해달라고 하는 것
@app.route('/setwebhook')
def setwebhook():
    url = "{}/bot{}/setWebhook?url={}/{}".format(base_url,token,my_url,token)
    res = requests.get(url) # json을 res에 저장 / 요청에 대한 결과값을 전송
    return '{}'.format(res), 200 # res 및 status코드200을 응답

# 텔레그램이 우리에게 알림을 줄 때 사용할 route
#   만약 특정 유저가 우리 봇으로 메세지를 보내게 되면,
#       텔레그램이 우리에게 알림을 보내옴(json)
# @app.route('/')
# def ():
#     return