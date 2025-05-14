import os
import sqlite3
import re
from pathlib import Path
from PyPDF2 import PdfReader

# Expresión regular suministrada
pattern = re.compile(r"\b([0-9A-Fa-f]\n*){95,100}\b")

# Configuración SQLite 
db_path = "facturas.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS facturas (
    nombre_archivo TEXT,
    num_paginas INTEGER,
    cufe TEXT,
    peso INTEGER
)
""")
conn.commit()

# Carpeta en la cual se almacenan las facturas a procesar
pdf_dir = Path("facturas")

for pdf_file in pdf_dir.glob("*.pdf"):
    nombre = pdf_file.name
    peso = pdf_file.stat().st_size 

    # lectura de pdf
    reader = PdfReader(str(pdf_file))
    num_paginas = len(reader.pages)

    texto = []
    for page in reader.pages:
        try:
            texto.append(page.extract_text() or "")
        except Exception:
            texto.append("")
    texto_completo = "\n".join(texto)

    # CUFE 
    match = pattern.search(texto_completo)
    cufe = match.group(0).replace("\n", "") if match else None

    cursor.execute(
        "INSERT INTO facturas (nombre_archivo, num_paginas, cufe, peso) VALUES (?, ?, ?, ?)",
        (nombre, num_paginas, cufe, peso)
    )
    conn.commit()

conn.close()

print(f"Proceso completado. Datos almacenados en {db_path}")