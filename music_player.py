import pygame
import os
from tkinter import Tk, filedialog
from tkinter import ttk
from tkinter import StringVar

def initialize_mixer():
    pygame.mixer.init()

def get_music_files():
    music_files = []
    current_directory = os.getcwd()
    for file in os.listdir(current_directory):
        if file.endswith(".mp3"):
            music_files.append(file)
    return music_files

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def main():
    initialize_mixer()

    root = Tk()
    root.title("Music Player")

    song_list = get_music_files()
    current_song_index = 0

    def play_next_song():
        nonlocal current_song_index
        current_song_index = (current_song_index + 1) % len(song_list)
        play_selected_song()

    def play_previous_song():
        nonlocal current_song_index
        current_song_index = (current_song_index - 1) % len(song_list)
        play_selected_song()

    def play_selected_song():
        file_path = song_list[current_song_index]
        play_music(file_path)
        update_song_label()

    def select_song():
        file_path = filedialog.askopenfilename(title="Select a music file", filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
        if file_path:
            song_list.append(file_path)
            nonlocal current_song_index
            current_song_index = len(song_list) - 1
            play_selected_song()

    def update_song_label():
        song_label.config(text="Currently Playing: " + os.path.basename(song_list[current_song_index]))

    volume_label = ttk.Label(root, text="Volume")
    volume_label.pack(pady=10)

    volume_scale = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=set_volume)
    volume_scale.set(70)
    volume_scale.pack()

    play_button = ttk.Button(root, text="Play", command=play_selected_song)
    play_button.pack(pady=10)

    stop_button = ttk.Button(root, text="Stop", command=stop_music)
    stop_button.pack(pady=10)

    pause_button = ttk.Button(root, text="Pause", command=pause_music)
    pause_button.pack(pady=10)

    resume_button = ttk.Button(root, text="Resume", command=resume_music)
    resume_button.pack(pady=10)

    next_button = ttk.Button(root, text="Next", command=play_next_song)
    next_button.pack(pady=10)

    previous_button = ttk.Button(root, text="Previous", command=play_previous_song)
    previous_button.pack(pady=10)

    select_song_button = ttk.Button(root, text="Select Song", command=select_song)
    select_song_button.pack(pady=10)

    song_label = ttk.Label(root, text="Currently Playing: ")
    song_label.pack(pady=10)

    def update_progress():
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            song = pygame.mixer.Sound(song_list[current_song_index])
            song_length = song.get_length()
            progress = (current_time / song_length) * 100
            progress_var.set(progress)
            root.after(1000, update_progress)

    progress_var = StringVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(fill="x", pady=10)

    update_progress()

    root.mainloop()

if __name__ == "__main__":
    main()
