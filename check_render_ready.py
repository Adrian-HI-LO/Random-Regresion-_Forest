#!/usr/bin/env python
"""
Verificación final antes de desplegar en Render
"""
import os
import sys

def check_render_ready():
    print("=" * 78)
    print("🚀 VERIFICACIÓN PRE-DEPLOY PARA RENDER")
    print("=" * 78)

    issues = []
    warnings = []

    base_dir = os.path.dirname(__file__)

    # 1. Verificar requirements.txt
    print("\n1. Verificando requirements.txt...")
    req_path = os.path.join(base_dir, 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            requirements = f.read()

        required_packages = {
            'Django': 'Django',
            'gdown': 'gdown',
            'gunicorn': 'gunicorn',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'scikit-learn': 'scikit-learn'
        }

        for name, package in required_packages.items():
            if package in requirements:
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name} NO encontrado")
                issues.append(f"Falta {package} en requirements.txt")
    else:
        print("   ❌ requirements.txt no encontrado")
        issues.append("requirements.txt no existe")

    # 2. Verificar settings.py
    print("\n2. Verificando settings.py...")
    settings_path = os.path.join(base_dir, 'malware_detector', 'settings.py')
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = f.read()

        # FILE_ID
        if 'GDRIVE_FILE_ID' in settings:
            if "GDRIVE_FILE_ID = '1ZLOcViao8-CXSRHImjIZSfoggqfIylro'" in settings or \
               ('GDRIVE_FILE_ID = ' in settings and 'None' not in settings):
                print("   ✅ GDRIVE_FILE_ID configurado")
            else:
                print("   ⚠️  GDRIVE_FILE_ID no configurado")
                warnings.append("FILE_ID no configurado - se usará FOLDER_ID")

        # ALLOWED_HOSTS
        if "ALLOWED_HOSTS = ['*']" in settings or "ALLOWED_HOSTS = []" in settings:
            print("   ✅ ALLOWED_HOSTS configurado")
        else:
            print("   ⚠️  ALLOWED_HOSTS puede necesitar ajuste")
            warnings.append("Verifica ALLOWED_HOSTS para tu dominio")

        # STATIC_ROOT
        if 'STATIC_ROOT' in settings:
            print("   ✅ STATIC_ROOT configurado")
        else:
            print("   ❌ STATIC_ROOT no configurado")
            issues.append("Falta STATIC_ROOT en settings.py")
    else:
        print("   ❌ settings.py no encontrado")
        issues.append("settings.py no existe")

    # 3. Verificar .gitignore
    print("\n3. Verificando .gitignore...")
    gitignore_path = os.path.join(base_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore = f.read()

        important_patterns = {
            '/dataset': 'Dataset local',
            '/temp_data': 'Cache de Google Drive',
            '/staticfiles': 'Archivos estáticos compilados',
            '*.pyc': 'Archivos Python compilados',
            'db.sqlite3': 'Base de datos local'
        }

        for pattern, desc in important_patterns.items():
            if pattern in gitignore:
                print(f"   ✅ {desc}")
            else:
                print(f"   ⚠️  {desc} no en .gitignore")
                warnings.append(f"Considera agregar {pattern} a .gitignore")
    else:
        print("   ⚠️  .gitignore no encontrado")
        warnings.append(".gitignore recomendado pero no crítico")

    # 4. Verificar que dataset/ NO exista o esté en .gitignore
    print("\n4. Verificando dataset...")
    dataset_path = os.path.join(base_dir, 'dataset')
    if os.path.exists(dataset_path):
        if '/dataset' in gitignore:
            print("   ✅ Dataset local existe pero está en .gitignore (OK)")
        else:
            print("   ⚠️  Dataset local existe y NO está en .gitignore")
            warnings.append("Dataset local se subirá al repo (no recomendado)")
    else:
        print("   ✅ Dataset local no existe (se descargará en Render)")

    # 5. Verificar Google Drive
    print("\n5. Verificando configuración de Google Drive...")
    if 'GDRIVE_FILE_ID' in settings:
        file_id_line = [line for line in settings.split('\n') if 'GDRIVE_FILE_ID = ' in line and 'None' not in line]
        if file_id_line:
            print("   ✅ FILE_ID configurado")
            print("   ℹ️  El dataset se descargará automáticamente en Render")
        else:
            print("   ⚠️  FILE_ID no configurado")
            warnings.append("Configura FILE_ID para mejor confiabilidad")

    # 6. Verificar archivos Django básicos
    print("\n6. Verificando estructura Django...")
    important_files = {
        'manage.py': 'Script de gestión Django',
        'malware_detector/wsgi.py': 'WSGI para producción',
        'malware_detector/urls.py': 'URLs principales',
    }

    for file_path, desc in important_files.items():
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {desc}")
        else:
            print(f"   ❌ {desc} no encontrado")
            issues.append(f"Falta {file_path}")

    # Resumen final
    print("\n" + "=" * 78)
    print("📋 RESUMEN")
    print("=" * 78)

    if not issues and not warnings:
        print("\n✅ ¡PERFECTO! Tu proyecto está 100% listo para Render")
        print("\n🚀 Próximos pasos:")
        print("   1. git add .")
        print("   2. git commit -m 'Listo para Render'")
        print("   3. git push")
        print("   4. Despliega en render.com")
        return True

    elif not issues and warnings:
        print("\n✅ Tu proyecto está LISTO para Render")
        print("\n⚠️  Advertencias (no críticas):")
        for warning in warnings:
            print(f"   • {warning}")

        print("\n🚀 Puedes desplegar ahora:")
        print("   1. git add .")
        print("   2. git commit -m 'Listo para Render'")
        print("   3. git push")
        print("   4. Despliega en render.com")
        return True

    else:
        print("\n❌ Hay problemas que deben corregirse:")
        for issue in issues:
            print(f"   • {issue}")

        if warnings:
            print("\n⚠️  Advertencias:")
            for warning in warnings:
                print(f"   • {warning}")

        print("\n🔧 Corrige los problemas antes de desplegar")
        return False

    print("\n" + "=" * 78)

if __name__ == "__main__":
    ready = check_render_ready()

    print("\n" + "=" * 78)
    print("📚 CONFIGURACIÓN DE RENDER")
    print("=" * 78)
    print("""
Build Command:     pip install -r requirements.txt
Start Command:     gunicorn malware_detector.wsgi:application --bind 0.0.0.0:$PORT
Python Version:    3.11 (o superior)
Instance Type:     Starter (o superior recomendado)

⏱️  Primera descarga: ~10-20 minutos (incluye dataset)
⚡  Siguientes deploys: ~5-8 minutos (usa cache)
""")
    print("=" * 78)

    sys.exit(0 if ready else 1)

