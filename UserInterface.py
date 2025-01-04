import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from PIL import Image, ImageTk

# Import the functions from the external script (morph_operations.py)
import MorphologicalOperation

def run_script(script_name):
    """Run an external Python script when a menu option is clicked."""
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run script: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"The script '{script_name}' was not found.")

def pick_and_show_image():
    """Allow the user to pick an image and display it in its original size."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        try:
            img = Image.open(file_path)
            
            # Check the size of the image to see if we need to scale it to fit within the window
            window_width = root.winfo_width()
            window_height = root.winfo_height()

            # Only resize if the image is larger than the window size
            img_width, img_height = img.size
            if img_width > window_width or img_height > window_height:
                img.thumbnail((window_width, window_height), Image.Resampling.LANCZOS)
            
            img_tk = ImageTk.PhotoImage(img)

            # Update the label with the new image
            img_label.config(image=img_tk)
            img_label.image = img_tk  # Keep a reference to the image to prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

# Create the main application window
root = tk.Tk()
root.title("Binary Image Processing")

# Set a fixed size for the main window
window_width = 1200
window_height = 800
root.geometry(f"{window_width}x{window_height}")
# root.resizable(False, False)  # Disable window resizing

# Create a menu bar
menu_bar = tk.Menu(root)

# Add "Option 1" to the menu bar
menu_bar.add_command(label="Binary Image Conversion", command=lambda: run_script("toBinaryImg.py"))

# Add "Option 2" with a submenu containing 4 options, calling functions from morph_operations.py
submenu = tk.Menu(menu_bar, tearoff=0)
submenu.add_command(label="Erosion", command=MorphologicalOperation.display_erosion)
submenu.add_command(label="Dilation", command=MorphologicalOperation.display_dilation)
submenu.add_command(label="Opening", command=MorphologicalOperation.display_opening)
submenu.add_command(label="Closing", command=MorphologicalOperation.display_closing)
menu_bar.add_cascade(label="Morphological Operation", menu=submenu)

# Add "Option 3"
menu_bar.add_command(label="Denoise", command=lambda: run_script("BinaryImgDenoise.py"))

# Add "Option 4"
menu_bar.add_command(label="Connecting Region Labeling", command=lambda: run_script("BinaryImgConnectRegionLabeling.py"))

# Attach the menu bar to the application
root.config(menu=menu_bar)

# Create a button to pick an image
pick_image_button = tk.Button(root, text="Pick an Image", command=pick_and_show_image)
pick_image_button.pack(pady=10)

# Frame to hold the images
image_frame = tk.Frame(root)
image_frame.pack()

# Label to display the selected image
img_label = tk.Label(image_frame)
img_label.image = None  # Initialize the image reference to avoid any issues
img_label.pack(side=tk.LEFT, padx=10)

# Run the application
root.mainloop()
