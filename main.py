import ffmpeg
import os
print("Josiah FFMPEG UI")
video = input("Input your video file: ")
videoName = video.split(".")[0]
videoNameOG = video.split(".")[0]

stream = ffmpeg.input(video)

def audioConvert():
    global video, videoNameOG
    (
        ffmpeg
        .input(video)
        .output(f"{videoNameOG}.{input('What is the extension for your audio?')}")
        .run()
    )
    print("Converted!")

while True:
    print(f"""
    Working on {videoName}
    ---
    Controls
    1. Flip video
    2. Overlay
    3. Trim (frames)
    ---
    Process
    r. Run processes
    a. Convert to audio
    """)
    choice = input("Input a choice: ")
    if choice.startswith("1"):
        stream = ffmpeg.hflip(stream)
        videoName = f"{videoName}_flipped"
    elif choice.startswith("2"):
        imgStream = ffmpeg.input(input("Input your image file: "))
        stream = ffmpeg.overlay(stream, imgStream)
        videoName = f"{videoName}_overlay"
    elif choice.startswith("3"):
        videoName = f"{videoName}_trimmed"
        stream = ffmpeg.trim(stream, start_frame=int(input("Start frame: ")), end_frame=int(input("End frame: ")))
    elif choice.startswith("r"):
        break
    elif choice.startswith("a"):
        audioConvert()
        exit(0)

ostream = ffmpeg.output(stream, videoName + "-noAudio.mp4")
audioStream = ffmpeg.output(stream, videoName + "-audio.mp3", acodec="mp3")

ffmpeg.run(ostream)
try:
    ffmpeg.run(audioStream)
except:
    print("Audio failed. No audio will be written.")
    noAudio = True


if not noAudio:
    finalVideoStream = ffmpeg.input(videoName + "-noAudio.mp4")
    finalAudioStream = ffmpeg.input(videoName + "-audio.mp3")
    finalStream = ffmpeg.concat(finalVideoStream, finalAudioStream)

    ffmpeg.run(finalStream)

    os.remove(videoName + "-noAudio.mp4")

os.remove(videoName + "-audio.mp3")

if noAudio:
    os.rename(videoName + "-noAudio.mp4", videoName + ".mp4")

print(f"Done! You can see it at {videoName}.mp4 now.")