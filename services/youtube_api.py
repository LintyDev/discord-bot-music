import yt_dlp
from googleapiclient.discovery import build

class Youtube_API:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def search(self, query):
        req = self.youtube.search().list(q=query, part="snippet", type="video", maxResults=1)
        res = req.execute()
        return res
    
    def get_audio(self, to_play_url):
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'temp_dl/%(id)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(to_play_url, download=True)
            file = ydl.prepare_filename(info)
        return file