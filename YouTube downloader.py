from tkinter import messagebox
from PIL import *
import yt_dlp
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import threading

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
app = ctk.CTk()
app.geometry("800x700")
app.title("Youtube Download System")
ytb_image_path = Image.open("youtube.png")
ytb_image = ctk.CTkImage(light_image=ytb_image_path,size=(200, 100))

def exit():
    app.destroy()
    

from tkinter import filedialog, messagebox  # Ensure these are imported

def get_file_path():
    vid_url = video_link.get().strip()
    file_pth = download_path.cget("text")
    # Check if URL and path are provided
    if not vid_url:
        messagebox.showerror("Error", "Please enter a video URL!")
        return
    
    pth = filedialog.askdirectory()
    
    # Checks if a directory was selected
    if pth:
        download_path.configure(text=pth)
        down()
    else:
        messagebox.showwarning("Directory Missing", "Please select a directory to save the video.")


def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', None)
        
        if total_bytes:
            percent = downloaded_bytes / total_bytes
            progress_bar.set(percent)
            progress_text.insert(
                "end", 
                f"Downloading: {int(percent * 100)}% ({downloaded_bytes / 1e6:.2f} MB of {total_bytes / 1e6:.2f} MB)\n"
            )
        else:
            progress_text.insert("end", f"Downloading: {downloaded_bytes / 1e6:.2f} MB downloaded\n")
        
        progress_text.see("end")  # Scroll to the latest log

    elif d['status'] == 'finished':
        progress_text.insert("end", "Download Complete\n")
        progress_text.see("end")
        progress_bar.set(1)
        


def down():
    try:
        url = video_link.get().strip()
        file_pth = download_path.cget("text")
        if file_pth == "Select File Directory":
            messagebox.showerror("Error", "Please select a file directory!")
            return

        selected_format = format_select.get()  #Fetch the selected format from the dropdown 
        yt_opts = {
            'outtmpl': f'{file_pth}/%(title)s.%(ext)s',
            'format': 'bestaudio/best' if selected_format == 'MP3' else 'bestvideo+bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}] if selected_format == 'MP3' else [],
            'nocolor': True,
            'progress_hooks': [progress_hook],
        }

        # Starts the download in a new thread
        def download_thread():
            try:
                progress_text.delete("1.0", "end")
                progress_bar.set(0)
                app.title('Downloading...')
                with yt_dlp.YoutubeDL(yt_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                video_title = info.get("title", "Unknown Title")
                app.title('Download complete.')

                # Success
                messagebox.showinfo("Success", f"Download completed: {video_title}")
                video_link.delete(0, "end")
            except yt_dlp.utils.DownloadError as e:
                messagebox.showerror("Download Error", f"An error occurred: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

        # Starts the thread
        threading.Thread(target=download_thread).start()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")



label_with_image = ctk.CTkLabel(app, image=ytb_image, text=" ")
label_with_image.pack(pady=20)

download_path = ctk.CTkLabel(master=app, text="Select File Directory")
download_path.pack(padx=10, pady=10)

download_link_label = ctk.CTkLabel(master=app, text="ENTER THE DOWNLOAD LINK BELLOW")
download_link_label.pack(padx=10, pady=10)

video_link = ctk.CTkEntry(master=app)
video_link.pack(padx=10, pady=10)

format_option_label = ctk.CTkLabel(master=app, text="Select Format:")
format_option_label.pack(padx=10, pady=5)

format_select = ctk.CTkOptionMenu(master=app, values=["MP4", "MP3"])
format_select.set("MP4")
format_select.pack(padx=10, pady=5)

download_btn = ctk.CTkButton(master=app, text="DOWNLOAD", command=get_file_path)
download_btn.pack(padx=10, pady=10)

progress_bar = ctk.CTkProgressBar(master=app, width=400)
progress_bar.pack(pady=10)
progress_bar.set(0)

progress_text = ctk.CTkTextbox(master=app, width=500, height=200)
progress_text.pack(padx=10, pady=10)


close_btn = ctk.CTkButton(master=app, command=exit, text="close")
close_btn.pack(padx=10, pady=10)

app.mainloop()

