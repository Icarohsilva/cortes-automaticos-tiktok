from moviepy import VideoFileClip

clip = VideoFileClip("original/video_original.mp4")
print("Funções disponíveis em VideoFileClip:")
print(dir(clip))