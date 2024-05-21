import youtube_dl
from tqdm import tqdm
playlist_url = "https://www.youtube.com/playlist?list=PLBBog2r6uMCSbEaxdWggDAnJ-Ov2D8Ndy"

ydl_opts = {
    'writesubtitles': True,
    'allsubtitles': True,
    'subtitleslangs': ['en'],
    'skip_download': True,  # Only download subtitles
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    playlist_info = ydl.extract_info(playlist_url, download=False)
    video_count = len(playlist_info['entries'])
    with tqdm(desc="Downloading", unit="videos", total=video_count) as bar:
        for video_info in playlist_info['entries']:
            video_title = video_info['title']
            video_id = video_info['id']
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            bar.update(1)
