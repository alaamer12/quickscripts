from pytube import Playlist
from tqdm import tqdm

p = Playlist("https://www.youtube.com/playlist?list=PLBBog2r6uMCSbEaxdWggDAnJ-Ov2D8Ndy")

print(len(p))
with tqdm(desc="Downloading", unit="videos", total=len(p)) as bar:
    for i, video in enumerate(p.videos):
        print(f"({i + 1}/{len(p)}) {video.title}")
        video.captions.get_by_language_code('en').xml_caption_to_srt(f'./subtitles/{video.title}.srt')
        bar.update(1)
