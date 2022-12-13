from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import speech_recognition as sr
import os.path
from pydub import AudioSegment, silence

class SubtitleGenerator:
    def __init__(self, video, audio, font, fontsize, color, stroke_color, stroke_width, method, align, size):
        self.video = video
        self.audiopath = audio
        self.r = sr.Recognizer()
        self.audio = sr.AudioFile(audio)
        self.text = self.extract_text()
        self.subtitle_properties = {
            "font": font,
            "fontsize": fontsize,
            "color": color,
            "stroke_color": stroke_color,
            "stroke_width": stroke_width,
            "method": method,
            "align": align,
            "size": size
        }
        self.generator = lambda txt: TextClip(txt, **self.subtitle_properties)

    def extract_text(self):
        # Utiliser l'API de reconnaissance vocale pour extraire le texte à partir de l'audio
        with self.audio as source:
            audio_file = self.r.record(source)
        return self.r.recognize_google(audio_file)

    def create_subtitles(self):
        # Utiliser pydub pour synchroniser les sous-titres à l'audio en détectant les silences
        audio_segment = AudioSegment.from_file(self.audiopath)
        non_silent_sections = silence.detect_nonsilent(audio_segment, min_silence_len=350, silence_thresh=-35)
        
        non_silent_durations = []
        
        for non_silent_section in non_silent_sections:
            non_silent_durations.append(non_silent_section[1] - non_silent_section[0])
            
        
        #Calculer le ratio de mots par secondes
        total_text_length = len(self.text)
        total_non_silent_durations = sum(non_silent_durations)
        words_per_second = total_text_length/total_non_silent_durations
        
        #Découper le texte en segments en fonction de la durée des sections non silencieuses
        text_segments = []
        current_segment = ""
        current_segment_length = 0
        for word in self.text.split(" "):
            current_segment += word + " "
            current_segment_length += len(word)
            if current_segment_length / words_per_second >= non_silent_durations[len(text_segments)]:
                text_segments.append(current_segment)
                current_segment = ""
                current_segment_length = 0
            if current_segment_length / words_per_second < non_silent_durations[-1] - non_silent_durations[-2]:
                text_segments[-1] += current_segment
                
        #Créer les sous-titres
        subs = []
        start_time = 0
        for segment in text_segments:
            end_time = start_time + non_silent_durations[len(subs)]
            if start_time == 0:
                subs.append(((start_time, end_time/1000), segment))
            else:
                subs.append(((start_time/1000, end_time/1000), segment))
            start_time = end_time
                
        
        return SubtitlesClip(subs, self.generator)    
    
