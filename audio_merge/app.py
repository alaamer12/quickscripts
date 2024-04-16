from moviepy.editor import VideoFileClip
import os
from pydub import AudioSegment

PATH = r"F:\TOURS\others\ما بعد الأساسيات - Beyond the basics"


def get_audios(path):
    videos = []
    for i, video_file in enumerate(os.listdir(path)):
        vid_file = video_file.encode("utf-16", "ignore").decode("utf-16")
        if vid_file.endswith(".webm") or vid_file.endswith(".mp4"):
            try:
                video_path = os.path.join(path, vid_file)
                if "-" in vid_file:
                    new_name = vid_file.replace("-", "")
                    os.rename(video_path, os.path.join(path, new_name))
                    video_path = os.path.join(path, new_name)
                print(f"({i + 1}) {video_path}")
                video = VideoFileClip(video_path)
                videos.append(video)
            except:
                continue

    for i, video in enumerate(videos):
        audio = video.audio
        audio.write_audiofile(f"{i + 1}.mp3")
        
def cleanup():
    cwd = os.getcwd()
    for i, audio in enumerate(cwd):
        if audio.endswith(".mp3"):
            os.remove(audio)


def merge_audios():
    final_audio = AudioSegment.empty()
    cwd = os.getcwd()
    audios = [os.path.join(cwd, audio) for audio in os.listdir(cwd) if audio.endswith(".mp3")]
    for i, audio in enumerate(audios):
        print(f"({i + 1}) {audio}")
        if audio.endswith(".mp3"):
            final_audio += AudioSegment.from_file(audio, format="mp3")
    print(f"Final audio: {final_audio}")
    final_audio.export("final.mp3", format="mp3")
    return


if __name__ == "__main__":
    audios = get_audios(PATH)
    merge_audios()
    cleanup()
