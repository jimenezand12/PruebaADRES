from django.shortcuts import render
import csv, io
from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import UploadFileForm

def cargar_archivo(request):
    errors = []
    success = False
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Leer todo el contenido del archivo y decodificarlo
            raw = request.FILES['file'].read().decode('utf-8')
            reader = csv.reader(io.StringIO(raw))
            for row_num, row in enumerate(reader, start=1):
                # a) verificar exactamente 5 columnas
                if len(row) != 5:
                    errors.append(f"Fila {row_num}: {len(row)} columnas (deben ser 5)")
                    continue

                # b) Columna 1: entero entre 3 y 10 dígitos
                col1 = row[0].strip()
                if not (col1.isdigit() and 3 <= len(col1) <= 10):
                    errors.append(f"Fila {row_num}, Columna 1: '{col1}' no es un entero de 3–10 dígitos")

                # c) Columna 2: email válido
                col2 = row[1].strip()
                try:
                    validate_email(col2)
                except ValidationError:
                    errors.append(f"Fila {row_num}, Columna 2: '{col2}' no es un correo válido")

                # d) Columna 3: solo “CC” o “TI”
                col3 = row[2].strip()
                if col3 not in ('CC', 'TI'):
                    errors.append(f"Fila {row_num}, Columna 3: '{col3}' debe ser 'CC' o 'TI'")

                # e) Columna 4: número entre 500000 y 1500000
                col4 = row[3].strip()
                try:
                    val4 = int(col4)
                    if not (500000 <= val4 <= 1500000):
                        errors.append(f"Fila {row_num}, Columna 4: {val4} fuera de rango (500000–1500000)")
                except ValueError:
                    errors.append(f"Fila {row_num}, Columna 4: '{col4}' no es un entero")

                # f) Columna 5: cualquier valor → no valida

            if not errors:
                success = True
    else:
        form = UploadFileForm()

    return render(request, 'validar/upload.html', {
        'form': form,
        'errors': errors,
        'success': success,
        })