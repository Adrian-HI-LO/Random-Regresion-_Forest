#!/usr/bin/env python
"""
Script auxiliar para obtener el file_id de un archivo dentro de una carpeta de Google Drive.
Esto es útil cuando solo tienes el folder_id.
"""
import sys

def print_instructions():
    """Imprimir instrucciones para obtener el file_id"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║            Cómo obtener el FILE_ID desde Google Drive                     ║
╚════════════════════════════════════════════════════════════════════════════╝

MÉTODO 1: Obtener FILE_ID directamente del archivo (RECOMENDADO)
═══════════════════════════════════════════════════════════════════════════

1. Ve a Google Drive en tu navegador
2. Abre la carpeta con ID: 1XzpNMznSMxekWF6i4XoihiYEEynF4dtf
3. Haz clic en el archivo CSV
4. Arriba a la derecha, haz clic en "Abrir en una nueva ventana" (ícono ⧉)
5. La URL cambiará a algo como:
   https://drive.google.com/file/d/FILE_ID_AQUI/view
   
6. Copia el FILE_ID_AQUI (la parte entre /d/ y /view)

7. Actualiza malware_detector/settings.py:
   
   GDRIVE_FILE_ID = 'EL_FILE_ID_QUE_COPIASTE'


MÉTODO 2: Compartir el archivo y obtener el enlace
═══════════════════════════════════════════════════════════════════════════

1. Ve a Google Drive
2. Haz clic derecho en el archivo CSV → "Compartir"
3. Cambia a "Cualquier persona con el enlace" → "Lector"
4. Haz clic en "Copiar enlace"
5. El enlace será algo como:
   https://drive.google.com/file/d/FILE_ID_AQUI/view?usp=sharing
   
6. Extrae el FILE_ID (entre /d/ y /view)


MÉTODO 3: Usar la API de Google Drive (avanzado)
═══════════════════════════════════════════════════════════════════════════

Si necesitas listar archivos programáticamente:

1. Ve a: https://console.cloud.google.com/
2. Crea un proyecto
3. Habilita Google Drive API
4. Crea credenciales (Service Account o OAuth2)
5. Usa la API para listar archivos en la carpeta


DESPUÉS DE OBTENER EL FILE_ID:
═══════════════════════════════════════════════════════════════════════════

1. Edita: malware_detector/settings.py

2. Cambia esta línea:
   GDRIVE_FILE_ID = None
   
   Por:
   GDRIVE_FILE_ID = 'TU_FILE_ID_AQUI'

3. Asegúrate de que el archivo sea público:
   - Cualquier persona con el enlace
   - Rol: Lector

4. Ejecuta la prueba:
   python test_gdrive_download.py

5. Si funciona, elimina la carpeta local (opcional):
   rm -rf dataset/


VERIFICAR QUE FUNCIONA:
═══════════════════════════════════════════════════════════════════════════

Puedes probar manualmente con:

  gdown https://drive.google.com/uc?id=TU_FILE_ID -O test.csv

Si esto descarga el archivo correctamente, entonces el FILE_ID es correcto.

═══════════════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    print_instructions()
    
    print("\n" + "─" * 78)
    print("INFORMACIÓN ACTUAL:")
    print("─" * 78)
    print(f"Folder ID configurado: 1XzpNMznSMxekWF6i4XoihiYEEynF4dtf")
    print(f"URL de la carpeta: https://drive.google.com/drive/folders/1XzpNMznSMxekWF6i4XoihiYEEynF4dtf")
    print("\nPor favor, sigue las instrucciones anteriores para obtener el FILE_ID.")
    print("═" * 78)

