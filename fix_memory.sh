#!/bin/bash
# Script para aplicar la solución de memoria y subir a GitHub

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   🔧 APLICANDO SOLUCIÓN DE MEMORIA PARA RENDER              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Verificar cambios
echo "1. Verificando cambios..."
git status --short
echo ""

# 2. Agregar archivos
echo "2. Agregando archivos..."
git add analyzer/ml_models.py analyzer/views.py gunicorn_config.py SOLUCION_MEMORIA.txt CONFIGURAR_DATASET_SIZE.txt templates/dashboard.html
echo "✅ Archivos agregados"
echo ""

# 3. Commit
echo "3. Haciendo commit..."
git commit -m "Fix dataset view + banner info subset + configuración tamaño dataset"
echo ""

# 4. Push
echo "4. Subiendo a GitHub..."
git push origin main
echo ""

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                     ✅ COMPLETADO                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 PRÓXIMOS PASOS EN RENDER:"
echo ""
echo "1. Ve a tu Web Service en Render"
echo ""
echo "2. Settings → Build & Deploy"
echo "   Cambiar Start Command a:"
echo "   gunicorn malware_detector.wsgi:application -c gunicorn_config.py"
echo ""
echo "3. Settings → Environment"
echo "   Agregar variable:"
echo "   USE_DATASET_SUBSET = true"
echo ""
echo "4. Manual Deploy → Deploy latest commit"
echo ""
echo "5. Espera 5-10 minutos"
echo ""
echo "6. ¡Debería funcionar sin Out of Memory! 🎉"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📖 Para más detalles, lee: SOLUCION_MEMORIA.txt"
echo ""

