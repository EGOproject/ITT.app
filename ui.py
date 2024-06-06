import os
import tkinter as tk
from tkinter import filedialog, messagebox
from dashboard import Dashboard
from ocr import perform_ocr
from grammar import correct_grammar
from file_operations import save_as_word, save_as_pdf, save_as_text, save_job, load_previous_jobs

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image OCR Application")

        self.dashboard = Dashboard(self.root, self)
        self.dashboard.pack()

    def start_new(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*")]
        )
        if not self.file_path:
            return

        try:
            self.img_text = perform_ocr(self.file_path)
            self.corrected_text = correct_grammar(self.img_text)
            self.display_result()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_result(self):
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("OCR Result")

        self.text_widget = tk.Text(self.result_window, wrap='word')
        self.text_widget.pack()
        self.text_widget.insert(tk.END, self.corrected_text)

        self.save_word_button = tk.Button(self.result_window, text="Save as Word", command=self.save_as_word)
        self.save_word_button.pack()

        self.save_pdf_button = tk.Button(self.result_window, text="Save as PDF", command=self.save_as_pdf)
        self.save_pdf_button.pack()

        self.save_text_button = tk.Button(self.result_window, text="Save as Text", command=self.save_as_text)
        self.save_text_button.pack()

        self.copy_button = tk.Button(self.result_window, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack()

    def save_as_word(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".docx")
        if file_path:
            save_as_word(self.corrected_text, file_path)

    def save_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if file_path:
            save_as_pdf(self.corrected_text, file_path)

    def save_as_text(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            save_as_text(self.corrected_text, file_path)

    def save_job(self):
        job_name = save_job(self.corrected_text)
        messagebox.showinfo("Job Saved", f"Job '{job_name}' saved successfully.")
        self.dashboard.update_dashboard()

    def copy_to_clipboard(self, text=None):
        text = text or self.corrected_text
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Text copied to clipboard")
