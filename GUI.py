import os.path
import ssl
import customtkinter as ctk
from pytube import YouTube


app = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


app.title("Youtube Downloader")
app.geometry("500x300")


def clear_entry():
    entry.delete(0, last_index=6000)


def download_youtube_video(link):
    resolution = combo_var.get()
    ssl._create_default_https_context = ssl._create_unverified_context
    yt = YouTube(link, on_progress_callback=on_progress)
    download_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    try:
        if resolution == "Высокое разрешение":
            yt.streams.get_highest_resolution().download(output_path=download_path, filename=f"{yt.title}.mp4")
        elif resolution == "Низкое разрешение":
            yt.streams.get_lowest_resolution().download(output_path=download_path, filename=f"{yt.title}.mp4")
        elif resolution == "Только звук":
            yt.streams.get_audio_only().download(output_path=download_path, filename=f"{yt.title}.mp3")
        else:
            yt.streams.get_by_resolution(resolution).download(output_path=download_path, filename=f"{yt.title}.mp4")
        os.path.join(r"Desktop", f"{yt.title}.mp4")
        status_label.configure(text="Скачено!", text_color="green")
        status_label.update()
    except Exception:
        status_label.configure(text="!Ошибка! Возможно не подходит разрешение или неверная ссылка", text_color="red")


def on_progress(stream, chunk, bytes_remaining):
    total = stream.filesize
    bytes_downloaded = total - bytes_remaining
    per_complited = bytes_downloaded / total * 100
    print(per_complited)
    progressbar.update()
    progressbar.set(float(per_complited / 100))


name = ctk.CTkLabel(app, text="Введите ссылку для скачивания", justify="center", font=("Arial", 20), fg_color="transparent")
name.grid(row=0, column=0, padx=10, pady=20)

entry = ctk.CTkEntry(app, width=450, placeholder_text="Здесь текст Вашей ссылки...")
entry.grid(row=1, column=0, padx=10, pady=8)

btn_download = ctk.CTkButton(app, text="Скачать!", command=lambda: download_youtube_video(entry.get()))
btn_download.grid(row=2, column=0, padx=(90, 0), sticky='w')


btn_clear = ctk.CTkButton(app, text="Очистить поле", command=lambda: clear_entry())
btn_clear.grid(row=2, column=0, padx=(0, 90), sticky='e')

combo_text = ["Высокое разрешение", "Низкое разрешение", "Только звук", "360p", "480p", "720p",]
combo_var = ctk.StringVar()
combobox = ctk.CTkComboBox(app, values=combo_text, width=200, variable=combo_var)
combobox.grid(row=3, column=0, pady=10)
combobox.set("720p")

status_label = ctk.CTkLabel(app, text="")
status_label.grid()

progressbar = ctk.CTkProgressBar(app, width=400, mode="determinate", progress_color="green", corner_radius=4)
progressbar.set(0)
progressbar.grid()

app.mainloop()
