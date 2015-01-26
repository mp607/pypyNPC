#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from youtube_search import youtube_search
from plurk_oauth.PlurkAPI import PlurkAPI

def getPlurks(plurk, t = 3):
    offset = datetime.utcnow() - timedelta(minutes=t)
    offset = offset.strftime('%Y-%m-%dT%H:%M:%S')

    return plurk.callAPI('/APP/Polling/getPlurks', {
        'offset': offset,
        })

def npc(plurk):
    plurks = getPlurks(plurk, 3)

    msgs = plurks['plurks']
    plurk_users = plurks['plurk_users']

    # plurk 處理
    for msg in msgs:
        if msg['content_raw'].find(u'想聽') == 0:
            response(msg)

def response(p):
    # 記一下自己的plurk id
    myID = str(plurk.callAPI('/APP/Users/me')['id'])

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

    if plurk:
        # 自動加入所有好友
        plurk.callAPI('/APP/Alerts/addAllAsFriends')
        # Start NPC
        npc(plurk)

