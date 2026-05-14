import os
import shutil
import hashlib
import logging
from tkinter import messagebox

# Log Configuration (to look professional)
logging.basicConfig(filename='file_management.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

EXT_MAP = {
    'Documents': ['.pdf', '.docx', '.txt'],
    'Images': ['.jpg', '.png', '.gif'],
    'Software': ['.exe', '.msi', '.iso'],
    'Compressed': ['.zip', '.rar']
}

def calculate_hash(path):
    """Calculates the MD5 of a file to check if it is a duplicate."""
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def process_files(source_folder):
    if not os.path.exists(source_folder):
        return "The path does not exist."

    count = 0
    for file in os.listdir(source_folder):
        full_path = os.path.join(source_folder, file)

        if os.path.isdir(full_path):
            continue

        name, ext = os.path.splitext(file)
        ext = ext.lower()

        for category, extensions in EXT_MAP.items():
            if ext in extensions:
                dest_dir = os.path.join(source_folder, category)
                os.makedirs(dest_dir, exist_ok=True)

                final_path = os.path.join(dest_dir, file)

                # Duplicate control by Hash
                if os.path.exists(final_path):
                    if calculate_hash(full_path) == calculate_hash(final_path):
                        os.remove(full_path)
                        logging.info(f"Duplicate deleted: {file}")
                        break

                shutil.move(full_path, final_path)
                logging.info(f"Moved: {file} -> {category}")
                count += 1
                break
    return f"Process completed. {count} files have been moved."

import tkinter as tk
from tkinter import filedialog

def run_interface():
    root = tk.Tk()
    root.title("ASIR File Sentinel v1.0")
    root.geometry("400x200")

    label = tk.Label(root, text="Automatic File Organizer", font=("Arial", 12, "bold"))
    label.pack(pady=20)

    def select_and_run():
        folder = filedialog.askdirectory()
        if folder:
            result = process_files(folder)
            messagebox.showinfo("Status", result)

    btn = tk.Button(root, text="Select Folder and Organize",
                    command=select_and_run, bg="#2c3e50", fg="white", pady=10)
    btn.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    run_interface()