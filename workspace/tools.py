import requests
from bs4 import BeautifulSoup

class PexelsParser:
    def __init__(self, api):
        self.api_key = api

    @staticmethod
    def get_highest_quality_video(video_files):
        highest_quality_video = max(video_files, key=lambda x: x['width'] * x['height'])
        return highest_quality_video['link']
    @staticmethod
    def find_videos(query, key, page=False):

        if(page!=False and page!='1'):
            req = requests.get(page,headers={'Authorization': key})
        else:
            req = requests.get(
                f'https://api.pexels.com/videos/search?query={query}&per_page=16&size=medium',
                headers={'Authorization': key}
            )
        ans = req.json()
        count = 0
        videos = []
        for video in ans['videos']:
            videos.append(PexelsParser.get_highest_quality_video(video['video_files']))
            count += 1

        return {'videos': videos, 'next_page': ans.get('next_page', False), 'prev_page': ans.get('prev_page', False)}


class PixabayParser:
    def __init__(self, api):
        self.api_key = api

    @staticmethod
    def find_videos(api_key, query, page=1):
        page = int(page)
        req = requests.get(
            f'https://pixabay.com/api/videos/?key={api_key}&q={query}&per_page=16&page={page}',
        )
        ans = req.json()
        count = 0
        videos = []
        for video in ans['hits']:
            video_ = video['videos']['large']
            videos.append(video_['url'])
            count += 1

        return {'videos': videos, 'next_page': page+1, 'prev_page': page-1}


class MixkitParser:
    @staticmethod
    def find_videos(query, page=1):
        page = int(page)
        query = query.split(' ')
        query = "".join(x + "-" for x in query)
        query = query[:-1]
        request = requests.get(f'https://mixkit.co/free-stock-video/{query}/?page={page}')
        soup = BeautifulSoup(request.text, 'lxml')
        divs = soup.find_all('div', {'class': 'item-grid-video-player__video-wrapper'})
        videos = []
        count = 0
        for div in divs:
            url = div.video['src']
            url = url.replace('small', 'large')
            videos.append(url)
            count += 1

        return {'videos': videos, 'next_page': page+1, 'prev_page': page-1}

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]