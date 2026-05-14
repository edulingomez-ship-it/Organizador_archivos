import os
import shutil
import hashlib
import logging
from tkinter import messagebox

# Configuración de Logs (para que parezca pro)
logging.basicConfig(filename='gestion_archivos.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

MAPA_EXT = {
    'Documentos': ['.pdf', '.docx', '.txt'],
    'Imagenes': ['.jpg', '.png', '.gif'],
    'Software': ['.exe', '.msi', '.iso'],
    'Comprimidos': ['.zip', '.rar']
}

def calcular_hash(ruta):
    """Calcula el MD5 de un archivo para verificar si es duplicado."""
    hasher = hashlib.md5()
    with open(ruta, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def procesar_archivos(carpeta_origen):
    if not os.path.exists(carpeta_origen):
        return "La ruta no existe."

    conteo = 0
    for archivo in os.listdir(carpeta_origen):
        ruta_full = os.path.join(carpeta_origen, archivo)
        
        if os.path.isdir(ruta_full): continue

        nombre, ext = os.path.splitext(archivo)
        ext = ext.lower()

        for categoria, extensiones in MAPA_EXT.items():
            if ext in extensiones:
                destino_dir = os.path.join(carpeta_origen, categoria)
                os.makedirs(destino_dir, exist_ok=True)
                
                final_path = os.path.join(destino_dir, archivo)

                # Control de duplicados por Hash
                if os.path.exists(final_path):
                    if calcular_hash(ruta_full) == calcular_hash(final_path):
                        os.remove(ruta_full)
                        logging.info(f"Duplicado borrado: {archivo}")
                        break
                
                shutil.move(ruta_full, final_path)
                logging.info(f"Movido: {archivo} -> {categoria}")
                conteo += 1
                break
    return f"Proceso finalizado. Se han movido {conteo} archivos."

import tkinter as tk 
from tkinter import filedialog

def ejecutar_interfaz():
    root = tk.Tk ()
    root.title("ASIR File Sentinel v1.0")
    root.geometry("400x200")

    label = tk.Label(root, text="Organizador Automático de Archivos", font=("Arial", 12, "bold"))
    label.pack(pady=20)

    def seleccionar_y_correr():
        folder = filedialog.askdirectory()
        if folder:
            resultado = procesar_archivos(folder)
            messagebox.showinfo("Estado", resultado)

    btn = tk.Button(root, text="Seleccionar Carpeta y Organizar", 
                    command=seleccionar_y_correr, bg="#2c3e50", fg="white", pady=10)
    btn.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    ejecutar_interfaz()