import re
from DecryptLogin import login
from DecryptLogin.platforms.music163 import Cracker
import os
import requests

def send(sckey,title,msg):
    url='http://sc.ftqq.com/%s.send'%(sckey)
    data={'text':title,'desp':msg}
    r=requests.post(url=url,data=data)
    print('server酱返回信息：'+r.text)


def run(username, password):
    try:
        result=''
        lg = login.Login()
        _, session = lg.music163(username, password)
        csrf = re.findall('__csrf=(.*?) for', str(session.cookies))[0]
        cracker = Cracker()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://music.163.com/discover',
            'Accept': '*/*'
        }
        signin_url = 'https://music.163.com/weapi/point/dailyTask?csrf_token=' + csrf
        # 模拟签到(typeid为0代表APP上签到, 为1代表在网页上签到)
        typeids = [0, 1]
        for typeid in typeids:
            client_name = 'Web端' if typeid == 1 else 'APP端'
            # --构造请求获得响应
            data = {
                'type': typeid
            }
            data = cracker.get(data)
            res = session.post(signin_url, headers=headers, data=data)
            res_json = res.json()
            # --判断签到是否成功
            if res_json['code'] == 200:
                print(res_json)
                print('%s签到成功...' % ( client_name))
                result+='%s签到成功...' % ( client_name)+'<br>'


            else:
                print(res_json)
                print('%s签到失败, 原因: %s...' % (client_name, res_json.get('msg')))
                result+='%s签到失败, 原因: %s...' % (client_name, res_json.get('msg'))+'<br>'
    except Exception as e:
        print(e.args)
        result+=e.args+'<br>'

    return result






if __name__ == '__main__':
    username = os.environ['username']
    password = os.environ['password']
    sckey = os.environ['sckey']


    result=run(username,password)
    send(sckey,'网易云签到通知',result)