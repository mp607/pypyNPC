#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from youtube_search import youtube_search
from plurk_oauth.PlurkAPI import PlurkAPI

def getPlurks(t = 3):
    offset = datetime.utcnow() - timedelta(minutes=t)
    offset = offset.strftime('%Y-%m-%dT%H:%M:%S')

    return plurk.callAPI('/APP/Polling/getPlurks', {
        'offset': offset,
        })

def hasResponsed(p):
    if p['response_count'] > 0:
        r = plurk.callAPI('/APP/Responses/get', {
            'plurk_id': p['plurk_id']
            })
        # 確認自己沒有回過這噗
        for key in r['friends'].keys():
            if key == myID:
                return True

def npc():
    plurks = getPlurks(3)

    msgs = plurks['plurks']
    plurk_users = plurks['plurk_users']

    # plurk 處理
    for msg in msgs:
        if hasResponsed(msg):
            continue

        if msg['content_raw'].find(u'想聽') == 0:
            findSongs(msg)

        elif msg['content_raw'].lower().find(u'@pypynpc') >=0:
            plurk.callAPI('/APP/Responses/responseAdd', {
                'plurk_id': msg['plurk_id'],
                'content': u'找我嗎？ (blush)'.encode('utf-8'),
                'qualifier': 'says'
                })

def findSongs(p):
    # 歌曲名稱
    name = p['content_raw'][2:]
    songs = youtube_search(name, 2)
    
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

if __name__ == "__main__":
    # 初始化
    plurk = PlurkAPI.fromfile('API.keys')

    if plurk:
        # 自動加入所有好友
        plurk.callAPI('/APP/Alerts/addAllAsFriends')

        # 記一下自己的plurk id
        myID = str(plurk.callAPI('/APP/Users/me')['id'])

        # Start NPC
        npc()

