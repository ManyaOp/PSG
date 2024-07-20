from cv2 import VideoCapture , imread,imwrite,cvtColor,COLOR_BGR2GRAY
import tkinter as tk
from tkinter import filedialog 
import os

global_image=None #image stored here
global_file_path=None

Dark_Blue="#2C3E50"
White="#ECF0F1"


#function to click image
def click_image():
    global global_image , global_file_path
    cam=VideoCapture(0)
    result , image = cam.read()
    if result is not None:
        global_file_path,global_image=save_as(image)
        convert_button['state'] = 'normal'

    else:
        pass #show some error


#function to save image
def save_as(image):

    file_path = filedialog.asksaveasfilename(defaultextension=".png")

    if file_path is not None:
        imwrite(file_path,image)
        return file_path,image
        #msg to sucess    
    else:
        pass #msg to fail


#function to choose image
def choose_image():
    global global_image , global_file_path

    file_path = filedialog.askopenfilename(filetypes=[
        ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")
    ])    
    if file_path is not None:
        image=imread(file_path)
        if image is not None:
            global_image=image
            global_file_path=file_path
            convert_button['state'] = 'normal'

        else:
            pass #error cant read file 

    else: 
        pass #msg that file not selected
#function to grayscale image
def grayscale():
    global global_image , global_file_path
    grayscale_image=None
    if global_image is not None and global_file_path is not None:
        grayscale_image = cvtColor(global_image, COLOR_BGR2GRAY)
        if grayscale_image is not None:
            file,ext=os.path.splitext(global_file_path)
            new_path=f"{file}_gray{ext}"
            imwrite(new_path,grayscale_image)
            #some msg to save sucess
            global_file_path=None
            global_image=None
            convert_button['state'] = 'disabled'

        else:
            pass #some conversion error
    else: 
        pass #msg image not selected    



Dark_Blue = "#2C3E50"
Light_Blue = "#3498DB"
Hover_Blue = "#2980B9"
White = "#FFFFFF"
Light_Gray = "#BDC3C7"

root = tk.Tk()
root.title("Grayscale Image Studio")
root.geometry("500x400")
root.configure(bg=Dark_Blue)

main_frame = tk.Frame(root, bg=Dark_Blue, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(main_frame, text="Grayscale Image Studio", font=("Helvetica", 24, "bold"), fg=White, bg=Dark_Blue)
title_label.pack(pady=(0, 20))

input_frame = tk.Frame(main_frame, bg=Dark_Blue)
input_frame.pack(pady=10)

choose_button = tk.Button(input_frame, text="Choose Image", bg=Light_Blue, fg=White, font=("Helvetica", 12, "bold"), padx=10, pady=10, width=20,command=choose_image)
choose_button.grid(row=0, column=0, padx=10)

capture_button = tk.Button(input_frame, text="Capture Photo(•ᴗ•)", bg=Light_Blue, fg=White, font=("Helvetica", 12, "bold"), padx=10, pady=10, width=20 , command=click_image)
capture_button.grid(row=0, column=1, padx=10)

convert_button = tk.Button(main_frame, text="Convert to Grayscale", state='disabled', bg=Light_Blue, fg=White, font=("Helvetica", 12, "bold"), padx=10, pady=10, width=20,command=grayscale)
convert_button.pack(pady=20)

footer_frame = tk.Frame(root, bg=Dark_Blue)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

footer_label = tk.Label(footer_frame, text="© I Just Added This To Use Some Space", font=("Helvetica", 10), fg=Light_Gray, bg=Dark_Blue)
footer_label.pack()

def on_enter(e):
    e.widget['background'] = Hover_Blue

def on_leave(e):
    e.widget['background'] = Light_Blue

for button in [choose_button, capture_button, convert_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

root.mainloop()

