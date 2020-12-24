#coding=utf-8
import time
import datetime
import jwt
import json
import requests

def GetJWTToken():
    # key = 'ZPH6YNyuKIzEaibQzGa8qgxHno5n4GBD'
    # secret = 'PQjX3oDL40ah1OZyDGHAAI6Y4jAoB637'

    key = 'Lzou33cnV6krZGTvrHErByMtriUesyIj'
    secret = '1JMNqfKTGgVqnrszS1tIYfRxlxJFVpI1'

    today = datetime.datetime.now()
    # delta = datetime.timedelta(hours=1)
    delta = datetime.timedelta(hours=0.5)
    exp = today + delta
    dt = exp.strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    exp = int(time.mktime(timeArray))

    # payload
    token_dict = {
        'iss': key,
        'iat': time.time(),  # 时间戳
        'exp': exp
    }
    """payload 中一些固定参数名称的意义, 同时可以在payload中自定义参数"""
    # iss  【issuer】发布者的url地址
    # exp 【expiration】 该jwt销毁的时间；unix时间戳
    # iat   【issued at】 该jwt的发布时间；unix 时间戳

    # headers
    headers = {
        "alg": "HS256",  # 声明所使用的算法
         "typ": "JWT"
    }


    # 调用jwt库,生成json web token
    jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                           secret,  # 进行加密签名的密钥
                           algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                           headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                           ).decode('ascii')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str

    return jwt_token

def test():
    jwt_token = GetJWTToken()
    print(jwt_token)
    for i in range(1):
        '''
        垃圾分类
        '''
        rsp = requests.get('https://ai.cubigdata.cn:5001/openapi/nlp/garbageclassifier/class?area=shanghai&name=塑料',verify=False, headers={"Content_type": "application/json;charset=utf-8","Authorization": "Bearer {}".format(jwt_token)})
        status_code = rsp.status_code
        print(rsp.content.decode("utf_8"))

if __name__ == "__main__":
    test()





# for i in range(1):
#     '''
#     内容审核
#     '''
#     rsp = requests.get('https://ai.cubigdata.cn:5001/openapi/nlp/sensitive_words/list?agentid=111&trackId=12',verify=False, headers={"agentid":"111","Content_type": "application/json;charset=utf-8","Authorization": "Bearer {}".format(jwt_token)})
#     status_code = rsp.status_code
#     print(rsp.content.decode("utf_8"))
#     print(status_code)


# for i in range(1):
#     '''
#     情感极性分类
#     '''
#     dateJson = '{"content":[{"id":"1", "text":"开心开心"},{"id":"", "text":"难过难过"},{"id":"3", "text":"这件衣服真好看"},{"id":"4", "text":"这顿饭太难吃了"}]}'
#     queryJson = json.loads(dateJson)
#     #     rsp = requests.post('https://ai.cubigdata.cn:5001/openapi/nlp/lexical/wordsegment/cn', json=queryJson,
#     #          headers={"Content_type": "application/json;charset=utf-8","Authentication": "Bearer {}".format(jwt_token)})
#     rsp = requests.post('https://ai.cubigdata.cn:5001/openapi/nlp/sentiment/polarity/cn', json=queryJson,verify=False,
#                         headers={"Authentication": "Bearer {}".format(jwt_token)})
#     status_code = rsp.status_code
#     print(rsp.content.decode("utf_8"))
