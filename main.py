from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from pydub import AudioSegment, silence
from SubtitleGenerator import SubtitleGenerator
import tkinter as tk
from tkinter import filedialog
import os.path


def genererVideo(videopath, resultpath):
    video = VideoFileClip(videopath)
    if not os.path.exists("audio.wav"):
        video.audio.write_audiofile("audio.wav")
    subGenerator = SubtitleGenerator(video, "audio.wav", "Arial", 20, "white", "black", 0.25, "caption", "center", (video.w, 100))
    subtitles = subGenerator.create_subtitles()
    result = CompositeVideoClip([video, subtitles.set_pos(("center", "bottom"))])
    #Enregistrer la vidéo avec les sous-titrs ajoutés
    result.write_videofile(resultpath, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    #Supprimer l'audio généré précédemment
    os.remove("audio.wav")

def chooseVideo():
    file = filedialog.askopenfile()
    if file:
        file_name = os.path.basename(file.name)
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(0, file_name)
        
window = tk.Tk()
window.geometry("600x400")



file_name_entry = tk.Entry(window)
file_name_entry.pack()

choose_video_button = tk.Button(window, text="Choose a video", command=chooseVideo)
choose_video_button.pack()

generate_button = tk.Button(window, text="Générer la vidéo", command= lambda: genererVideo(file_name_entry.get(), file_name_entry.get() + "_withsubtitles.mp4"))
generate_button.pack()

window.mainloop()

