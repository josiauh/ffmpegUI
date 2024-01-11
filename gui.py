from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
import ffmpeg
import os

currentVid = None
stream = None
videoName = None
videoNameOG = None
#region Commands
def openVideo():
    global stream, videoName, videoNameOG, currentVid
    currentVid = filedialog.askopenfile(initialdir=".", title="Select a video")
    videoLabel.configure(text=f"Current video: {currentVid.name}")
    stream = ffmpeg.input(currentVid.name)
    if len(os.path.basename(currentVid.name).split(".")) > 2:
        messagebox.showwarning("Multiple . in file", "This will change your video's name.")
    videoName = os.path.basename(currentVid.name).split(".")[0]
    videoNameOG = videoName

def deloadVideo():
    global stream, videoName, videoNameOG, currentVid
    currentVid = None
    videoLabel.configure(text=f"No video.")
    stream = None
    videoName = None
    videoNameOG = None

def flipVideo():
    global stream, videoName
    if stream == None:
        messagebox.showerror("No video", "You don't have a video.")
    else:
        stream = ffmpeg.hflip(stream)
        videoName = videoName + "_flipped"

def runStream():
    global stream, videoName
    if stream == None:
        messagebox.showerror("No video", "You don't have a video.")
    else:
        stream = ffmpeg.output(stream, videoName + f".{extensionThing.get(INSERT, END)}'")
        ffmpeg.run(stream)
        messagebox.showinfo("Ran", f"Run complete!")

def overlay():
    global stream, videoName
    overlayImage = filedialog.askopenfile(initialdir=".", title="Select the image to overlay.")
    overlayImageStream = ffmpeg.input(overlayImage.name)
    stream = ffmpeg.overlay(stream, overlayImageStream)

def helpDialog():
    global theme
    helpDia = Tk()
    helpDia.title("Help")
    helpDia.tk.call("source", "azure.tcl")
    helpDia.tk.call("set_theme", theme)
    Label(helpDia, text="Josiah FFMPEG UI is a UI for doing things related to FFMPEG.\nEvery time you add a control, it adds it to the FFMPEG stream.\nWhen ready, run the process.").pack()
    Button(helpDia, text="Exit", command=helpDia.destroy).pack()

def audioConvert():
    global stream, videoNameOG
    if stream == None:
        messagebox.showerror("No video", "You don't have a video.")
    else:
        stream = ffmpeg.output(stream, f'{videoNameOG}.{extensionThing.get("1.0", END)}')
        ffmpeg.run(stream)
        messagebox.showinfo("Converted", f"Conversion complete!")
    
def setVideoExtension():
    global extensionThing
    extensionThing.delete("1.0", END)
    extensionThing.insert(INSERT, "mp4")

def setAudioExtension():
    global extensionThing
    extensionThing.delete("1.0", END)
    extensionThing.insert(INSERT, "mp3")

def change_theme():
    global theme
    # NOTE: The theme's real name is azure-<mode>
    if app.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        theme = "light"
        app.tk.call("set_theme", "light")
    else:
        # Set dark theme
        theme = "dark"
        app.tk.call("set_theme", "dark")
#endregion
theme = "dark"
darkOn = False
app = Tk()

app.title("Josiah ffmpeg UI")
app.geometry("500x500")
app.iconphoto(True, PhotoImage(file="ffmpegJosiauhIcon.png"))
app.tk.call("source", "azure.tcl")
app.tk.call("set_theme", theme)

title = Label(app, text="Josiah FFMPEG")
title.pack()
videoLabel = Label(app, text="No video.")
videoLabel.pack()
openButton = Button(app, text="Open", command=openVideo)
openButton.pack()
Button(app, text="Unload", command=deloadVideo).pack()
Separator(app, orient="horizontal").pack(fill='x')
Label(app, text="Controls").pack()
flipButton = Button(app, text="Flip Video", command=flipVideo)
flipButton.pack()
Button(app, text="Overlay Image").pack()
Separator(app, orient="horizontal").pack(fill='x')
Label(app, text="Process").pack()
runButton = Button(app, text="Run", command=runStream)
runButton.pack()
Button(app, text="Audio Convert", command=audioConvert).pack()
Label(app, text="Extension (default: mp4 for video, mp3 for audio)").pack()
extensionThing = Text(app, height=1, width=25)
extensionThing.insert(INSERT, "mp4")
extensionThing.pack()
Separator(app, orient="horizontal").pack(fill='x')
Label(app, text="Extensions").pack()
Button(app, text="Audio", command=setAudioExtension).pack()
Button(app, text="Default", command=setVideoExtension).pack()
Separator(app, orient="horizontal").pack(fill='x')
Button(app, text="Help", command=helpDialog).pack()
Button(app, text="Change Theme", style='Accent.TButton', command=change_theme).pack()

app.mainloop()