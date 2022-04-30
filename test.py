import os
# os.system(
#     "spotdl https://open.spotify.com/track/6Sflud15ff1KqBzg6wj78S?si=f29da68ad34f4250")
# os.system("yt-dlp https://youtu.be/yhbVFtaBmso --extract-audio --audio-format mp3")
link = "https://open.spotify.com/track/6Sflud15ff1KqBzg6wj78S?si=f29da68ad34f4250"
command = link+" --path-template "+"./umusic/{title}.{ext}"
print(command)
os.system(f"spotdl {command}")
# command = str(link)+" - -extract-audio - -audio-format mp3 -o " + \
#     "./umusic/%(title)s.%(ext)s"
# link = "https://youtu.be/yhbVFtaBmso"
# command = f"{link} --extract-audio --audio-format mp3 -o ./umusic/%(title)s.%(ext)s"
# os.system(f"yt-dlp {command}")
