#!/usr/bin/env python

import sys
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

def youtube_search(name, max_results):
    try: 
        file = open('API.keys', 'r+')
    except IOError:
        print "You need to put keys in API.keys"
        raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
    else:
        data = json.load(file)
        file.close()
        if not data['GOOGLE_DEVELOPER_KEY']:
            print "You need to put keys in API.keys"
        else:
            DEVELOPER_KEY = data['GOOGLE_DEVELOPER_KEY']

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
            q=name,
            part="id,snippet",
            type="video",
            maxResults=max_results
            ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        videos.append(
                {
                    'title': search_result['snippet']['title'],
                    'id': search_result['id']['videoId']
                    }
                )

    return videos

if __name__ == '__main__':
    try:
        result = youtube_search('Hello, World!', 2)
        print result
    except HttpError, e:
         print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
