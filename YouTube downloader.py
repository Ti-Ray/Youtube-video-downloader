from pytube import YouTube
from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from PIL import *

pg = Tk()
pg.title("Youtube Download System")
pg.geometry("500x500")
pg.config(bg="white")
img_top = PhotoImage(file="youtube.png")
img_top = img_top.subsample(4,4)
Label(pg, text="YouTube Download System", bg="white", font=("gothic", "18")).pack(anchor=CENTER, padx=10, pady=10)
Label(pg, image=img_top).pack(padx=10, pady=10)

def plc():
    pth = filedialog.askdirectory()
    path_label.config(text=pth)

def exit():
    pg.destroy()

def down():
    try:
        url = ent1.get()
        video = YouTube(url)
        file_pth = path_label.cget("text")
        pg.title('Downloading. . . .')
        Label(pg, text=(video.title), font="bold", bg="grey").pack(padx=10, pady=10)
        vid = YouTube(url).streams.get_highest_resolution().download(file_pth)
        pg.title('Download complete.')
        ent1.delete(0, END)
    except:
        messagebox.showinfo("Error", "Plz enter a link !")

path_label = Label(pg, text="Select File Directory: ", font="bold", bg="white")
path_label.pack(padx=10, pady=10)
Label(pg, text="Enter your video link", bg="white", font="bold").pack(anchor=CENTER, padx=10, pady=10)
ent1 = Entry(pg, width=30, bg="white")
ent1.pack(anchor=CENTER, padx=10, pady=10)
link = ""
btn = Button(pg, text="Download", font="bold", bg="gold", command=down)
btn.pack(anchor=CENTER, padx=10, pady=10)
plc_btn = Button(pg, text="Select Folder", font="bold", bg="gold", command=plc)
plc_btn.pack(anchor=CENTER, padx=10, pady=10)
close_btn = Button(pg, text="Close", font="bold", command=exit, bg="red")
close_btn.pack(padx=10, pady=10)

pg.mainloop()
