from cv2 import VideoCapture , imread,imwrite,cvtColor,COLOR_BGR2GRAY,COLOR_BGR2RGB,resize
import tkinter as tk
from tkinter import filedialog , messagebox
import os
from PIL import Image, ImageTk

global_image=None #image yaha
global_file_path=None #filepath yaha

Dark_Blue = "#2C3E50"
Light_Blue = "#3498DB"
Hover_Blue = "#2980B9"
White = "#FFFFFF"
Light_Gray = "#BDC3C7"


# click image
def click_image():
    global global_image, global_file_path
    try:
        cam = VideoCapture(0)
        result, image = cam.read()
        if result:
            global_file_path, global_image = save_as(image)
            display_choosen_image()
            display_converted_image(None,None)
            convert_button['state'] = 'normal'
        else:
            raise Exception("Failed to capture image")
    except Exception as e:
        messagebox.showerror("Camera Error", error)
    finally:
        cam.release()


# save image
def save_as(image):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            imwrite(file_path, image)
            return file_path, image
        else:
            raise Exception("No file path selected")
    except Exception as error:
        messagebox.showerror("Save Error", error)
        return None, None


#choose image
def choose_image():
    global global_image, global_file_path
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            image = imread(file_path)
            if image is not None:
                global_image = image
                global_file_path = file_path
                display_choosen_image()
                display_converted_image(None,None)

                convert_button['state'] = 'normal'
            else:
                raise Exception("Unable to read the selected file")
        else:
            raise Exception("No file selected")
    except Exception as error:
        messagebox.showerror("File Selection Error",error)

# grayscale image
def grayscale():
    global global_image, global_file_path
    try:
        if global_image is not None and global_file_path is not None:
            grayscale_image = cvtColor(global_image, COLOR_BGR2GRAY)
            if grayscale_image is not None:
                file, ext = os.path.splitext(global_file_path)
                new_path = f"{file}_gray{ext}"
                imwrite(new_path, grayscale_image)
                messagebox.showinfo("Success", f"Grayscale image saved as {new_path}")
                global_file_path = None
                global_image = None
                display_converted_image(grayscale_image,new_path)
                convert_button['state'] = 'disabled'
            else:
                raise Exception("Conversion failed")
        else:
            raise Exception("No image selected")
    except Exception as error:
        messagebox.showerror("Grayscale Conversion Error", error)   

#updates image on screen 
#  cv2 image incompatible with tk so had to convert to bgr to rgb then use pillow to convert to array then to some tk compatible image          
def display_choosen_image():
    global global_image, global_file_path
    if global_image is not None:
        rgb_image = cvtColor(global_image, COLOR_BGR2RGB)
        height, width = rgb_image.shape[:2]
        if height>300 or width>400 :
            scale_height = 300 / height
            scale_width = 400 / width
            scale = min(scale_height, scale_width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            rgb_image = resize(rgb_image, (new_width, new_height))
        image = Image.fromarray(rgb_image)
        photo = ImageTk.PhotoImage(image)
        choosen_image_label.config(image=photo)
        choosen_image_label.image = photo
        choosen_filepath_label.config(text=f"File: {global_file_path}")
    else:
        choosen_image_label.config(image=None)
        choosen_filepath_label.config(text="No image selected")

def display_converted_image(converted_image,converted_filepath):
    if converted_image is not None:
        rgb_image = cvtColor(converted_image, COLOR_BGR2RGB)
        height, width = rgb_image.shape[:2]
        if height>300 or width>400 :
            scale_height = 300/ height
            scale_width = 400 / width
            scale = min(scale_height, scale_width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            rgb_image = resize(rgb_image, (new_width, new_height))
        image = Image.fromarray(rgb_image)
        photo = ImageTk.PhotoImage(image)
        converted_filepath_label.grid()
        converted_image_label.grid()
        converted_image_label.config(image=photo)
        converted_image_label.image = photo
        converted_filepath_label.config(text=f"File: {converted_filepath}")
        arrow_label.grid()
    else:
        converted_image_label.config(image=None)
        converted_image_label.image = None
        converted_filepath_label.config(text="")        
        arrow_label.grid_remove()
        converted_filepath_label.grid_remove()
        converted_image_label.grid_remove()

def on_enter(e):
    e.widget['background'] = Hover_Blue

def on_leave(e):
    e.widget['background'] = Light_Blue

root = tk.Tk()
root.title("Grayscale Image Studio")
root.state("zoomed")
root.configure(bg=Dark_Blue)
root.geometry("700x500")

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

display_frame = tk.Frame(main_frame, bg=Dark_Blue)
display_frame.pack(pady=10)

choosen_image_label = tk.Label(display_frame, bg=Dark_Blue)
choosen_image_label.grid(padx=10,row=0,column=0)

choosen_filepath_label = tk.Label(display_frame, text="No image selected", font=("Helvetica", 10), fg=White, bg=Dark_Blue)
choosen_filepath_label.grid(pady=5,padx=10,row=1,column=0)

converted_image_label = tk.Label(display_frame, bg=Dark_Blue)
converted_image_label.grid(padx=10,row=0,column=2)
converted_image_label.grid_remove()

converted_filepath_label = tk.Label(display_frame, text="", font=("Helvetica", 10), fg=White, bg=Dark_Blue)
converted_filepath_label.grid(padx=10,pady=5,row=1,column=2)
converted_filepath_label.grid_remove()

arrow_image = Image.open("arrow.png")
arrow_image = arrow_image.resize((50, 50))
arrow_photo = ImageTk.PhotoImage(arrow_image)

arrow_label = tk.Label(display_frame, image=arrow_photo, bg=Dark_Blue)
arrow_label.grid(padx=10, row=0, column=1)
arrow_label.grid_remove() 


footer_frame = tk.Frame(root, bg=Dark_Blue)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

footer_label = tk.Label(footer_frame, text="© I Just Added This To Use Some Space", font=("Helvetica", 10), fg=Light_Gray, bg=Dark_Blue)
footer_label.pack()

for button in [choose_button, capture_button, convert_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

root.mainloop()

