#!/usr/bin/env python
"""
Script auxiliar para verificar la configuración de Google Drive
"""
import os
import sys

def main():
    print("=" * 78)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN - Google Drive")
    print("=" * 78)
    
    # Verificar settings.py
    print("\n1. Verificando configuración...")
    settings_path = os.path.join(os.path.dirname(__file__), 'malware_detector', 'settings.py')
    
    if not os.path.exists(settings_path):
        print("   ❌ No se encontró malware_detector/settings.py")
        return False
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Verificar FOLDER_ID
    if 'GDRIVE_FOLDER_ID' in content:
        if '1XzpNMznSMxekWF6i4XoihiYEEynF4dtf' in content:
            print("   ✅ GDRIVE_FOLDER_ID configurado: 1XzpNMznSMxekWF6i4XoihiYEEynF4dtf")
        else:
            print("   ⚠️  GDRIVE_FOLDER_ID configurado pero con valor diferente")
    else:
        print("   ❌ GDRIVE_FOLDER_ID no encontrado en settings.py")
    
    # Verificar FILE_ID
    if 'GDRIVE_FILE_ID' in content:
        if 'GDRIVE_FILE_ID = None' in content or "GDRIVE_FILE_ID = 'TU_FILE_ID_AQUI'" in content:
            print("   ⚠️  GDRIVE_FILE_ID no configurado (necesitas configurarlo)")
            print("      → Ejecuta: python get_file_id_from_folder.py")
        else:
            # Extraer el FILE_ID
            for line in content.split('\n'):
                if 'GDRIVE_FILE_ID' in line and '=' in line and 'None' not in line:
                    file_id = line.split('=')[1].strip().strip("'").strip('"')
                    if file_id and file_id != 'TU_FILE_ID_AQUI':
                        print(f"   ✅ GDRIVE_FILE_ID configurado: {file_id[:20]}...")
                        break
    else:
        print("   ❌ GDRIVE_FILE_ID no encontrado en settings.py")
    
    # Verificar dataset local
    print("\n2. Verificando dataset local...")
    local_dataset = os.path.join(os.path.dirname(__file__), 'dataset', 'TotalFeatures-ISCXFlowMeter.csv')
    
    if os.path.exists(local_dataset):
        size_mb = os.path.getsize(local_dataset) / (1024 * 1024)
        print(f"   ✅ Dataset local encontrado: {size_mb:.2f} MB")
        print("      (Se usará el local en lugar de descargar)")
    else:
        print("   ℹ️  Dataset local no encontrado")
        print("      (Se descargará desde Google Drive)")
    
    # Verificar temp_data
    print("\n3. Verificando cache...")
    temp_dataset = os.path.join(os.path.dirname(__file__), 'temp_data', 'TotalFeatures-ISCXFlowMeter.csv')
    
    if os.path.exists(temp_dataset):
        size_mb = os.path.getsize(temp_dataset) / (1024 * 1024)
        print(f"   ✅ Dataset en cache: {size_mb:.2f} MB")
        print("      (Ya descargado desde Google Drive)")
    else:
        print("   ℹ️  No hay dataset en cache")
        print("      (Se descargará en el primer uso)")
    
    # Verificar requirements.txt
    print("\n4. Verificando dependencias...")
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            req_content = f.read()
        
        if 'gdown' in req_content:
            print("   ✅ gdown está en requirements.txt")
        else:
            print("   ❌ gdown NO está en requirements.txt")
    else:
        print("   ❌ requirements.txt no encontrado")
    
    # Verificar si gdown está instalado
    try:
        import gdown
        print("   ✅ gdown instalado")
    except ImportError:
        print("   ❌ gdown NO instalado")
        print("      → Ejecuta: pip install gdown")
    
    # Verificar .gitignore
    print("\n5. Verificando .gitignore...")
    gitignore_path = os.path.join(os.path.dirname(__file__), '.gitignore')
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        checks = {
            '/dataset': 'Carpeta dataset',
            '/temp_data': 'Carpeta temp_data',
            '*.pyc': 'Archivos compilados'
        }
        
        for pattern, desc in checks.items():
            if pattern in gitignore_content:
                print(f"   ✅ {desc} en .gitignore")
            else:
                print(f"   ⚠️  {desc} NO en .gitignore")
    else:
        print("   ⚠️  .gitignore no encontrado")
    
    # Resumen final
    print("\n" + "=" * 78)
    print("📋 RESUMEN")
    print("=" * 78)
    
    # Determinar estado
    file_id_configured = 'GDRIVE_FILE_ID' in content and 'None' not in content
    has_local_dataset = os.path.exists(local_dataset)
    has_cache_dataset = os.path.exists(temp_dataset)
    
    if has_local_dataset:
        print("\n✅ LISTO PARA DESARROLLO")
        print("   Usando dataset local")
    elif file_id_configured and has_cache_dataset:
        print("\n✅ LISTO PARA PRODUCCIÓN")
        print("   Dataset descargado y en cache")
    elif file_id_configured:
        print("\n⚠️  CASI LISTO")
        print("   FILE_ID configurado pero dataset no descargado")
        print("   → Ejecuta: python test_gdrive_download.py")
    else:
        print("\n⚠️  CONFIGURACIÓN INCOMPLETA")
        print("   Necesitas configurar GDRIVE_FILE_ID")
        print("   → Ejecuta: python get_file_id_from_folder.py")
    
    print("\n" + "=" * 78)
    print("📝 PRÓXIMOS PASOS")
    print("=" * 78)
    
    if not file_id_configured:
        print("\n1. Obtener FILE_ID:")
        print("   python get_file_id_from_folder.py")
        print("\n2. Probar descarga:")
        print("   python test_gdrive_download.py")
        print("\n3. Iniciar servidor:")
        print("   python manage.py runserver")
    elif not has_cache_dataset and not has_local_dataset:
        print("\n1. Probar descarga:")
        print("   python test_gdrive_download.py")
        print("\n2. Iniciar servidor:")
        print("   python manage.py runserver")
    else:
        print("\n✅ Todo configurado correctamente!")
        print("   python manage.py runserver")
    
    print("\n" + "=" * 78)

if __name__ == "__main__":
    main()

