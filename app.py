import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image OCR Application")

        # Create a button to open file dialog
        self.open_button = tk.Button(root, text="Select Image", command=self.open_image)
        self.open_button.pack()

        # Label to display selected image
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Text widget to display extracted text
        self.text_widget = tk.Text(root, wrap='word', height=20, width=80)
        self.text_widget.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*")]
        )
        if not file_path:
            return
        
        try:
            img = Image.open(file_path)
            self.display_image(img)
            text = self.perform_ocr(img)
            self.display_text(text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_image(self, img):
        img.thumbnail((300, 300))  # Resize image for display
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

    def perform_ocr(self, img):
        text = pytesseract.image_to_string(img)
        return text

    def display_text(self, text):
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
