import subprocess

def compress_video_av1(input_file, output_file):
    command = [
        'ffmpeg', '-i', input_file,
        '-c:v', 'libaom-av1',  # Use AV1 codec
        '-crf', '30',          # Compression quality (lower = better, 30 is a good start)
        '-b:v', '0',           # Constant rate factor mode
        '-c:a', 'aac',         # Audio codec
        '-b:a', '128k',        # Audio bitrate
        output_file
    ]
    subprocess.run(command)

compress_video_av1(r"E:\Learnings\Tours\The Programming Tour\Testing\SoftWare testing\Software_Testing_Course_in_Arabic__%2320_-_Behavior_Driven_Development__BDD___%D8%A8%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A_software_testing(0).mp4", r'output_av1.mkv')
i = input("Press Enter to exit")