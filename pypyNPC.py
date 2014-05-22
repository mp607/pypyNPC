#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from youtube_search import youtube_search
from plurk_oauth.PlurkAPI import PlurkAPI

def response(p):
    if p['response_count'] > 0:
        r = plurk.callAPI('/APP/Responses/get', {
            'plurk_id': p['plurk_id']
            })
        # 確認自己沒有回過這噗
        for key in r['friends'].keys():
            if key == myID:
                return

    # 歌曲名稱
    name = p['content_raw'][2:]
    songs = findSong(name)
    
    for song in songs:
        resp = u'為您帶來'
        resp += ' '
        resp += song['title']
        resp += ' '
        resp += '^_^'
        resp += '\n'
        resp += 'http://www.youtube.com/watch?v='
        resp += song['id']

        plurk.callAPI('/APP/Responses/responseAdd', {
            'plurk_id': p['plurk_id'],
            'content': resp.encode('utf-8'),
            'qualifier': 'likes' 
            })

def findSong(name):
    return youtube_search(name, 2)

if __name__ == "__main__":
    # 初始化
    plurk = PlurkAPI.fromfile('API.keys')

    # 自動加入所有好友
    plurk.callAPI('/APP/Alerts/addAllAsFriends')

    # 記一下自己的plurk id
    myID = str(plurk.callAPI('/APP/Users/me')['id'])

    # 取得三分鐘前的時間(utc)當參數
    offset = datetime.utcnow() - timedelta(minutes=3)
    offset = offset.strftime('%Y-%m-%dT%H:%M:%S')

    # 取的最近三分鐘的噗
    msgs = plurk.callAPI('/APP/Polling/getPlurks', {
        'offset': offset,
        })['plurks']

    for msg in msgs:
        if msg['content_raw'].find(u'想聽') == 0:
            response(msg)

