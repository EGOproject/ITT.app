import os
import tkinter as tk
from tkinter import ttk, messagebox
from file_operations import load_previous_jobs, save_as_word, save_as_pdf, save_as_text

class Dashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Job', 'Actions'), show='headings')
        self.tree.heading('Job', text='Job')
        self.tree.heading('Actions', text='Actions')
        self.tree.pack()

        self.new_button = tk.Button(self, text='Start New', command=self.app.start_new)
        self.new_button.pack()

        self.tree.bind('<Double-1>', self.on_double_click)
        self.update_dashboard()

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        job_name = self.tree.item(item, 'values')[0]
        jobs = load_previous_jobs()
        job = next(job for job in jobs if job['name'] == job_name)

        self.show_job_options(job)

    def show_job_options(self, job):
        self.options_window = tk.Toplevel(self)
        self.options_window.title(f"Options for {job['name']}")

        self.text_widget = tk.Text(self.options_window, wrap='word')
        self.text_widget.pack()
        self.text_widget.insert(tk.END, job['text'])

        self.save_word_button = tk.Button(self.options_window, text="Save as Word", command=lambda: save_as_word(job['text'], job['path'] + ".docx"))
        self.save_word_button.pack()

        self.save_pdf_button = tk.Button(self.options_window, text="Save as PDF", command=lambda: save_as_pdf(job['text'], job['path'] + ".pdf"))
        self.save_pdf_button.pack()

        self.save_text_button = tk.Button(self.options_window, text="Save as Text", command=lambda: save_as_text(job['text'], job['path'] + ".txt"))
        self.save_text_button.pack()

        self.copy_button = tk.Button(self.options_window, text="Copy to Clipboard", command=lambda: self.app.copy_to_clipboard(job['text']))
        self.copy_button.pack()

        self.delete_button = tk.Button(self.options_window, text="Delete Job", command=lambda: self.delete_job(job))
        self.delete_button.pack()

    def delete_job(self, job):
        os.remove(job['path'])
        self.update_dashboard()

    def update_dashboard(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        jobs = load_previous_jobs()
        for job in jobs:
            self.tree.insert('', 'end', values=(job['name'], 'Actions'))
