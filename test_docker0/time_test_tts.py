# coding=utf-8
import argparse
import websocket           
import json
import time
import os
import base64
import jwthelper
import ssl
#import pyaudio

def test_time(content, return_mode, connect_method, speeker):
    websocket.enableTrace(True)
    print(connect_method)
    print("creating a connection to server")
    if connect_method == "vpn":
        url = 'ws://192.168.26.7:5000/api/tts?speeker=' + speeker
        ws = websocket.create_connection(url)
    elif connect_method == "127":
        url = 'ws://127.0.0.1:5000/api/tts?speeker=' + speeker
        ws = websocket.create_connection(url)
        if not ws:
            url = 'ws://127.0.0.1:5000/api/tts'
            ws = websocket.create_connection(url)
    elif connect_method == "gateway":
        url = 'wss://ai.cubigdata.cn:5001/openapi/speech/tts?speeker=' + speeker
        jwt_token = jwthelper.GetJWTToken()
        url = url.format(jwt_token)
        header={"Content_type:application/json;charset=utf-8","Authorization:Bearer {}".format(jwt_token)}
        ws = websocket.create_connection(url,header=header, sslopt={"cert_reqs": ssl.CERT_NONE})
    
    data = {'content':content, 'return_mode':return_mode}
    data = json.dumps(data)
    fw = open('output_{}.pcm'.format(connect_method), 'wb')
    time_list = []    
    ws.send(data)
    time_list.append(time.time())
    while True:
        res = ws.recv()
        time_list.append(time.time())
        if res is None or res == "":
            break
        if return_mode == "sentence":
            res = json.loads(res)
            status = res['status']
            audio = base64.b64decode(res['audio'])
            fw.write(audio)
            if status == 1:
                break
        elif return_mode == 'stream':
            fw.write(res)
    fw.close()
    ws.close()
    for i in range(1, len(time_list)):
        print("receive audio {}th: {}s".format(i, time_list[i] - time_list[i-1]))
    return
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--connect_method', default = 'vpn', choices = ['vpn', '127', 'gateway'])
    parser.add_argument('--file_path', default = './a.txt')
    parser.add_argument('--return_mode', default = 'sentence', choices = ['sentence','stream'])
    parser.add_argument('--speeker', default = 'ttsw01', choices = ['ttscw01', 'ttsw01'])
    args = parser.parse_args()
    connect_method = args.connect_method
    speeker = args.speeker
    return_mode = args.return_mode
    file_path = args.file_path
    f = open(file_path, 'r')
    content = f.read()
    f.close()
    test_time(connect_method = connect_method, speeker = speeker, return_mode = return_mode, content = content)
